#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prepara la entrada del documentalista para los recursos del Repositorio de VCE (ADR 0008).

    repositorio.py <carpeta de datos del bot> <carpeta de salida> <AAAA-MM-DD> [url ...]

El Repositorio de recursos de Vibe Coding Educativo es una hoja de cálculo publicada en CSV, la
misma que lee su web. Cada recurso que entra desde DESDE va a una cola; sale de ella cuando el
diario ya lo ha contado (en una pieza del redactor o en un artículo del repositorio) o cuando se
descarta. Cada noche decide qué toca, sin IA:

- viernes (el número del sábado): todo lo que queda en la cola, en una sola pieza («semana»);
- otro día con menos de UMBRAL piezas (las del redactor y las de la Biblioteca): hasta MAX_DIA
  recursos de la cola, el más antiguo primero y nunca dos de la misma persona («dia»);
- un día flojo con la cola vacía: tres candidatos del fondo del repositorio, para que el
  documentalista elija uno («fondo»).

De cada recurso abre la página en un Chromium sin pantalla, guarda una captura en
repositorio/capturas/ y el texto que se ve. Escribe <salida>/<fecha>.md (para el agente) y
<salida>/<fecha>.json. Con urls, prepara esos recursos sin mirar la cola. La variable
REPOSITORIO_MODO (dia, semana o fondo) fuerza el modo, para probar.
Sale con 0 si hay algo que escribir y con 3 si no.
"""
import csv
import datetime
import io
import json
import os
import pathlib
import random
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CSV = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_hltRI4Q0QolINWJVcKxCMMjfpdiCkKzSdgp9d8RlGTdU"
       "U1UIKvaj-TBSkq0JQGneDhfUkSQuFzy/pub?output=csv")
WEB = "https://vibe-coding-educativo.github.io/app_edu/"
DESDE = "2026-10-27"      # el día que el bot empezó a dar las altas: lo anterior es el fondo
UMBRAL = 4                # un número con menos piezas que estas es un día flojo (3 hasta el 04-11-2026)
MAX_DIA = 2               # recursos de la cola que se cuentan como mucho en un día flojo
CANDIDATOS_FONDO = 3
VIERNES = 5
# Lo que no se puede ver sin cuenta ni es una web: no va al fondo
NO_FONDO = ("chatgpt.com/g/", "chat.openai.com/g/", "gemini.google.com", "claude.ai", "g.co/gemini")
COLUMNAS = {"alta": "marca temporal", "autor": "tu nombre", "titulo": "título de la aplicación",
            "url": "enlace (url)", "descripcion": "descripción breve", "plataforma": "plataforma de creación",
            "tipo": "tipo de recurso", "niveles": "nivel o niveles", "areas": "área o áreas",
            "claves": "palabras clave", "licencia": "licencia de uso", "idiomas": "idiomas de la aplicación"}
ANCHO, ALTO = 1280, 800   # la captura, a la medida de una pantalla de portátil


def norm(u):
    """La misma dirección escrita de formas distintas cuenta como una sola."""
    u = (u or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"[?#].*$", "", u)
    return re.sub(r"/(index\.html?)?$", "", u)


def enlace_ficha(url):
    """La vista de solo esa ficha en la web del repositorio, como la enlaza el bot (catalogo.enlace_catalogo)."""
    if not url.strip() or "," in url:
        return WEB
    return WEB + "?ids=" + urllib.parse.quote(url.strip(), safe=":/")


def fecha_alta(texto):
    """«3/11/2026 14:10:23» → «2026-11-03»."""
    m = re.match(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})", texto or "")
    return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else ""


def destino(url):
    """Adónde lleva de verdad un enlace: algunas fichas usan un acortador (ja.cat) y el diario
    enlaza la dirección final. Si no responde, la misma."""
    try:
        pet = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (diario-ia-educativa)"})
        with urllib.request.urlopen(pet, timeout=15) as r:
            return r.geturl()
    except Exception:
        return url


def ya_contado(r, hechos):
    if norm(r["url"]) in hechos:
        return True
    r.setdefault("destino", destino(r["url"]))
    return norm(r["destino"]) in hechos


def hoja():
    with urllib.request.urlopen(urllib.request.Request(CSV, headers={"User-Agent": "diario-ia-educativa"}), timeout=60) as r:
        filas = list(csv.DictReader(io.StringIO(r.read().decode("utf-8"))))
    if not filas:
        return []
    cab = {k: next((c for c in filas[0] if c.strip().lower().startswith(v)), None) for k, v in COLUMNAS.items()}
    recursos = {}
    for f in filas:   # como la web: si un enlace se repite, vale la última fila
        r = {k: (f.get(c) or "").strip() if c else "" for k, c in cab.items()}
        if not r["url"] or not r["titulo"]:
            continue
        r["alta"] = fecha_alta(r["alta"])
        recursos[norm(r["url"])] = r
    return list(recursos.values())


def contados():
    """Lo que el diario ya ha contado o ha descartado, por dirección normalizada."""
    hechos = set()
    for f in sorted((RAIZ / "ediciones").glob("*.json")):
        d = json.loads(f.read_text())
        textos = [json.dumps(p, ensure_ascii=False) for p in d.get("piezas", [])] + \
                 [json.dumps(b, ensure_ascii=False) for b in d.get("breves", [])]
        for t in textos:
            hechos.update(norm(u) for u in re.findall(r"https?://[^\s\"')\]]+", t))
    for f in sorted((RAIZ / "repositorio").glob("*.json")):
        d = json.loads(f.read_text())
        for p in d.get("piezas", []):
            hechos.update(norm(x.get("url")) for x in p.get("recursos", []))
        for x in d.get("descartado", []):
            if isinstance(x, dict) and x.get("url"):
                hechos.add(norm(x["url"]))
    hechos.discard("")
    return hechos


def turnos():
    """Por autor, la fecha de su último recurso con artículo: quien lleva más tiempo sin salir va
    antes, para que nadie acapare el espacio (Juanjo, 04-11-2026: tratado como cualquiera)."""
    ultimo = {}
    for f in sorted((RAIZ / "repositorio").glob("*.json")):
        d = json.loads(f.read_text())
        fecha = d.get("fecha") or f.stem
        for p in d.get("piezas", []):
            for x in p.get("recursos", []):
                a = (x.get("autoria") or "").strip().lower()
                if a:
                    ultimo[a] = max(ultimo.get(a, ""), fecha)
    return ultimo


def piezas_del_dia(fecha):
    n = 0
    f = RAIZ / "ediciones" / f"{fecha}.json"
    if f.exists():
        d = json.loads(f.read_text())
        n += len(d.get("piezas", [])) if d.get("hay_edicion") else 0
    b = RAIZ / "biblioteca" / f"{fecha}.json"
    if b.exists():
        n += len(json.loads(b.read_text()).get("piezas", []))
    return n


def con_aviso(base):
    """Los recursos con un aviso pendiente de la revisión del repositorio (bot, ADR 0013): no van al fondo."""
    try:
        avisos = json.loads((base / "avisos.json").read_text())
    except (OSError, ValueError):
        return set()
    pendientes = {u: a for u, a in avisos.items() if (a or {}).get("estado") != "resuelto"}
    # Por enlace y por título: si el autor cambió el enlace sin dar el aviso por resuelto, sigue pendiente
    return {norm(u) for u in pendientes} | {"titulo:" + (a.get("titulo") or "").strip().lower() for a in pendientes.values()}


def ficha_corta(titulo):
    s = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode().lower()
    return "-".join(re.findall(r"[a-z0-9]+", s))[:40].strip("-") or "recurso"


def capturar(recursos, fecha):
    """Abre cada recurso como lo vería quien llega desde el diario y guarda captura y texto visible."""
    # La captura espera a que carguen todas las tipografías; si una no llega nunca (FoQo, 03-11-2026),
    # se queda colgada. Con esto no espera: sale con la letra de repuesto.
    os.environ.setdefault("PW_TEST_SCREENSHOT_NO_FONTS_READY", "1")
    from playwright.sync_api import sync_playwright
    carpeta = RAIZ / "repositorio" / "capturas"
    carpeta.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(viewport={"width": ANCHO, "height": ALTO}, color_scheme="light", locale="es-ES")
        try:
            for r in recursos:
                r["captura"] = f"{fecha}-{r['id']}.jpg"
                pag = ctx.new_page()
                try:
                    resp = pag.goto(r["url"], wait_until="domcontentloaded", timeout=30000)
                    try:   # hay páginas con algún recurso que no acaba de cargar nunca: se espera un rato, no más
                        pag.wait_for_load_state("load", timeout=12000)
                    except Exception:
                        pass
                    pag.wait_for_timeout(2500)   # lo que se dibuja después de cargar
                    r["estado_http"] = resp.status if resp else None
                    r["direccion_final"] = pag.url
                    r["titulo_pagina"] = pag.title()
                    r["texto_visible"] = re.sub(r"\n{3,}", "\n\n", pag.inner_text("body"))[:6000]
                    r["pide_contrasena"] = pag.locator("input[type=password]").count() > 0
                    r["enlaces"] = pag.eval_on_selector_all(
                        "a[href]", "as => [...new Set(as.map(a => a.href).filter(h => /github|gitlab|licen|creativecommons|LICENSE/i.test(h)))].slice(0, 15)")
                    pag.screenshot(path=str(carpeta / r["captura"]), type="jpeg", quality=72)
                    r["abre"] = bool(resp and resp.status < 400)
                except Exception as ex:   # no abre, tarda demasiado o el navegador falla en esa página
                    r["abre"], r["error"] = False, str(ex).splitlines()[0][:200]
                    (carpeta / r["captura"]).unlink(missing_ok=True)
                    r["captura"] = ""
                finally:
                    pag.close()
        finally:
            nav.close()
    return recursos


def preparar(r, usados):
    base = ficha_corta(r["titulo"])
    rid, n = base, 2
    while rid in usados:
        rid, n = f"{base}-{n}", n + 1
    usados.add(rid)
    es_codigo = bool(re.match(r"https?://(www\.)?(github|gitlab)\.com/", r["url"], re.I))
    return dict(r, id=rid, ficha=enlace_ficha(r["url"]), es_codigo=es_codigo)


def elegir(fecha, base, pedidos):
    todos = hoja()
    hechos = contados()
    if pedidos:
        p = {norm(u) for u in pedidos}
        return "dia", [r for r in todos if norm(r["url"]) in p]
    cola = sorted((r for r in todos if r["alta"] and DESDE <= r["alta"] <= fecha and not ya_contado(r, hechos)),
                  key=lambda r: r["alta"])
    flojo = piezas_del_dia(fecha) < UMBRAL
    modo = os.environ.get("REPOSITORIO_MODO") or (
        "semana" if datetime.date.fromisoformat(fecha).isoweekday() == VIERNES and cola else
        "dia" if flojo and cola else "fondo" if flojo else "")
    print(f"repositorio: {len(cola)} en la cola, {piezas_del_dia(fecha)} pieza(s) en el número, modo {modo or 'ninguno'}")
    if modo == "semana":
        return modo, cola
    if modo == "dia":
        hueco = max(1, min(MAX_DIA, UMBRAL - piezas_del_dia(fecha)))
        elegidos, autores = [], set()
        turno = turnos()   # por turnos de autor y, dentro, por antigüedad
        for r in sorted(cola, key=lambda r: (turno.get(r["autor"].strip().lower(), ""), r["alta"])):
            if r["autor"].lower() not in autores:
                elegidos.append(r)
                autores.add(r["autor"].lower())
            if len(elegidos) == hueco:
                break
        return modo, elegidos
    if modo == "fondo":
        avisos = con_aviso(base)
        fondo = [r for r in todos if r["alta"] and r["alta"] < DESDE and norm(r["url"]) not in hechos
                 and norm(r["url"]) not in avisos and "titulo:" + r["titulo"].strip().lower() not in avisos and r["licencia"] and not any(x in r["url"].lower() for x in NO_FONDO)]
        random.Random(fecha).shuffle(fondo)   # el mismo día da siempre los mismos candidatos
        turno = turnos()   # y, entre ellos, primero los autores que llevan más tiempo sin salir
        fondo.sort(key=lambda r: turno.get(r["autor"].strip().lower(), ""))
        # La dirección final cuenta también: hay fichas con acortador (ja.cat) y avisos guardados con la final
        buenos = [r for r in fondo[:CANDIDATOS_FONDO * 4] if not ya_contado(r, hechos) and norm(r["destino"]) not in avisos]
        return modo, buenos[:CANDIDATOS_FONDO * 2]   # el doble, por si alguno no abre
    return "", []


def main():
    base, out, fecha = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    modo, elegidos = elegir(fecha, base, sys.argv[4:])
    if not elegidos:
        sys.exit(3)
    usados = set()
    recursos = capturar([preparar(r, usados) for r in elegidos], fecha)
    abren = [r for r in recursos if r["abre"]]
    no_abren = [r for r in recursos if not r["abre"]]
    for r in no_abren:
        print(f"repositorio: no abre {r['url']} ({r.get('error') or r.get('estado_http')})")
    if modo == "fondo":
        abren = abren[:CANDIDATOS_FONDO]
    # El sábado, lo que sigue sin abrir sale de la cola: se descarta con su motivo
    descartes = [{"url": r["url"], "motivo": f"no abre: {r.get('error') or r.get('estado_http')}"} for r in no_abren] if modo == "semana" else []
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{fecha}.json").write_text(json.dumps({"fecha": fecha, "modo": modo, "recursos": abren, "descartes": descartes},
                                                  ensure_ascii=False, indent=1))
    if not abren:
        print("repositorio: ninguno de los elegidos abre")
        sys.exit(3)
    rotulo = {"dia": "Nuevo en el repositorio", "semana": "La semana del repositorio", "fondo": "Del fondo del repositorio"}[modo]
    que = {"dia": f"{len(abren)} recurso(s) de la cola: un artículo por cada uno.",
           "semana": f"los {len(abren)} recursos que quedan en la cola: una sola pieza con todos." if len(abren) > 1 else
                     "el único recurso que queda en la cola: un artículo, como un día flojo.",
           "fondo": f"{len(abren)} candidatos del fondo del repositorio: elige uno y escribe su artículo."}[modo]
    partes = [f"# Repositorio de recursos de Vibe Coding Educativo · para el número con fecha {fecha}\n",
              f"- Modo: **{modo if not (modo == 'semana' and len(abren) == 1) else 'dia'}** — {que}",
              f"- Antetítulo de la pieza: «{rotulo}»",
              f"- Web del repositorio: {WEB}\n"]
    for r in abren:
        partes.append(f"\n## Recurso «{r['titulo']}» (id `{r['id']}`)\n")
        for etiqueta, clave in (("Autoría (tal como figura en la ficha)", "autor"), ("Enlace", "url"), ("Ficha en el repositorio", "ficha"),
                                ("Entró en el repositorio", "alta"), ("Licencia declarada", "licencia"), ("Tipo", "tipo"),
                                ("Niveles", "niveles"), ("Áreas", "areas"), ("Idiomas", "idiomas"), ("Plataforma de creación", "plataforma"),
                                ("Palabras clave", "claves")):
            if r.get(clave):
                partes.append(f"- {etiqueta}: {r[clave]}")
        partes.append(f"- Captura de la página al abrirla (mírala con Read): repositorio/capturas/{r['captura']} "
                      f"(en el campo `captura`, solo el nombre: «{r['captura']}»)")
        if r["es_codigo"]:
            partes.append("- El enlace es un repositorio de código, no la web que usará el lector: la captura muestra GitHub. "
                          "Busca si tiene una web pública (GitHub Pages) y, si no, di que se descarga desde su repositorio. "
                          "Deja `captura` vacío.")
        if r.get("pide_contrasena"):
            partes.append("- La página pide una contraseña: comprueba si se puede usar sin cuenta.")
        if r.get("enlaces"):
            partes.append("- Enlaces de la página a código o licencia: " + ", ".join(r["enlaces"]))
        partes.append(f"\n### Descripción de la ficha\n\n{r['descripcion']}\n")
        partes.append(f"### Texto que se ve al abrir la página (título: «{r.get('titulo_pagina', '')}»)\n\n{r.get('texto_visible', '')}\n")
    (out / f"{fecha}.md").write_text("\n".join(partes) + "\n")
    print(f"repositorio: {len(abren)} recurso(s) para el {fecha}, modo {modo} ({', '.join(r['id'] for r in abren)})")


if __name__ == "__main__":
    main()
