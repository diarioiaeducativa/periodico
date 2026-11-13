#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La imagen de vista previa de cada número (ADR 0010): la mancheta, el número, la fecha y la
pieza que abre la portada, con su dibujo. La enseñan Telegram y las redes al compartir la portada
o el día, y así cada aviso de la mañana se ve distinto del anterior.

    scripts/og-numero.py [AAAA-MM-DD ...]   (fechas de las conversaciones; sin fechas, las que falten)

Escribe og/numeros/<fecha>-<es|ca>.png (1200 × 630); generar.py las copia a sitio/og/ y las pone
en la portada y en la página de cada día. Sin IA: Chromium de Playwright hace la captura.

Y la de cada pieza (og/piezas/<idioma>/<fecha>-<id>.png), con su propio titular y su dibujo, en los cinco
idiomas, para que al compartir una noticia no salga la imagen genérica. Como son muchas (una por pieza y por
idioma), se aligeran con Pillow: reducidas a 64 colores pesan un tercio (de unos 78 kB a unos 26) y no se
nota, porque son tinta sobre papel y un dibujo de colores planos. Sin Pillow se quedan como salen.
Si falla, el sitio sigue con la imagen genérica (og-es.png, og-ca.png).
"""
import html
import pathlib
import re
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402

SALIDA = RAIZ / "og" / "numeros"
PIEZAS = RAIZ / "og" / "piezas"
EST = (RAIZ / "estaticos").as_uri()


def apertura(d):
    """La pieza que abre el número: la primera que no es de la Biblioteca, como en la portada."""
    return next((p for p in d["piezas"] if p.get("seccion") != "biblioteca"), d["piezas"][0])


def dibujo(d, p):
    f = generar.con_traduccion("ilustraciones", f'{d["fecha"]}-{p["id"]}.svg')
    if f.exists():
        return re.sub(r"<\?xml.*?\?>", "", f.read_text()).strip()
    # Un artículo del repositorio lleva la captura de su recurso
    r = next((x for x in p.get("recursos", []) if x.get("captura")), None)
    if r:
        c = RAIZ / "repositorio" / "capturas" / pathlib.Path(r["captura"]).name
        if c.exists():
            return f'<img src="{c.as_uri()}" alt="">'
    return generar.icono(p.get("seccion"))


def pagina(d, p):
    L = generar.L
    e = html.escape
    sale = generar.publicacion(d["fecha"])
    seccion = L["reportaje"] if p.get("reportaje") else L["secciones"].get(p.get("seccion"), "")
    return f"""<!doctype html><html lang="{L["codigo"]}" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="{EST}/fuentes.css"><link rel="stylesheet" href="{EST}/comun.css"><link rel="stylesheet" href="{EST}/diario.css">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#fbfbf9;color:#16181d}}
