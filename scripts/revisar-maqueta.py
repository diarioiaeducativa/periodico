#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La revisión de la maqueta de cada madrugada (ADR 0041), sin IA: tras montar la vista previa de las 5:00, abre la
portada de cada idioma y la página del número con el Chromium de Playwright a nueve anchuras y pasa la misma
comprobación que `revisar-maqueta.js` (scripts/maqueta-pagina.js). Si algo falla, avisa a Juanjo por Telegram, con
la captura de cada bloque, antes de que el número salga a las 6:50, y lo deja en registro/<fecha>-maqueta.json
para el informe del día (ADR 0069).

    scripts/revisar-maqueta.py AAAA-MM-DD            (la fecha de las conversaciones, como noche.sh)
    scripts/revisar-maqueta.py AAAA-MM-DD --sin-aviso

Necesita el sitio ya montado (`generar.py`); lo sirve en un puerto local, como portadas.py.
"""
import datetime
import functools
import http.server
import json
import pathlib
import sys
import threading
import urllib.request
import uuid

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402

ANCHOS = (1366, 1100, 960, 900, 840, 800, 700, 640, 390)   # los de revisar-anchos.js
CONFIG = pathlib.Path.home() / ".config" / "avisar-juanjo" / "config.json"
VISTA = "http://192.168.1.113:8770/"
# Cada bloque, con el nombre que se ve en el diario, no con el del código
BLOQUES = (("semana-franja", "«La semana en vídeo»"), ("fila-breves-hu", "los breves y «Hace un año»"),
           ("fila-destacadas", "las destacadas"), ("mas-dia", "«Más del día»"), ("nb-grupos", "los grupos de la semana"),
           ("alt-", "una sección"), ("fila-seccion", "una sección"), ("sec-", "una sección"))
PAGINAS = {"es": "portada en castellano", "ca": "en catalán", "gl": "en gallego", "eu": "en euskera", "en": "en inglés",
           "es-número": "página del número"}


def legible(fallo):
    """«hueco de 278 px en editorial semana-franja (…)» → «un hueco de unos 280 px en «La semana en vídeo»»."""
    bloque = next((n for k, n in BLOQUES if k in fallo), "un bloque de la portada")
    px = "".join(ch for ch in fallo.split(" px")[0] if ch.isdigit())
    tipo = "un hueco" if fallo.startswith("hueco") else "una fila incompleta"
    return f"{tipo} de unos {round(int(px), -1) if px else '?'} px en {bloque}", bloque


class Callado(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def comprobacion():
    texto = (RAIZ / "scripts" / "maqueta-pagina.js").read_text()
    return "(" + "\n".join(x for x in texto.splitlines() if not x.startswith("//")).strip() + ")()"


def foto(ruta, pie):
    """Una captura a Juanjo, por el mismo bot que avisar-juanjo."""
    try:
        bot = json.loads(CONFIG.read_text())
        limite = "----" + uuid.uuid4().hex
        partes = []
        for k, v in (("chat_id", str(bot["chat_id"])), ("caption", pie[:1000])):
            partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="photo"; filename="{ruta.name}"\r\n'
                      f'Content-Type: image/png\r\n\r\n'.encode() + ruta.read_bytes() + b"\r\n")
        partes.append(f"--{limite}--\r\n".encode())
        req = urllib.request.Request(f"https://api.telegram.org/bot{bot['token']}/sendPhoto", data=b"".join(partes),
                                     headers={"Content-Type": f"multipart/form-data; boundary={limite}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return bool(json.load(r).get("ok"))
    except Exception as ex:   # noqa: BLE001  — sin la foto, queda el texto
        print("no se pudo mandar la captura:", ex)
        return False


def main():
    from playwright.sync_api import sync_playwright
    fecha = sys.argv[1]
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    paginas = [(c, d["carpeta"]) for c, d in generar.IDIOMAS.items()] + [("es-número", f"{fecha}/")]
    carpeta = RAIZ / "registro" / f"{fecha}-maqueta"
    carpeta.mkdir(parents=True, exist_ok=True)
    # Las capturas de más de un mes, fuera
    import shutil
    for vieja in (RAIZ / "registro").glob("*-maqueta"):
        if vieja.is_dir() and vieja.name[:10] < (datetime.date.fromisoformat(fecha) - datetime.timedelta(days=30)).isoformat():
            shutil.rmtree(vieja, ignore_errors=True)
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Callado, directory=str(generar.SITIO)))
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_address[1]}/"
    js = comprobacion()
    fallos = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(viewport={"width": 1366, "height": 900}, color_scheme="light", service_workers="block")
        pag = ctx.new_page()
        for nombre, ruta in paginas:
            if not (generar.SITIO / ruta / "index.html").exists():
                continue
            pag.set_viewport_size({"width": 1366, "height": 900})
            pag.goto(base + ruta + "?nocontar=1", wait_until="load")
            pag.wait_for_timeout(1500)
            for ancho in ANCHOS:
                pag.set_viewport_size({"width": ancho, "height": 900})
                pag.wait_for_timeout(900)   # que la página iguale las filas
                r = [x for x in pag.evaluate(js) if x.startswith(("hueco", "fila incompleta"))]
                if not r:
                    continue
                cap = carpeta / f"{nombre}-{ancho}.png"
                el = pag.query_selector("[data-maqueta-fallo]")
                try:
                    (el.screenshot if el else pag.screenshot)(path=str(cap))
                except Exception:   # noqa: BLE001
                    cap = None
                fallos.append({"pagina": nombre, "ruta": ruta, "ancho": ancho, "fallos": r, "bloques": [legible(x)[1] for x in r],
                               "captura": str(cap) if cap else ""})
        nav.close()
    servidor.shutdown()
    (RAIZ / "registro" / f"{fecha}-maqueta.json").write_text(json.dumps(fallos, ensure_ascii=False, indent=1))
    if not fallos:
        print("maqueta: sin huecos")
        return
    print("maqueta:", json.dumps(fallos, ensure_ascii=False))
    if "--sin-aviso" in sys.argv:
        return
    # Un aviso por bloque distinto: el mismo hueco en varios idiomas o a varias anchuras es uno, con la captura del
    # primero que se encontró
    vistos = {}
    for f in fallos:
        for x in f["fallos"]:
            v = vistos.setdefault(legible(x)[1], {"f": f, "x": legible(x)[0], "paginas": [], "anchos": []})
            v["paginas"] += [PAGINAS.get(f["pagina"], f["pagina"])] if PAGINAS.get(f["pagina"], f["pagina"]) not in v["paginas"] else []
            v["anchos"] += [f["ancho"]] if f["ancho"] not in v["anchos"] else []
    for v in list(vistos.values())[:4]:
        f = v["f"]
        pie = (f"Maqueta del número del {publica[8:10]}-{publica[5:7]}: queda {v['x']} ({', '.join(v['paginas'])}; "
               f"con la pantalla a {', '.join(map(str, sorted(v['anchos'], reverse=True)))} px de ancho). "
               f"Sale igual a las 6:50; vista previa: {VISTA}{f['ruta']}")
        if not (f["captura"] and foto(pathlib.Path(f["captura"]), pie)):
            import subprocess
            subprocess.run(["avisar-juanjo", "--de", "Diario de IA Educativa", pie], check=False)


if __name__ == "__main__":
    main()
