#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Revisa los dibujos de un día tal como se ven en el sitio, en tema claro y oscuro (ADR 0005).

    revisar-dibujos.py AAAA-MM-DD [es|ca] [id ...]

Sin IA: abre en un Chromium sin pantalla la página de cada pieza con dibujo (las de la edición,
la presentación, la Biblioteca y el reportaje del día), en los dos temas, y comprueba lo que se puede medir:

- ningún relleno negro puro (una forma sin clase o con una variable de color sin definir; la
  tinta del diario nunca es #000),
- todas las formas y rótulos con una de las clases de la hoja de estilo (o la de su <g>, en un icono de Lucide),
- rótulos dentro del dibujo y sin pisarse entre ellos,
- contraste de rótulos (4,5:1) y trazos (3:1) con el fondo del dibujo.

Deja una captura de cada dibujo en cada tema en revision/FECHA/ (las mira después el revisor
visual) y el resultado en revision/FECHA/<idioma>.json. Hay que haber generado el sitio antes.
Sale con 0 si todo está bien, 4 si algún dibujo tiene problemas y 1 si no ha podido revisar.
"""
import functools
import http.server
import json
import pathlib
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"
CLASES = {"t", "a", "r", "fa", "ft", "fz", "lbl"}

MEDIR = """(fig) => {
  const svg = fig.querySelector('svg'), caja = svg.getBoundingClientRect(), out = [];
  const rgb = s => (s.match(/[\\d.]+/g) || []).slice(0, 4).map(Number);
  const lum = c => { const v = c.slice(0, 3).map(x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; });
                     return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  const contraste = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  let fondo = null;
  for (let n = fig; n && !fondo; n = n.parentElement) {
    const c = rgb(getComputedStyle(n).backgroundColor);
    if (c.length >= 3 && (c.length < 4 || c[3] > 0)) fondo = c;
  }
  fondo = fondo || [255, 255, 255];
  const formas = svg.querySelectorAll('path, circle, rect, ellipse, polygon, polyline, line, text');
  let sinClase = 0, negros = 0;
  formas.forEach(el => {
    let clases = [];   // la suya o, en un icono de Lucide (ADR 0014), la de su <g>
    for (let n = el; n && n !== svg; n = n.parentElement) clases = clases.concat((n.getAttribute('class') || '').split(/\\s+/).filter(Boolean));
    if (!clases.some(c => CLASES.includes(c))) sinClase++;
    const f = getComputedStyle(el).fill;
    if (f === 'rgb(0, 0, 0)') negros++;
  });
  if (sinClase) out.push(`${sinClase} forma(s) o rótulo(s) sin ninguna clase de la hoja de estilo`);
  if (negros) out.push(`${negros} relleno(s) negro(s) puro(s): forma sin clase o color de relleno sin definir`);
  const rotulos = [...svg.querySelectorAll('text')].map(t => ({t: t.textContent.trim(), b: t.getBoundingClientRect(), el: t}));
  rotulos.forEach(r => {
    if (r.b.left < caja.left - 1 || r.b.right > caja.right + 1 || r.b.top < caja.top - 1 || r.b.bottom > caja.bottom + 1)
      out.push(`el rótulo «${r.t}» se sale del dibujo`);
    const c = contraste(rgb(getComputedStyle(r.el).fill), fondo);
    if (c < 4.5) out.push(`el rótulo «${r.t}» tiene poco contraste con el fondo (${c.toFixed(1)}:1)`);
  });
  for (let i = 0; i < rotulos.length; i++) for (let j = i + 1; j < rotulos.length; j++) {
    const a = rotulos[i].b, b = rotulos[j].b;
    const x = Math.min(a.right, b.right) - Math.max(a.left, b.left), y = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (x > 2 && y > 2) out.push(`los rótulos «${rotulos[i].t}» y «${rotulos[j].t}» se pisan`);
  }
  const vistos = new Set();
  svg.querySelectorAll('.t, .a, .r').forEach(el => {
    const s = getComputedStyle(el).stroke, c = contraste(rgb(s), fondo), k = (el.getAttribute('class') || '') + s;
    if (c < 3 && !vistos.has(k)) { vistos.add(k); out.push(`trazo «${el.getAttribute('class')}» con poco contraste con el fondo (${c.toFixed(1)}:1)`); }
  });
  return out;
}"""


def dibujos(fecha, idioma):
    """Las piezas del día que tienen dibujo: id, titular y página."""
    sufijo = "" if idioma == "es" else f"-{idioma}"
    carpeta = "" if idioma == "es" else f"{idioma}/"
    piezas = []
    ed = RAIZ / "ediciones" / f"{fecha}.json"
    if ed.exists():
        d = json.loads(ed.read_text())
        piezas += d.get("piezas", []) + ([d["editorial"]] if d.get("editorial") else [])
    bib = RAIZ / "biblioteca" / f"{fecha}.json"   # los artículos de la Biblioteca digital (ADR 0006)
    if bib.exists():
        piezas += json.loads(bib.read_text()).get("piezas", [])
    rep = RAIZ / "reportajes" / f"{fecha}.json"
    if rep.exists():
        r = json.loads(rep.read_text())
        if r.get("hay_reportaje"):
            piezas.append(r)
    out = []
    for p in piezas:
        svg = RAIZ / f"ilustraciones{sufijo}" / f"{fecha}-{p['id']}.svg"
        if not svg.exists() and sufijo:
            continue   # sin traducción, la página catalana usa el dibujo castellano, ya revisado
        if svg.exists():
            out.append({"id": p["id"], "titular": p.get("titular", ""), "svg": str(svg.relative_to(RAIZ)),
                        "pagina": f"{carpeta}{fecha}/{p['id']}.html"})
    return out


def servidor():
    class Callado(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    manejador = functools.partial(Callado, directory=str(SITIO))
    srv = socketserver.TCPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    fecha = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else "es"
    solo = set(sys.argv[3:])
    lista = [d for d in dibujos(fecha, idioma) if not solo or d["id"] in solo]
    salida = RAIZ / "revision" / fecha
    salida.mkdir(parents=True, exist_ok=True)
    if not lista:
        print(f"{idioma}: ningún dibujo que revisar")
        (salida / f"{idioma}.json").write_text(json.dumps({"fecha": fecha, "idioma": idioma, "dibujos": []}, ensure_ascii=False, indent=1))
        return 0
    srv = servidor()
    base = f"http://127.0.0.1:{srv.server_address[1]}/"
    medir = MEDIR.replace("CLASES.includes", json.dumps(sorted(CLASES)) + ".includes")
    try:
        with sync_playwright() as pw:
            nav = pw.chromium.launch()
            try:
                for tema, nombre in (("light", "claro"), ("dark", "oscuro")):
                    pg = nav.new_page(color_scheme=tema, viewport={"width": 1100, "height": 900})
                    pg.set_default_timeout(20000)
                    for d in lista:
                        pg.goto(base + d["pagina"], wait_until="load")
                        fig = pg.locator("main .ilu").first
                        if not fig.count():
                            d.setdefault("problemas", []).append(f"la página no muestra el dibujo ({nombre})")
                            continue
                        problemas = fig.evaluate(medir)
                        d.setdefault("problemas", []).extend(f"{p} ({nombre})" for p in problemas)
                        captura = salida / f"{idioma}-{d['id']}-{nombre}.png"
                        fig.screenshot(path=str(captura))
                        d.setdefault("capturas", []).append(str(captura.relative_to(RAIZ)))
                    pg.close()
            finally:
                nav.close()
    except Exception as err:   # sin navegador no hay revisión: lo dice y quien llama decide
        print(f"ERROR: no se pudieron revisar los dibujos: {err}")
        return 1
    finally:
        srv.shutdown()
    (salida / f"{idioma}.json").write_text(json.dumps({"fecha": fecha, "idioma": idioma, "dibujos": lista}, ensure_ascii=False, indent=1))
    malos = [d for d in lista if d.get("problemas")]
    for d in lista:
        print(f"{idioma} {d['id']}: " + ("; ".join(d["problemas"]) if d.get("problemas") else "bien"))
    return 4 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
