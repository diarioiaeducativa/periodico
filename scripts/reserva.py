#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las piezas de reserva: el plan B para que no haya ningún día sin número (ADR 0021).

    scripts/reserva.py cuantas             cuántas piezas de reserva hay listas
    scripts/reserva.py faltan              cuántas faltan para tener OBJETIVO listas
    scripts/reserva.py clave               una clave libre para escribir la siguiente
    scripts/reserva.py siguiente           de qué fuente escribir la siguiente: repositorio o biblioteca
    scripts/reserva.py guardar CLAVE [repositorio|biblioteca]
                                           pasa a reserva/CLAVE/ lo que repositorio.sh o biblioteca.sh escribió con esa clave
    scripts/reserva.py caducar             retira las que pasan de CADUCA días (se escribirán otras)
    scripts/reserva.py usar AAAA-MM-DD [fallo|relleno]
                                           pone una pieza de reserva en el número de esas conversaciones

Una pieza de reserva es un artículo del fondo del Repositorio de VCE («Del fondo del repositorio») o,
desde el 08-11-2026, del fondo de la Biblioteca digital («Del fondo de la biblioteca»), que se
alternan para que el día que se use no toque siempre una aplicación.
Puede caducar (el recurso cambia de dirección, desaparece o pasa a ser de pago): a los CADUCA días
sin usarse se retira y se escribe otra, y antes de usarla se comprueba que el recurso sigue
respondiendo (ADR 0028). La escribe repositorio.sh, con su documentalista, su revisor y su traductor, con una
clave de fecha provisional (2099-01-NN) que no choca con ningún número; aquí se guarda en
reserva/CLAVE/ con su captura. Usarla no necesita IA: se cambia la clave por la fecha del día en
el JSON y en el nombre de la captura, se pasa a repositorio/ y se marca la edición con
"reserva": "fallo" o "relleno". Con «fallo» (la redacción no pudo preparar el número) la web lo
dice y la noche siguiente recupera las conversaciones de ese día (noche.sh); con «relleno» (no
había nada que contar y tampoco salió nada del repositorio) no hay nada que recuperar. Si el día
ya tiene piezas (la redacción terminó pero se atascó después), no se añade nada. En los dos casos,
si faltan los avisos de los grupos, se escriben aquí, sin IA.

