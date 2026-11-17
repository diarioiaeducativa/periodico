#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El reparador del diario (ADR 0087): cuando algo falla, un agente con terminal lo diagnostica y lo arregla
en una copia, y este programa, sin IA, comprueba el resultado antes de ponerlo en el número.

    scripts/reparador.py incidencia [--sin-aviso] [--bloqueo] [--fecha AAAA-MM-DD] "qué ha fallado"
    scripts/reparador.py incidencia --sin-aviso --registro registro/F.log --desde LÍNEA   (los AVISO y ERROR del registro)
    scripts/reparador.py atender        atiende la cola (lo lanza solo `incidencia`, aparte)
    scripts/reparador.py estado         la cola y las últimas reparaciones
    scripts/reparador.py medir FECHA    cómo está el número de esa fecha, según las comprobaciones

Es la única puerta de los fallos: lo que antes se le avisaba a Juanjo pasa primero por aquí. Si el agente lo
arregla y la comprobación lo da por bueno, a Juanjo le llega un solo mensaje con lo que falló y lo que se hizo.
Si no, le llega el aviso de siempre, con el diagnóstico. `--sin-aviso` es para lo que antes solo quedaba en el
registro: si no hay nada que arreglar, no se le dice nada. `--bloqueo`, para cuando el número no ha llegado a
prepararse: el segundo intento de la noche espera a que el reparador acabe.

Lo que hace `atender`, una incidencia (o las que haya juntas) cada vez:
 1. Copia la redacción a una carpeta aparte y mide cómo está el número (`medir`).
 2. Lanza Claude Code con Opus, con terminal, en esa copia y con un tope de tiempo: antes de publicar, el que
    quede hasta las 6:40 (hasta las 6:25 si el número no está preparado). Sin tiempo, espera a que salga el
    número y lo arregla después.
 3. Comprueba, sin IA: que no ha tocado lo protegido (este programa, sus instrucciones, lo que publica), que los
    JSON del día valen, que el texto de los artículos y de la viñeta es el mismo, que el generador funciona y
    que ninguna medida ha empeorado. Si algo no se cumple, no se aplica nada.
 4. Lleva a la redacción solo los archivos cambiados (si mientras tanto no han cambiado allí), guarda en git lo
    que sea código, rehace el sitio y, con el número ya publicado, vuelve a publicar la web.
 5. Lo apunta en registro/reparador.jsonl y avisa.

