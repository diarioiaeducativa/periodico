# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las capturas de la ficha de Google Play (1080 × 1920), del diario publicado (ADR 0042).

    python3 android/fitxa/capturas.py [es,ca,...]

Cuatro por idioma, como se ven en la app, que no lleva barra de dirección: la portada, la primera
pieza del último número, la viñeta y, en tema oscuro, la hemeroteca. Quedan en android/fitxa/capturas/
en JPEG, que Play admite. Playwright no suma visitas al contador (ADR 0033).
"""

import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

AQUI = pathlib.Path(__file__).resolve().parent
SALIDA = AQUI / "capturas"
BASE = "https://diarioiaeducativa.github.io/"
IDIOMAS = sys.argv[1].split(",") if len(sys.argv) > 1 else ["es", "ca", "gl", "eu", "en"]


def contexto(nav, codigo, tema):
    c = nav.new_context(locale=codigo, viewport={"width": 360, "height": 640}, device_scale_factor=3,
                        is_mobile=True, has_touch=True, color_scheme=tema)
    c.add_init_script(f"try{{localStorage.setItem('sala.idioma','{codigo}');}}catch(_){{}}")
    return c


def foto(pag, nombre):
    png = SALIDA / f"{nombre}.png"
    pag.wait_for_timeout(1500)
    pag.screenshot(path=str(png))
    subprocess.run(["convert", str(png), "-quality", "86", str(png.with_suffix(".jpg"))], check=True)
    png.unlink()
    print(png.with_suffix(".jpg"))


SALIDA.mkdir(exist_ok=True)
with sync_playwright() as p:
    nav = p.chromium.launch()
    for codigo in IDIOMAS:
        raiz = BASE + ("" if codigo == "es" else codigo + "/")
        c = contexto(nav, codigo, "light")
        pag = c.new_page()
        pag.goto(raiz, wait_until="networkidle")
        foto(pag, f"{codigo}-1-portada")
        pieza = pag.eval_on_selector_all(
            "main a[href]", "as => as.map(a => a.href).find(h => /\\d{4}-\\d{2}-\\d{2}\\/[^/]+\\.html$/.test(h))")
        pag.goto(pieza, wait_until="networkidle")
        foto(pag, f"{codigo}-2-pieza")
        pag.goto(raiz + "vineta.html", wait_until="networkidle")
        foto(pag, f"{codigo}-3-vineta")
        c.close()
        c = contexto(nav, codigo, "dark")
        pag = c.new_page()
        pag.goto(raiz + "archivo.html", wait_until="networkidle")
        foto(pag, f"{codigo}-4-hemeroteca")
        c.close()
    nav.close()
