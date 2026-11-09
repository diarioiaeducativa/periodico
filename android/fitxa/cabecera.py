# SPDX-License-Identifier: AGPL-3.0-or-later
"""La cabecera de la ficha de Google Play (1024 × 500) en cada idioma (ADR 0042).

    python3 android/fitxa/cabecera.py      deja cabecera-XX.png aquí

Es la imagen de vista previa del diario (og/og-es.html): la mancheta, el filete, el lema y Tiza y
Algoritmo, con el título y el lema de cada edición, sacados de generar.py. Hace falta sitio/ generado
(la letra y los estilos salen de allí).
"""

import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ))

from playwright.sync_api import sync_playwright  # noqa: E402
import generar  # noqa: E402


def html(codigo):
    d = generar.IDIOMAS[codigo]
    base = (RAIZ / "og" / "og-es.html").read_text()
    base = base.replace('href="../sitio/', f'href="{(RAIZ / "sitio").as_uri()}/')
    base = base.replace('lang="es"', f'lang="{codigo}"')
    base = base.replace("width:1200px;height:630px", "width:1024px;height:500px")
    base = base.replace("grid-template-columns:1fr 380px;align-items:center;height:630px;padding:0 64px",
                        "grid-template-columns:1fr 300px;align-items:center;height:500px;padding:0 56px")
    base = base.replace("font-size:104px", "font-size:86px").replace("font-size:31px", "font-size:27px")
    base = base.replace(".vineta svg{width:380px}", ".vineta svg{width:300px}")
    base = re.sub(r"<h1>.*?</h1>", f"<h1>{d['titulo']}</h1>", base)
    return re.sub(r"<p>.*?</p>", f"<p>{d['lema']}</p>", base, count=1)


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={"width": 1024, "height": 500})
    for codigo in generar.IDIOMAS:
        tmp = AQUI / f".cabecera-{codigo}.html"
        tmp.write_text(html(codigo))
        pag.goto(tmp.as_uri())
        pag.wait_for_timeout(500)
        pag.screenshot(path=str(AQUI / f"cabecera-{codigo}.png"))
        tmp.unlink()
        print(AQUI / f"cabecera-{codigo}.png")
    nav.close()