REPARADOR=0 (o el archivo estado/reparador/apagado) lo desconecta: los avisos salen como antes.
"""
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

RAIZ = pathlib.Path(os.environ.get("REPARADOR_RAIZ") or pathlib.Path(__file__).resolve().parent.parent)
ESTADO = RAIZ / "estado" / "reparador"
COLA = ESTADO / "cola"
REGISTRO = RAIZ / "registro" / "reparador.jsonl"
MODELO = os.environ.get("MODELO_REPARADOR", "claude-opus-5-5")   # por su nombre exacto
MINUTOS = int(os.environ.get("REPARADOR_MIN", "45"))             # tope de cada reparación
ESPERA = int(os.environ.get("REPARADOR_ESPERA", "120"))          # para atender juntos los avisos de un mismo fallo
TRABAJO = pathlib.Path(os.environ.get("REPARADOR_TRABAJO", "/tmp/reparador"))
LIMITE_BLOQUEO, LIMITE_ANTES = 6 * 60 + 25, 6 * 60 + 40          # el plan B salta a las 6:30 y se publica a las 6:50
MINIMO = 15                                                       # con menos minutos no se empieza
DESTINATARIO = "Diario de IA Educativa"

# Lo que no entra en la copia ni se compara: lo que se genera, lo que pesa y lo que es de cada momento
FUERA = ("sitio", ".git", "cache", "estado", "registro", "instagram", "indice", "__pycache__", "node_modules",
         "registro-pruebas", "prototipos")
# Lo que el agente no puede cambiar: a sí mismo, lo que publica o envía y lo que corre fuera del contenedor
PROTEGIDO = ("scripts/reparador.py", "encargos/reparador.md", "nas/", ".github/", "ionos/", "android/",
             "scripts/publicar-nas.sh", "scripts/publicar-web.sh", "scripts/instagram.py", "scripts/redes/",
             "scripts/vigilante.sh", "scripts/subir-videos.py", "scripts/archivar.py", "scripts/avisos-personas.py",
             "scripts/buscar-mcp.json", "LICENSE", "LICENSE-CODIGO")
# Lo que, si cambia, es código y se guarda en git
CODIGO = re.compile(r"^(scripts/|encargos/|estaticos/|docs/|[^/]+\.(py|sh|js|md|json|css)$)")
TEXTOS = ("antetitulo", "titular", "entradilla", "cuerpo", "texto", "cartela")   # lo que lee el público y no se reescribe
CARPETAS_DIA = ("ediciones", "biblioteca", "repositorio", "hace-un-ano", "reportajes", "vinetas")
INFORME = "reparador-informe.json"


def ahora():
    return datetime.datetime.now()


def minutos_del_dia():
    a = ahora()
    return a.hour * 60 + a.minute


def dia_del_numero():
    """La fecha de las conversaciones del número de hoy, como en reloj.sh: ayer."""
    return (ahora().date() - datetime.timedelta(days=1)).isoformat()


def apagado():
    return os.environ.get("REPARADOR") == "0" or (ESTADO / "apagado").exists()


def avisar(texto):
    if os.environ.get("REPARADOR_SIN_AVISOS") == "1":   # en las pruebas
        print(f"[aviso a Juanjo] {texto}")
        return
    subprocess.run(["avisar-juanjo", "--de", DESTINATARIO, texto[:3500]], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def apuntar(**datos):
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open("a") as f:
        f.write(json.dumps({"hora": ahora().isoformat(timespec="seconds"), **datos}, ensure_ascii=False) + "\n")


# --- la cola -------------------------------------------------------------------------------------------------

def incidencia(args):
    aviso, bloqueo, fecha, registro, desde, resto = True, False, None, None, 0, []
    it = iter(args)
    for a in it:
        if a == "--sin-aviso":
            aviso = False
        elif a == "--bloqueo":
            bloqueo = True
        elif a == "--fecha":
            fecha = next(it)
        elif a == "--registro":
            registro = next(it)
        elif a == "--desde":
            desde = int(next(it) or 0)
        else:
            resto.append(a)
    mensaje = " ".join(resto).strip()
    if registro:   # los AVISO y ERROR que la noche dejó en su registro y no se le dijeron a nadie
        try:
            lineas = pathlib.Path(registro).read_text(errors="replace").splitlines()[desde:]
        except OSError:
            lineas = []
        graves = [x for x in lineas if re.search(r"^\S+ \S+  (AVISO|ERROR)", x)]
        if not graves:
            return 0
        mensaje = (mensaje + " " if mensaje else "") + f"Avisos y errores en {registro}: " + " | ".join(graves)[:3000]
    if not mensaje:
        return 0
    if apagado():
        if aviso:
            avisar(mensaje)
        return 0
    COLA.mkdir(parents=True, exist_ok=True)
    nombre = f"{ahora():%Y%m%d-%H%M%S}-{os.getpid()}.json"
    (COLA / nombre).write_text(json.dumps({"hora": ahora().isoformat(timespec="seconds"), "mensaje": mensaje,
                                           "aviso": aviso, "bloqueo": bloqueo, "fecha": fecha or dia_del_numero()},
                                          ensure_ascii=False))
    if bloqueo:
        (ESTADO / "bloqueo").write_text(nombre)
    if os.environ.get("REPARADOR_NO_LANZAR") != "1":   # el que atiende va aparte: quien avisa no espera
        subprocess.Popen([sys.executable, str(pathlib.Path(__file__).resolve()), "atender"], cwd=RAIZ, start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


def tomar_cola():
    incs = []
    for f in sorted(COLA.glob("*.json")):
        try:
            incs.append(json.loads(f.read_text()))
        except (OSError, ValueError):
            pass
        f.unlink(missing_ok=True)
    return incs


def coger_turno():
    """Un solo reparador a la vez. Devuelve False si ya hay otro vivo."""
    ESTADO.mkdir(parents=True, exist_ok=True)
    marca = ESTADO / "en-marcha"
    if marca.exists():
        try:
            os.kill(int(marca.read_text().strip()), 0)
            return False
        except (ValueError, OSError):
            pass   # se quedó la marca de uno que murió
    marca.write_text(str(os.getpid()))
    return True


# --- medir ---------------------------------------------------------------------------------------------------

def correr(orden, raiz, tope=900, entorno=None):
    try:
        r = subprocess.run(orden, check=False, cwd=raiz, capture_output=True, text=True, timeout=tope, env=entorno)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "se pasó de tiempo"
    except OSError as ex:
        return 127, str(ex)


def json_del_dia(raiz, fecha):
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    fs = [f for patron in (f"*/{fecha}.json", f"*/*/{fecha}.json", f"*/{fecha}-*.json") for f in raiz.glob(patron)]
    fs += [raiz / "avisos" / f"{publica}.json"]
    return sorted({f for f in fs if f.is_file() and not any(p in FUERA for p in f.relative_to(raiz).parts)})


def leer(f):
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return None


def medir(raiz, fecha, maqueta=True):
    """Cómo está el número, con las comprobaciones sin IA del diario. Cuanto más bajo, mejor."""
    m = {"json_rotos": sum(1 for f in json_del_dia(raiz, fecha) if leer(f) is None)}
    codigo, salida = correr([sys.executable, "generar.py"], raiz)
    m["generador"] = codigo == 0
    if codigo != 0:
        m["generador_error"] = salida[-1500:]
    try:
        idiomas = correr([sys.executable, "scripts/idiomas.py", "lista"], raiz)[1].split()
    except Exception:   # noqa: BLE001
        idiomas = []
    faltan, mal = [], []
    for tipo in ("edicion", "biblioteca", "repositorio", "hace-un-ano", "reportaje"):
        for c in idiomas:
            faltan += [x for x in correr([sys.executable, "scripts/idiomas.py", "falta", tipo, fecha, c], raiz)[1].splitlines() if x.strip()]
            mal += [x for x in correr([sys.executable, "scripts/idiomas.py", "comprobar", tipo, fecha, c, "--mirar"], raiz)[1].splitlines() if x.strip()]
    m["traducciones_faltan"], m["traducciones_mal"] = len(faltan), len(mal)
    m["detalle"] = (faltan + mal)[:12]
    if m["generador"]:
        m["castellano_colado"] = len([x for x in correr([sys.executable, "scripts/revisar-idiomas.py", "--dia", fecha], raiz)[1].splitlines() if x.strip()])
        codigo, salida = correr([sys.executable, "scripts/revisar-estilo.py", "--dia", fecha], raiz)
        m["estilo"] = len([x for x in salida.splitlines() if x.strip()]) if codigo == 4 else 0
        if maqueta and os.environ.get("REPARADOR_SIN_MAQUETA") != "1":
            (raiz / "registro").mkdir(exist_ok=True)
            correr([sys.executable, "scripts/revisar-maqueta.py", fecha, "--sin-aviso"], raiz, tope=600)
            huecos = leer(raiz / "registro" / f"{fecha}-maqueta.json")
            if isinstance(huecos, list):
                m["maqueta"] = len(huecos)
    return m


def empeora(antes, despues):
    """Las medidas que han ido a peor."""
    peor = []
    if not despues.get("generador"):
        peor.append("el generador no funciona: " + (despues.get("generador_error") or "")[-300:])
    if despues.get("json_rotos"):
        peor.append(f"quedan {despues['json_rotos']} JSON del día que no valen")
    # Con el generador parado o un original roto, las medidas de antes no dicen nada: no había número que medir
    if antes.get("generador") and not antes.get("json_rotos"):
        for k in ("traducciones_faltan", "traducciones_mal", "castellano_colado", "estilo", "maqueta"):
            if k in antes and k in despues and despues[k] > antes[k]:
                peor.append(f"{k.replace('_', ' ')}: de {antes[k]} a {despues[k]}")
    return peor


# --- la copia y la comprobación --------------------------------------------------------------------------------

def huella(f):
    try:
        return hashlib.sha1(f.read_bytes()).hexdigest()
    except OSError:
        return None


def archivos(raiz):
    """Los archivos que cuentan, con su huella."""
    salida = {}
    for carpeta, subs, nombres in os.walk(raiz):
        rel = pathlib.Path(carpeta).relative_to(raiz)
        subs[:] = [s for s in subs if s not in FUERA and not (rel == pathlib.Path(".") and s in FUERA)]
        for n in nombres:
            f = pathlib.Path(carpeta) / n
            if f.is_file() and not f.is_symlink():
                salida[str(rel / n) if str(rel) != "." else n] = huella(f)
    return salida


def copiar(destino):
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    excluye = [x for d in FUERA for x in ("--exclude", f"/{d}/")] + ["--exclude", "__pycache__/", "--exclude", "*.mp4"]
    subprocess.run(["rsync", "-a", *excluye, f"{RAIZ}/", f"{destino}/"], check=True)
    # El registro del día y el estado, para leer: el agente los necesita para diagnosticar
    for d in ("registro", "estado"):
        if (RAIZ / d).is_dir():
            subprocess.run(["rsync", "-a", "--exclude", "/reparador/", "--exclude", "*.png", f"{RAIZ}/{d}/", f"{destino}/{d}/"], check=False)
    (destino / INFORME).unlink(missing_ok=True)


def firma_textos(x, dentro=False):
    """Los textos que lee el público, en párrafos y ordenados: lo que el reparador no puede reescribir."""
    salida = []
    if isinstance(x, dict):
        for k, v in x.items():
            salida += firma_textos(v, dentro or k in TEXTOS) if k in TEXTOS or isinstance(v, (dict, list)) else []
    elif isinstance(x, list):
        for v in x:
            salida += firma_textos(v, dentro)
    elif isinstance(x, str) and dentro:
        salida += [" ".join(p.split()) for p in re.split(r"\n\s*\n", x) if p.strip()]
    return salida


def protegido(ruta):
    return any(ruta == p or (p.endswith("/") and ruta.startswith(p)) for p in PROTEGIDO)


def comprobar(copia, fecha, antes_archivos, antes_textos, antes_medidas, informe):
    """Devuelve (cambiados, borrar, medidas, problemas): si hay problemas, no se aplica nada."""
    problemas = []
    despues = archivos(copia)
    cambiados = sorted(r for r, h in despues.items() if antes_archivos.get(r) != h and r != INFORME
                       and not r.startswith("revision/") and not r.endswith(".pyc"))
    borrar = []
    for r in informe.get("borrar") or []:
        r = str(r).lstrip("/")
        if ".." in pathlib.PurePosixPath(r).parts or protegido(r) or CODIGO.match(r) or r.split("/")[0] in FUERA:
            problemas.append(f"quiere borrar algo que no puede: {r}")
        elif r in antes_archivos:
            borrar.append(r)
    for r in cambiados:
        if protegido(r):
            problemas.append(f"ha tocado algo protegido: {r}")
    for r in antes_archivos:
        if r not in despues and r not in borrar and not r.startswith("revision/"):
            if protegido(r) or CODIGO.match(r):
                problemas.append(f"ha borrado {r}")
    for carpeta in CARPETAS_DIA:   # el texto de los artículos y de la viñeta, el mismo que antes
        clave = f"{carpeta}/{fecha}.json"
        if antes_textos.get(clave) is None:
            continue
        ahora_ = leer(copia / clave)
        if ahora_ is None or sorted(firma_textos(ahora_)) != antes_textos[clave]:
            problemas.append(f"ha cambiado el texto de {clave}, y no puede reescribir lo que escribió la redacción")
    for r in cambiados:   # el código cambiado, que al menos se pueda leer
        f = copia / r
        if r.endswith(".py"):
            c, s = correr([sys.executable, "-m", "py_compile", str(f)], copia)
        elif r.endswith(".sh"):
            c, s = correr(["bash", "-n", str(f)], copia)
        elif r.endswith(".json"):
            c, s = (0, "") if leer(f) is not None else (1, "no es JSON válido")
        else:
            continue
        if c != 0:
            problemas.append(f"{r} no vale: {(s.strip().splitlines() or [''])[-1][:200]}")
    medidas = {}
    if not problemas:
        medidas = medir(copia, fecha)
        problemas += empeora(antes_medidas, medidas)
    return cambiados, borrar, medidas, problemas


def aplicar(copia, cambiados, borrar, en_redaccion):
    """Lleva a la redacción lo cambiado, si allí no ha cambiado mientras tanto."""
    for r in cambiados + borrar:
        if huella(RAIZ / r) != en_redaccion.get(r):
            return f"{r} ha cambiado en la redacción mientras se reparaba"
    for r in cambiados:
        (RAIZ / r).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(copia / r, RAIZ / r)
    for r in borrar:
        (RAIZ / r).unlink(missing_ok=True)
    return ""


def guardar_codigo(cambiados, informe):
    """Lo que es código, a git, para que no se pierda: un commit con el motivo y la nota del modelo."""
    codigo = [r for r in cambiados if CODIGO.match(r)]
    seguidos = correr(["git", "ls-files", "--", *codigo], RAIZ)[1].split() if codigo else []
    nuevos = [r for r in codigo if r not in seguidos and (r.startswith(("scripts/", "encargos/", "docs/")))]
    codigo = [r for r in codigo if r in seguidos] + nuevos
    if not codigo or not (RAIZ / ".git").exists():
        return []
    motivo = " ".join(str(informe.get("commit") or informe.get("que_fallaba") or "arreglo").split())[:160]
    correr(["git", "add", "--", *codigo], RAIZ)
    c, s = correr(["git", "commit", "-q", "-m", f"Reparador: {motivo}",
                   "-m", " ".join(str(informe.get("que_he_hecho") or "").split())[:900], "--", *codigo], RAIZ)
    if c != 0:
        return []
    correr(["git", "notes", "--ref=ia", "add", "-f", "-m",
            f"Modelo: Claude Opus 5.5 ({MODELO}) · Claude Code, reparador del diario en el NAS (ADR 0087)", "HEAD"], RAIZ)
    if os.environ.get("REPARADOR_SIN_PUSH") != "1":   # si no sube ahora, sube con el número
        if correr(["git", "push", "-q"], RAIZ, tope=120)[0] == 0:
            correr(["git", "push", "-q", "origin", "refs/notes/ia"], RAIZ, tope=120)
    return codigo


# --- el agente -----------------------------------------------------------------------------------------------

def lanzar_agente(copia, incs, fecha, fase, minutos, medidas, ident):
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    encargo = (copia / "encargos" / "reparador.md").read_text()
    situacion = {"antes": "El número está preparado y aún no se ha publicado (sale a las 6:50).",
                 "bloqueo": "El número NO ha llegado a prepararse: la noche (scripts/noche.sh) ha fallado. Arregla la causa; después la noche se repite sola.",
                 "despues": "El número de hoy ya se ha publicado. Si lo que arreglas cambia la web, se volverá a publicar sola."}[fase]
    texto = (encargo + "\n\n## Esta vez\n\n"
             f"- Fecha de las conversaciones (FECHA): {fecha}. Fecha de cabecera del número: {publica}.\n"
             f"- {situacion}\n- Tienes {minutos} minutos; pasado ese tiempo se te corta y no se aplica nada.\n"
             f"- La redacción de verdad está en {RAIZ} (solo para mirar; su historial, con `git -C {RAIZ} log`). Tu copia: {copia}.\n"
             "- Cómo está el número según las comprobaciones (cuanto más bajo, mejor): "
             + json.dumps({k: v for k, v in medidas.items() if k != "generador_error"}, ensure_ascii=False) + "\n"
             + ("- El generador falla así:\n```\n" + medidas["generador_error"] + "\n```\n" if medidas.get("generador_error") else "")
             + "\n### Lo que ha fallado\n\n" + "\n".join(f"- ({i['hora']}) {i['mensaje']}" for i in incs) + "\n")
    casa = copia.parent / "casa"   # sin las claves de despliegue ni los permisos de las redes a mano
    (casa / "bin").mkdir(parents=True, exist_ok=True)
    mudo = casa / "bin" / "avisar-juanjo"   # lo que el agente ponga en marcha no avisa a nadie: avisa este programa
    mudo.write_text(f"#!/bin/sh\necho \"$*\" >> '{casa}/avisos.txt'\n")
    mudo.chmod(0o755)
    entorno = dict(os.environ, HOME=str(casa), PATH=f"{casa}/bin:{os.environ.get('PATH', '')}", REPARADOR="0",
                   REPARADOR_NO_LANZAR="1")
    orden = ["timeout", str(minutos * 60), "claude", "-p", "--model", MODELO, "--permission-mode", "acceptEdits",
             "--allowedTools", "Bash", "Read", "Edit", "Write", "Glob", "Grep", "WebFetch", "WebSearch",
             "--output-format", "json"]
    inicio = time.time()
    try:
        r = subprocess.run(orden, check=False, input=texto, cwd=copia, capture_output=True, text=True, env=entorno, timeout=minutos * 60 + 60)
        codigo, salida = r.returncode, r.stdout
    except subprocess.TimeoutExpired:
        codigo, salida = 124, ""
    except OSError as ex:
        codigo, salida = 127, str(ex)
    shutil.rmtree(casa, ignore_errors=True)
    datos = {}
    try:
        datos = json.loads(salida)
    except ValueError:
        pass
    (RAIZ / "registro").mkdir(exist_ok=True)
    (RAIZ / "registro" / f"reparador-{ident}.log").write_text(texto + "\n\n===== RESPUESTA =====\n" + str(datos.get("result") or salida)[-20000:])
    return codigo, round(time.time() - inicio), datos.get("total_cost_usd")


# --- atender -------------------------------------------------------------------------------------------------

def esperar(condicion, hasta_minuto, cada=30):
    """Espera a que se cumpla la condición, como mucho hasta ese minuto del día. Devuelve si se cumplió."""
    while not condicion():
        if minutos_del_dia() >= hasta_minuto:
            return False
        time.sleep(cada)
    return True


def reenviar(incs, diagnostico="", siempre=False):
    """Los avisos tal como habrían llegado sin reparador, con lo que se sabe. Lo que antes solo quedaba en el
    registro no se le dice, salvo que el agente haya visto un problema de verdad (`siempre`)."""
    for i in incs:
        if i.get("aviso"):
            avisar(i["mensaje"])
    if diagnostico and (siempre or any(i.get("aviso") for i in incs)):
        avisar("El reparador del diario no lo ha arreglado: " + diagnostico)


def una_reparacion(incs):
    fecha = max(i.get("fecha") or dia_del_numero() for i in incs)
    E = RAIZ / "estado" / fecha
    bloqueo = any(i.get("bloqueo") for i in incs)
    estado = lambda sufijo: pathlib.Path(f"{E}.{sufijo}").exists()   # noqa: E731
    hoy = fecha == dia_del_numero()
    fase = "bloqueo" if bloqueo else ("despues" if estado("publicado") or not hoy else "antes")
    minutos = MINUTOS
    if fase != "despues":
        minutos = min(MINUTOS, (LIMITE_BLOQUEO if bloqueo else LIMITE_ANTES) - minutos_del_dia())
        if minutos < MINIMO and os.environ.get("REPARADOR_SIN_HORARIO") != "1":
            if bloqueo:   # no da tiempo: el plan B de las 6:30 saca el número; la causa se mira después de publicar
                (ESTADO / "bloqueo").unlink(missing_ok=True)
            for i in incs:   # y lo que había que decirle no espera a la reparación
                if i.get("aviso"):
                    avisar(i["mensaje"])
                    i["aviso"] = False
            esperar(lambda: estado("publicado"), 9 * 60 + 10, cada=60)
            fase, minutos, bloqueo = "despues", MINUTOS, False
        elif os.environ.get("REPARADOR_SIN_HORARIO") == "1":
            minutos = MINUTOS
    ident = f"{ahora():%Y%m%d-%H%M%S}"
    copia = TRABAJO / ident / "copia"   # y, al lado, la carpeta personal del agente; al acabar se borra todo
    resultado = {"incidencias": [i["mensaje"][:300] for i in incs], "fecha": fecha, "fase": fase, "id": ident}
    try:
        copiar(copia)
        en_redaccion = archivos(copia)   # la redacción tal como se copió: para saber si allí cambia algo mientras tanto
        antes_textos = {}
        for carpeta in CARPETAS_DIA:
            d = leer(copia / carpeta / f"{fecha}.json")
            antes_textos[f"{carpeta}/{fecha}.json"] = sorted(firma_textos(d)) if d is not None else None
        antes_medidas = medir(copia, fecha)
        antes_archivos = archivos(copia)   # la copia ya medida: lo que cambie desde aquí lo ha cambiado el agente
        if fase != "despues" and os.environ.get("REPARADOR_SIN_HORARIO") != "1":   # copiar y medir ha llevado un rato
            limite = LIMITE_BLOQUEO if fase == "bloqueo" else LIMITE_ANTES
            minutos = max(5, min(minutos, limite - minutos_del_dia()))
        codigo, segundos, coste = lanzar_agente(copia, incs, fecha, fase, minutos, antes_medidas, ident)
        informe = leer(copia / INFORME) or {}
        resultado.update(segundos=segundos, coste_usd=coste, antes=antes_medidas,
                         informe={k: informe.get(k) for k in ("resultado", "que_fallaba", "que_he_hecho", "causa", "pendiente")})
        veredicto = informe.get("resultado")
        if codigo != 0 or not informe:
            motivo = "se le acabó el tiempo" if codigo == 124 else f"el agente no terminó (código {codigo})" if codigo else "el agente no dejó su informe"
            apuntar(**resultado, resultado="no_arreglado", motivo=motivo)
            reenviar(incs, motivo + ". Detalle: /volume1/docker/diario-ia-educativa/repo/registro/reparador-" + ident + ".log")
            return
        if veredicto == "nada_que_arreglar":
            apuntar(**resultado, resultado="nada_que_arreglar")
            reenviar(incs)
            return
        if veredicto != "arreglado":
            apuntar(**resultado, resultado="no_arreglado", motivo="el agente dice que no puede")
            reenviar(incs, " ".join(str(informe.get("que_fallaba") or "").split())[:800] + " "
                     + " ".join(str(informe.get("pendiente") or informe.get("que_he_hecho") or "").split())[:800], siempre=True)
            return
        cambiados, borrar, medidas, problemas = comprobar(copia, fecha, antes_archivos, antes_textos, antes_medidas, informe)
        resultado.update(despues=medidas, cambiados=cambiados, borrados=borrar)
        if not problemas and not cambiados and not borrar and not (informe.get("reintentar") or []):
            problemas.append("dice que lo ha arreglado pero no ha cambiado nada")
        if not problemas and fase == "antes" and (estado("publicando") or estado("publicado")):
            esperar(lambda: estado("publicado") and not estado("publicando"), minutos_del_dia() + 20)
            fase = resultado["fase"] = "despues"
        if not problemas:
            fallo = aplicar(copia, cambiados, borrar, en_redaccion)
            if fallo:
                problemas.append(fallo)
        if problemas:
            apuntar(**resultado, resultado="no_aplicado", motivo="; ".join(problemas))
            reenviar(incs, "lo intentó, pero la comprobación no lo da por bueno (" + "; ".join(problemas)[:600] + ") y no se ha aplicado nada.")
            return
        codigo_git = guardar_codigo(cambiados, informe)
        despues_txt = despues_de_aplicar(fecha, fase, informe, bool(cambiados or borrar))
        apuntar(**resultado, resultado="arreglado", codigo=codigo_git)
        partes = ["🔧 Diario: había un fallo y el reparador lo ha arreglado.",
                  "Qué fallaba: " + " ".join(str(informe.get("que_fallaba") or "").split())[:700],
                  "Qué ha hecho: " + " ".join(str(informe.get("que_he_hecho") or "").split())[:900]]
        if codigo_git:
            partes.append("Ha cambiado el programa (" + ", ".join(codigo_git)[:300] + ") y está guardado en el repositorio.")
        if informe.get("pendiente"):
            partes.append("Queda pendiente: " + " ".join(str(informe["pendiente"]).split())[:500])
        partes.append(despues_txt)
        avisar("\n".join(p for p in partes if p))
    except Exception as ex:   # noqa: BLE001 — pase lo que pase, el aviso original llega
        apuntar(**resultado, resultado="no_arreglado", motivo=f"el reparador falló: {ex!r}")
        reenviar(incs, f"el propio reparador falló ({ex!r}).")
    finally:
        shutil.rmtree(copia.parent, ignore_errors=True)
        if bloqueo:
            (ESTADO / "bloqueo").unlink(missing_ok=True)


def despues_de_aplicar(fecha, fase, informe, hay_cambios):
    """Lo que toca tras aplicar el arreglo, según el momento. Devuelve la frase que lo cuenta."""
    E = RAIZ / "estado" / fecha
    reintentar = [str(x) for x in informe.get("reintentar") or []]
    frases = []
    if fase == "bloqueo":   # la noche se repite sola: si ya gastó sus dos intentos, uno más, una vez
        f, marca = pathlib.Path(f"{E}.intentos"), pathlib.Path(f"{E}.reparador-reintento")
        try:
            n = int(f.read_text().strip())
        except (OSError, ValueError):
            n = 0
        if n >= 2 and not marca.exists():
            marca.touch()
            f.write_text("1\n")
        frases.append("La redacción vuelve a preparar el número ahora.")
    elif fase == "antes":
        if hay_cambios:
            c = correr([sys.executable, "generar.py"], RAIZ)[0]
            correr([sys.executable, "-m", "pagefind", "--site", "sitio"], RAIZ)
            frases.append("El número sale a su hora, a las 6:50; ya está así en la vista previa." if c == 0
                          else "OJO: al rehacer el sitio el generador ha fallado.")
    else:
        if hay_cambios or "web" in reintentar:
            if (E.parent / "multimedia.publicando").exists() or pathlib.Path(f"{E}.publicando").exists():
                frases.append("La web se volverá a publicar con el siguiente número: ahora mismo se estaba publicando otra cosa.")
            elif os.environ.get("REPARADOR_SIN_PUSH") == "1":
                frases.append("(prueba: la web no se vuelve a publicar)")
            else:
                c = correr(["bash", "scripts/publicar-web.sh"], RAIZ, tope=1200)[0]
                frases.append("La web se ha vuelto a publicar con el arreglo." if c == 0 else "OJO: no se ha podido volver a publicar la web.")
    # Lo que el agente pide repetir lo repite el reloj, no él: aquí solo se le quita la marca de «ya intentado»
    hoy = ahora().date().isoformat()
    marcas = {"instagram": (pathlib.Path(f"{E}.instagram-intento"), pathlib.Path(f"{E}.instagram")),
              "publicar": (pathlib.Path(f"{E}.publicar-fallo"), pathlib.Path(f"{E}.publicado")),
              "reserva": (E.parent / f"reserva-{hoy}", None)}
    for que in reintentar:
        if que in marcas:
            marca, hecho = marcas[que]
            if marca.exists() and not (hecho and hecho.exists()):
                marca.unlink()
                frases.append({"instagram": "El carrusel de Instagram se vuelve a intentar en unos minutos.",
                               "publicar": "La publicación se vuelve a intentar en unos minutos.",
                               "reserva": "La reserva se vuelve a reponer en unos minutos."}[que])
    return " ".join(frases)


def atender():
    if apagado() or not coger_turno():
        return 0
    try:
        while True:
            # Un defecto no se arregla mientras la noche aún escribe el número: se espera a que acabe y se
            # atienden juntos todos sus avisos. Si el número no ha llegado a prepararse (bloqueo), no se espera.
            en_marcha = RAIZ / "estado" / f"{dia_del_numero()}.en-marcha"
            if not (ESTADO / "bloqueo").exists():
                esperar(lambda f=en_marcha: not f.exists(), LIMITE_ANTES)
            time.sleep(ESPERA)
            incs = tomar_cola()
            if not incs:
                break
            una_reparacion(incs)
    finally:
        (ESTADO / "en-marcha").unlink(missing_ok=True)
    if any(COLA.glob("*.json")) and not apagado():   # llegó algo justo al acabar
        return atender()
    return 0


def estado():
    print("apagado" if apagado() else "encendido", "·", "trabajando" if (ESTADO / "en-marcha").exists() else "en reposo",
          "· en cola:", len(list(COLA.glob("*.json"))) if COLA.exists() else 0)
    if REGISTRO.exists():
        for linea in REGISTRO.read_text().splitlines()[-10:]:
            d = json.loads(linea)
            print(f"{d['hora']}  {d.get('resultado', '?'):18} {d.get('fase', ''):8} {d.get('segundos', '-')} s  "
                  f"{(d.get('motivo') or (d.get('informe') or {}).get('que_fallaba') or '')[:110]}")
    return 0


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "incidencia":
        sys.exit(incidencia(sys.argv[2:]))
    elif orden == "atender":
        sys.exit(atender())
    elif orden == "estado":
        sys.exit(estado())
    elif orden == "medir":
        print(json.dumps(medir(RAIZ, sys.argv[2], maqueta="--maqueta" in sys.argv), ensure_ascii=False, indent=1))
    else:
        print(__doc__)
        sys.exit(2)
