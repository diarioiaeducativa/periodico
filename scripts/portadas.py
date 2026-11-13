#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La portada de cada número para la hemeroteca (ADR 0053): la página del día, de la cabecera a la viñeta
incluida, tal como se ve en un ordenador, reducida a miniatura.

    scripts/portadas.py [AAAA-MM-DD ...]   (fechas de las conversaciones; sin fechas, las que falten)

Necesita el sitio ya montado (`generar.py`): lo sirve en un puerto local, lo abre con el Chromium de
Playwright como un ordenador de 1280 px de ancho, en tema claro, y la guarda ya reducida (el navegador la
dibuja a escala ANCHO/1280) en portadas/<fecha>-<idioma>.jpg, con sus medidas en portadas/medidas.json para
que la página le reserve el sitio. generar.py las copia a sitio/portadas/ y las pone en el calendario de la
hemeroteca. Sin IA ni Pillow (el contenedor no lo tiene). Si falla, la hemeroteca sale sin miniatura.
"""
import functools
import json
import http.server
import pathlib
import sys
import threading

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402

SALIDA = RAIZ / "portadas"
ANCHO = 720        # a la derecha de la hemeroteca se ve a unos 700 px; en pequeño, nítida en alta densidad
CALIDAD = 55


class Callado(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    from playwright.sync_api import sync_playwright
    SALIDA.mkdir(exist_ok=True)
    pedidas = set(sys.argv[1:])
    f_medidas = SALIDA / "medidas.json"
    try:
        medidas = json.loads(f_medidas.read_text())
    except (OSError, ValueError):
        medidas = {}
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Callado, directory=str(generar.SITIO)))
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_address[1]}/"
    hechas = 0
    try:
        with sync_playwright() as pw:
            nav = pw.chromium.launch()
            # Sin service worker, sin contar la visita y en claro, como se imprime un diario
            ctx = nav.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=ANCHO / 1280,
                                  color_scheme="light", service_workers="block")
            pag = ctx.new_page()
            for codigo, idioma in generar.IDIOMAS.items():
                for d in generar.cargar():
                    if not d["piezas"]:
                        continue
                    destino = SALIDA / f'{d["fecha"]}-{codigo}.jpg'
                    if (d["fecha"] not in pedidas) if pedidas else destino.exists():
                        continue
                    pagina = generar.SITIO / idioma["carpeta"] / d["fecha"] / "index.html"
                    if not pagina.exists():
                        continue
                    pag.goto(f'{base}{idioma["carpeta"]}{d["fecha"]}/?nocontar=1', wait_until="networkidle")
                    pag.evaluate("document.fonts.ready")
                    vineta = pag.query_selector("section.vineta")
                    if vineta:
                        caja = vineta.bounding_box()
                        alto = int(caja["y"] + caja["height"] + 24)
                    else:   # un día sin viñeta: hasta donde llegue la página
                        alto = int(pag.evaluate("document.documentElement.scrollHeight"))
                    pag.screenshot(path=str(destino), full_page=True, type="jpeg", quality=CALIDAD,
                                   clip={"x": 0, "y": 0, "width": 1280, "height": alto})
                    medidas[destino.name] = [ANCHO, round(alto * ANCHO / 1280)]
                    hechas += 1
            nav.close()
    finally:
        servidor.shutdown()
        f_medidas.write_text(json.dumps(dict(sorted(medidas.items())), indent=0) + "\n")
    print(f"portadas: {hechas} miniatura(s)")


if __name__ == "__main__":
    main()