.og{{display:grid;grid-template-columns:1fr 520px;gap:40px;height:630px;padding:52px 60px;box-sizing:border-box}}
.izq{{display:flex;flex-direction:column;min-width:0}}
.mancheta{{font-family:Newsreader;font-weight:800;font-size:58px;line-height:1;letter-spacing:-.02em;font-variation-settings:"opsz" 72;margin:0}}
.filete{{height:8px;border-top:4px solid #16181d;border-bottom:2px solid #16181d;margin:18px 0 14px}}
.cuando{{font-family:Newsreader;font-style:italic;font-size:27px;color:#4f5562;margin:0}}
.cuando b{{font-style:normal;color:#c42b1c}}
.seccion{{margin:auto 0 10px;font-family:Newsreader;font-weight:700;font-size:22px;letter-spacing:.06em;text-transform:uppercase;color:var(--sec,#1d3fa6)}}
.titular{{font-family:Newsreader;font-weight:700;font-size:46px;line-height:1.1;letter-spacing:-.01em;margin:0;
  display:-webkit-box;-webkit-line-clamp:7;-webkit-box-orient:vertical;overflow:hidden;font-variation-settings:"opsz" 48}}
.der{{align-self:center;display:flex;align-items:center;justify-content:center;background:var(--papel-2);padding:18px;box-sizing:border-box;margin:0;max-height:526px}}
.der svg,.der img{{width:100%;height:auto;max-height:100%}}
.der svg.ico{{width:55%;color:var(--sec,#1d3fa6)}}
</style></head>
<body><div class="og sec-{"reportaje" if p.get("reportaje") else e(p.get("seccion") or "")}">
<div class="izq">
  <p class="mancheta">{e(L["titulo"])}</p>
  <div class="filete"></div>
  <p class="cuando"><b>{e(L["num"])} {d["numero"]}</b> · {e(generar.mayus(generar.fecha_larga(sale)))}</p>
  <p class="seccion">{e(seccion)}</p>
  <h1 class="titular">{e(p["titular"])}</h1>
</div>
<figure class="der ilu">{dibujo(d, p)}</figure>
</div></body></html>"""


def aligerar(ruta, colores=64):
    """Reduce la imagen a una paleta de pocos colores, sin tramado. Una captura de pantalla (la de un recurso
    del repositorio) tiene degradados y pide más colores que un dibujo."""
    try:
        from PIL import Image
    except ImportError:
        return
    with Image.open(ruta) as im:
        q = im.convert("RGB").quantize(colors=colores, dither=Image.Dither.NONE)
    q.save(ruta, "PNG", optimize=True)


# El titular llena la columna (Juanjo, 07-11-2026: sin huecos entre la fecha y la sección, ningún día):
# crece desde 46 px mientras quepa entero y, si no cabe, baja hasta 34 px.
AJUSTE = """() => {
  const t = document.querySelector('.titular');
  const cabe = () => t.getBoundingClientRect().bottom <= 630 - 52 && t.scrollHeight <= t.clientHeight + 1;
  let s = 46;
  t.style.fontSize = s + 'px';
  while (!cabe() && s > 34) { s -= 2; t.style.fontSize = s + 'px'; }
  while (s < 66) { t.style.fontSize = (s + 2) + 'px'; if (!cabe()) { t.style.fontSize = s + 'px'; break; } s += 2; }
  const sec = document.querySelector('.seccion'), hueco = sec.getBoundingClientRect().top - document.querySelector('.cuando').getBoundingClientRect().bottom;
  return [s, Math.round(hueco)];
}"""


def main():
    from playwright.sync_api import sync_playwright
    SALIDA.mkdir(parents=True, exist_ok=True)
    pedidas = set(sys.argv[1:])
    hechas = 0
    en_castellano = {}   # el titular de cada pieza en castellano, para saber si la de otro idioma está traducida
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        nav = pw.chromium.launch()
        pag = nav.new_page(viewport={"width": 1200, "height": 630})
        for codigo in generar.IDIOMAS:   # el castellano va primero
            generar.L = generar.IDIOMAS[codigo]
            for d in generar.cargar():
                if not (d.get("numero") and d["piezas"]):
                    continue
                destino = SALIDA / f'{d["fecha"]}-{codigo}.png'
                pedida = d["fecha"] in pedidas
                h = pathlib.Path(tmp) / "og.html"

                def captura(p, donde, ligera=False):
                    texto = pagina(d, p)
                    h.write_text(texto)
                    pag.goto(h.as_uri())
                    pag.evaluate("document.fonts.ready")
                    pag.evaluate(AJUSTE)
                    pag.screenshot(path=str(donde))
                    if ligera:
                        aligerar(donde, 256 if '<figure class="der ilu"><img' in texto else 64)

                if pedida if pedidas else not destino.exists():
                    captura(apertura(d), destino)
                    hechas += 1
                    if codigo == "es":   # la de cada grupo, para su aviso (los avisos van en castellano)
                        for g in generar.GRUPOS:
                            p = generar.pieza_de_grupo(d, g)
                            if not p or p is apertura(d):
                                continue
                            captura(p, SALIDA / f'{d["fecha"]}-es-{g}.png')
                            hechas += 1
                if pedidas and not pedida:
                    continue
                # La de cada pieza del número, también el reportaje, en cada idioma. Si la pieza aún no está
                # traducida (el titular es el del castellano), no se hace: generar.py pone la del castellano.
                carpeta = PIEZAS / codigo
                carpeta.mkdir(parents=True, exist_ok=True)
                for p in d["piezas"] + ([d["reportaje"]] if d.get("reportaje") else []):
                    clave = (d["fecha"], p["id"])
                    if codigo == "es":
                        en_castellano[clave] = p["titular"]
                    elif p["titular"] == en_castellano.get(clave):
                        continue
                    dp = carpeta / f'{d["fecha"]}-{p["id"]}.png'
                    if dp.exists() and not pedida:
                        continue
                    captura(p, dp, ligera=True)
                    hechas += 1
        nav.close()
    print(f"og-numero: {hechas} imagen(es)")


if __name__ == "__main__":
    main()