«usar» sale con 0 si ha puesto la reserva, con 4 si el día ya tenía piezas (no hace falta) y con 3
si no queda ninguna.
"""
import datetime
import json
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESERVA = RAIZ / "reserva"
OBJETIVO = 3          # piezas de reserva que tiene que haber siempre listas
CADUCA = 60           # días sin usarse: se retira y se escribe otra (Juanjo, 06-11-2026)
TRADUCCIONES = ("ca", "gl", "eu", "en")   # los idiomas a los que se traduce (scripts/idiomas.py, ADR 0026)
PREFIJO = "2099-01-"  # las claves provisionales: una fecha que nunca será un número
TIPOS = ("repositorio", "biblioteca")   # las dos fuentes de la reserva


def tipo(d):
    """repositorio o biblioteca, según lo que guarde la reserva."""
    return "biblioteca" if (d / "biblioteca.json").exists() else "repositorio"


def principal(d):
    return d / f"{tipo(d)}.json"


def escrita(d):
    """La fecha en que se escribió (escrita.txt; si falta, la del archivo)."""
    try:
        return datetime.date.fromisoformat((d / "escrita.txt").read_text().strip())
    except (OSError, ValueError):
        return datetime.date.fromtimestamp(principal(d).stat().st_mtime)


def listas():
    """Las reservas vigentes con alguna pieza, la más antigua primero."""
    out = []
    hoy = datetime.date.today()
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        f = principal(d)
        try:
            if json.loads(f.read_text()).get("piezas") and (hoy - escrita(d)).days <= CADUCA:
                out.append(d)
        except (OSError, ValueError):
            pass
    return out


def retirar(d, motivo):
    viejo = RESERVA / "retiradas" / d.name
    viejo.parent.mkdir(exist_ok=True)
    shutil.rmtree(viejo, ignore_errors=True)
    shutil.move(str(d), viejo)
    (viejo / "motivo.txt").write_text(f"{datetime.date.today().isoformat()}: {motivo}\n")
    print(f"reserva: {d.name} retirada ({motivo})")


def caducar():
    hoy = datetime.date.today()
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        if principal(d).exists() and (hoy - escrita(d)).days > CADUCA:
            retirar(d, f"escrita el {escrita(d)}, pasa de {CADUCA} días")


def vigente(d):
    """Que cada recurso, o el documento, siga respondiendo en su dirección (sin IA, para que el plan B
    sea rápido)."""
    import reserva_reportaje   # noqa: E402 — la misma comprobación de enlaces
    for p in json.loads(principal(d).read_text()).get("piezas", []):
        urls = [r.get("url") for r in p.get("recursos", [])] + [(p.get("documento") or {}).get("url")]
        for u in urls:
            if u and not reserva_reportaje.responde(u):
                return False, f"{u} no responde"
    return True, ""


def siguiente():
    """La fuente de la siguiente pieza: la que tenga menos en la reserva; a la par, la biblioteca."""
    n = {t: 0 for t in TIPOS}
    for d in listas():
        n[tipo(d)] += 1
    return "repositorio" if n["repositorio"] < n["biblioteca"] else "biblioteca"


def mover_dibujos(origen_clave, destino_clave, de, a):
    """Los dibujos de las piezas (ilustraciones/ y sus traducciones) de la carpeta de la reserva a la
    redacción o al revés, cambiando la clave del nombre."""
    for carpeta in [RAIZ / "ilustraciones"] + [RAIZ / f"ilustraciones-{c}" for c in TRADUCCIONES]:
        sub = carpeta.name
        desde = (de / sub) if de else carpeta
        for f in desde.glob(f"{origen_clave}-*.svg"):
            hasta = (a / sub) if a else carpeta
            hasta.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), hasta / f.name.replace(origen_clave, destino_clave))


def clave_libre():
    usadas = {d.name for d in RESERVA.glob(PREFIJO + "*")} | \
             {f.stem for c in ("repositorio", "repositorio-borrador", "biblioteca", "biblioteca-borrador")
              for f in (RAIZ / c).glob(PREFIJO + "*.json")}
    for n in range(1, 32):
        k = f"{PREFIJO}{n:02d}"
        if k not in usadas:
            return k
    raise SystemExit("reserva: no quedan claves libres")


def guardar(clave, fuente="repositorio"):
    """De repositorio/ (o biblioteca/) a reserva/CLAVE/. Lo que el documentalista descartó se guarda
    igual, para que repositorio.py o biblioteca.py no vuelvan a proponerlo (cuentan reserva/ como ya
    contado)."""
    dest = RESERVA / clave
    dest.mkdir(parents=True, exist_ok=True)
    if fuente == "biblioteca":
        for origen, nombre in [("biblioteca", "biblioteca.json")] + [(f"biblioteca-{c}", f"biblioteca-{c}.json") for c in TRADUCCIONES]:
            f = RAIZ / origen / f"{clave}.json"
            if f.exists():
                shutil.move(str(f), dest / nombre)
        # Si el revisor no dio nada por bueno, biblioteca.sh borra el archivo: los candidatos se apuntan
        # igual como descartados, desde el borrador, para que biblioteca.py no los vuelva a proponer
        borrador = RAIZ / "biblioteca-borrador" / f"{clave}.json"
        if not (dest / "biblioteca.json").exists() and borrador.exists():
            try:
                b = json.loads(borrador.read_text())
            except ValueError:
                b = {}
            descartes = list(b.get("descartado", [])) + [
                f"mensaje {(p.get('mensaje') or {}).get('id')}: el revisor no lo dio por bueno"
                for p in b.get("piezas", [])]
            (dest / "biblioteca.json").write_text(json.dumps({"fecha": clave, "piezas": [], "descartado": descartes},
                                                             ensure_ascii=False, indent=1) + "\n")
        mover_dibujos(clave, clave, None, dest)
        (dest / "escrita.txt").write_text(datetime.date.today().isoformat() + "\n")
        for c in ("biblioteca-borrador", "biblioteca-entrada"):
            for f in (RAIZ / c).glob(f"{clave}*"):
                f.unlink()
        ok = (dest / "biblioteca.json").exists() and json.loads((dest / "biblioteca.json").read_text()).get("piezas")
        print(f"reserva: {clave} {'guardada (biblioteca)' if ok else 'sin pieza (solo descartes)'}; listas: {len(listas())}")
        return 0 if ok else 2
    for origen, nombre in [("repositorio", "repositorio.json")] + [(f"repositorio-{c}", f"repositorio-{c}.json") for c in TRADUCCIONES]:
        f = RAIZ / origen / f"{clave}.json"
        if f.exists():
            shutil.move(str(f), dest / nombre)
    (dest / "escrita.txt").write_text(datetime.date.today().isoformat() + "\n")
    for f in (RAIZ / "repositorio" / "capturas").glob(f"{clave}-*.jpg"):
        (dest / "capturas").mkdir(exist_ok=True)
        shutil.move(str(f), dest / "capturas" / f.name)
    for c in ("repositorio-borrador", "repositorio-entrada"):
        for f in (RAIZ / c).glob(f"{clave}.*"):
            f.unlink()
    ok = (dest / "repositorio.json").exists() and json.loads((dest / "repositorio.json").read_text()).get("piezas")
    print(f"reserva: {clave} {'guardada (repositorio)' if ok else 'sin pieza (solo descartes)'}; listas: {len(listas())}")
    return 0 if ok else 2


def piezas_del_dia(fecha):
    n = 0
    f = RAIZ / "ediciones" / f"{fecha}.json"
    if f.exists():
        d = json.loads(f.read_text())
        n += len(d.get("piezas", [])) if d.get("hay_edicion") else 0
    for c in ("biblioteca", "repositorio"):
        g = RAIZ / c / f"{fecha}.json"
        if g.exists():
            n += len(json.loads(g.read_text()).get("piezas", []))
    return n


def titulares(fecha):
    out = []
    for c in ("ediciones", "biblioteca", "repositorio"):
        g = RAIZ / c / f"{fecha}.json"
        if g.exists():
            d = json.loads(g.read_text())
            if c != "ediciones" or d.get("hay_edicion"):
                out += [p.get("titular", "").rstrip(".") for p in d.get("piezas", []) if p.get("titular")]
    return out


def avisos(fecha, fallo):
    """Los avisos de los grupos sin IA, si el agente no los escribió: los titulares del número y, si
    la redacción falló, que las noticias de ayer salen mañana. El bot les pone la cabecera, el
    enlace y la imagen del número."""
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    f = RAIZ / "avisos" / f"{publica}.json"
    try:
        if json.loads(f.read_text()).get("avisos"):
            return
    except (OSError, ValueError):
        pass
    puntos = titulares(fecha)[:3 if not fallo else 2]
    if fallo:
        puntos.append("Las noticias de los grupos de ayer no han podido salir hoy por un fallo de la redacción del diario: salen mañana, junto con las de hoy")
    if len(puntos) < 2:
        puntos.append("Todas las piezas, con sus fuentes, en el diario")
    f.parent.mkdir(exist_ok=True)
    f.write_text(json.dumps({"fecha": publica, "avisos": {g: {"saludo": "Buenos días.", "puntos": puntos}
                                                           for g in ("chatgpt", "vce", "edumedia")}},
                            ensure_ascii=False, indent=2) + "\n")


def usar(fecha, motivo="fallo"):
    if piezas_del_dia(fecha):
        avisos(fecha, False)
        print(f"reserva: el número del {fecha} ya tiene piezas; no hace falta la reserva")
        return 4
    caducar()
    r = None
    for d in listas():
        ok, motivo = vigente(d)
        if ok:
            r = d
            break
        retirar(d, motivo)
    if r is None:
        print("reserva: no queda ninguna pieza de reserva", file=sys.stderr)
        return 3
    clave = r.name
    t = tipo(r)
    nuevas = []
    for nombre, destino in [(f"{t}.json", t)] + [(f"{t}-{c}.json", f"{t}-{c}") for c in TRADUCCIONES]:
        f = r / nombre
        if not f.exists():
            continue
        d = json.loads(f.read_text().replace(clave, fecha))   # la fecha y el nombre de la captura
        d["fecha"] = fecha
        g = RAIZ / destino / f"{fecha}.json"
        if g.exists():   # el día ya tenía un archivo (solo descartes): se le añaden las piezas
            viejo = json.loads(g.read_text())
            viejo["piezas"] = viejo.get("piezas", []) + d.get("piezas", [])
            d = viejo
        g.parent.mkdir(exist_ok=True)
        g.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        if destino == t:
            nuevas = d.get("piezas", [])
    for f in (r / "capturas").glob("*.jpg"):
        (RAIZ / "repositorio" / "capturas").mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), RAIZ / "repositorio" / "capturas" / f.name.replace(clave, fecha))
    mover_dibujos(clave, fecha, r, None)
    ed = RAIZ / "ediciones" / f"{fecha}.json"
    d = json.loads(ed.read_text()) if ed.exists() else {"fecha": fecha, "hay_edicion": False, "piezas": [], "breves": []}
    d["reserva"] = motivo
    d["motivo"] = (d.get("motivo") + " · " if d.get("motivo") else "") + f"número con la pieza de reserva {clave} ({motivo})"
    ed.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    avisos(fecha, motivo == "fallo")
    shutil.rmtree(r)
    print(f"reserva: el número del {fecha} sale con la reserva {clave}, de {t} ({', '.join(p['id'] for p in nuevas)}); quedan {len(listas())}")
    return 0


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "cuantas":
        print(len(listas()))
    elif orden == "caducar":
        caducar()
    elif orden == "faltan":
        print(max(0, OBJETIVO - len(listas())))
    elif orden == "clave":
        print(clave_libre())
    elif orden == "siguiente":
        print(siguiente())
    elif orden == "guardar" and len(sys.argv) in (3, 4) and (sys.argv[3:] or ["repositorio"])[0] in TIPOS:
        sys.exit(guardar(sys.argv[2], (sys.argv[3:] or ["repositorio"])[0]))
    elif orden == "usar" and len(sys.argv) in (3, 4) and (sys.argv[3:] or ["fallo"])[0] in ("fallo", "relleno"):
        codigo = usar(sys.argv[2], (sys.argv[3:] or ["fallo"])[0])
        # El sábado, el número del domingo lleva siempre reportaje: si la noche no llegó a hacerlo,
        # el de reserva (ADR 0028). No cambia lo que se responde sobre las piezas.
        if datetime.date.fromisoformat(sys.argv[2]).weekday() == 5:
            import reserva_reportaje   # noqa: E402
            reserva_reportaje.usar(sys.argv[2])
        sys.exit(codigo)
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
