#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El número del día en Instagram, como carrusel de @comunidad.iaeducativa (ADR 0015).

    scripts/instagram.py imagenes AAAA-MM-DD   las imágenes del carrusel y su texto
    scripts/instagram.py publicar AAAA-MM-DD   las sube y publica el carrusel
    scripts/instagram.py reel AAAA-MM-DD       publica «La semana en vídeo» del sábado AAAA-MM-DD (ADR 0016)
    scripts/instagram.py renovar               renueva el permiso de Instagram si tiene más de 7 días
    scripts/instagram.py comprobar             dice si el permiso sigue valiendo y hasta cuándo

AAAA-MM-DD es la fecha de las conversaciones, como en los demás scripts; el número sale al día
siguiente. `imagenes` escribe instagram/<fecha>/NN.jpg (1080 × 1350) y texto.txt: la portada con
los titulares, una imagen por pieza, las tres viñetas de Tiza y Algoritmo y el cierre. Las hace
Chromium de Playwright con los datos del número, sin IA; si un texto no cabe ni con la letra más
pequeña permitida, falla y no hay carrusel ese día. `publicar` las sube a la rama `instagram` del
repositorio del sitio, que se rehace cada día con un solo commit para no engordar su historia, y
publica con la API oficial de Instagram (inicio de sesión unificado, graph.facebook.com) usando el permiso guardado en
~/.config/diario-instagram.json. Publica una sola vez por número: el estado queda en
estado/<fecha>.instagram con el enlace de la publicación.
"""
import datetime
import html
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402
import vineta  # noqa: E402

ANCHO, ALTO = 1080, 1350
EST = (RAIZ / "estaticos").as_uri()
SALIDA = RAIZ / "instagram"
CREDENCIALES = pathlib.Path(os.environ.get("INSTAGRAM_CREDENCIALES", pathlib.Path.home() / ".config" / "diario-instagram.json"))
API = "https://graph.facebook.com/v24.0"   # se puede cambiar con "api" en las credenciales
REPO_SITIO = os.environ.get("INSTAGRAM_REPO", "git@github.com:diarioiaeducativa/diarioiaeducativa.github.io.git")
RAMA = "instagram"
URL_IMAGENES = "https://raw.githubusercontent.com/diarioiaeducativa/diarioiaeducativa.github.io/instagram"
MAX_PIEZAS = 5
ETIQUETAS = "#IAEducativa #InteligenciaArtificial #Educación #Docentes #EdTech"
GRUPOS_TXT = "ChatGPT-IA-edu, Vibe Coding Educativo y EduMedia-IAG"

e = html.escape


def _og():
    """og-numero.py: su forma de elegir el dibujo de una pieza (dibujo, captura o icono)."""
    spec = importlib.util.spec_from_file_location("og_numero", RAIZ / "scripts" / "og-numero.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------- Las imágenes ----------

CSS = """
html,body{margin:0;width:1080px;height:1350px;overflow:hidden;background:#fbfbf9;color:#16181d}
.ig{box-sizing:border-box;width:1080px;height:1350px;padding:64px 72px 72px;display:flex;flex-direction:column}
.cab{display:flex;justify-content:space-between;align-items:baseline;font-family:Newsreader;font-size:28px;color:#4f5562}
.cab b{font-weight:800;color:#16181d;letter-spacing:-.01em;font-size:30px}
.cab i b{font-style:normal;color:#c42b1c;font-size:28px}
.filete{height:8px;border-top:4px solid #16181d;border-bottom:2px solid #16181d;margin:16px 0 34px;flex:none}
.seccion{display:flex;align-items:center;justify-content:flex-start;gap:12px;font-family:Newsreader;font-weight:700;font-size:30px;letter-spacing:.06em;text-transform:uppercase;color:var(--sec,#1d3fa6);margin:0 0 12px}
.seccion .ico{width:34px;height:34px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.ante{font-family:Newsreader;font-style:italic;font-size:32px;color:#4f5562;margin:0 0 8px}
.titular{font-family:Newsreader;font-weight:700;font-size:62px;line-height:1.08;letter-spacing:-.015em;margin:0;font-variation-settings:"opsz" 60}
.entradilla{font-family:Newsreader;font-size:34px;line-height:1.3;color:#2f3440;margin:26px 0 0;flex:none}
.dibujo{flex:1 1 auto;min-height:0;margin:30px 0 0;display:flex;align-items:center;justify-content:center;background:var(--papel-2);padding:24px;box-sizing:border-box;overflow:hidden}
.dibujo svg,.dibujo img{max-width:100%;max-height:100%;width:auto;height:100%}
.dibujo svg.ico{width:40%;height:auto;color:var(--sec,#1d3fa6)}
/* portada */
.mancheta{font-family:Newsreader;font-weight:800;font-size:124px;line-height:.95;letter-spacing:-.03em;margin:18px 0 0;font-variation-settings:"opsz" 72}
.cuando{font-family:Newsreader;font-style:italic;font-size:38px;color:#4f5562;margin:0}
.cuando b{font-style:normal;color:#c42b1c}
.hoy{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:34px;flex:1 1 auto;min-height:0;overflow:hidden}
.hoy li{border-left:8px solid var(--sec,#1d3fa6);padding-left:22px}
.hoy .s{display:block;font-family:Newsreader;font-weight:700;font-size:24px;letter-spacing:.06em;text-transform:uppercase;color:var(--sec,#1d3fa6)}
.hoy .t{display:block;font-family:Newsreader;font-weight:700;font-size:46px;line-height:1.12;letter-spacing:-.01em}
.desliza{flex:none;margin:18px 0 0;text-align:right;font-family:Newsreader;font-style:italic;font-size:30px;color:#4f5562}
svg.vineta{border:0;margin:0;padding:0}
/* viñeta */
.vt{display:flex;justify-content:space-between;align-items:baseline;font-family:Newsreader;font-weight:700;font-size:40px;color:var(--sec);margin:0 0 22px}
.vt span{font-weight:400;font-style:italic;font-size:30px;color:#4f5562}
.panel-ig{flex:1 1 auto;display:flex;align-items:center;justify-content:center;min-height:0}
.panel-ig svg{width:100%;height:auto;max-height:100%}
.origen{font-family:Newsreader;font-style:italic;font-size:30px;line-height:1.3;color:#4f5562;margin:22px 0 0;flex:none}
/* cierre */
.cierre{justify-content:center;text-align:center;align-items:center}
.cierre .mancheta{font-size:112px;margin:30px 0 26px}
.cierre .lema{font-family:Newsreader;font-style:italic;font-size:40px;line-height:1.25;color:#2f3440;margin:0 40px 54px}
.cierre .hora{font-family:Newsreader;font-weight:700;font-size:44px;margin:0 0 12px}
.cierre .enlace{font-family:Newsreader;font-size:38px;margin:0 0 8px;color:#2f3440}
.cierre .web{font-family:Newsreader;font-weight:700;font-size:38px;color:#1c3faa;margin:0}
.cierre svg{width:520px;height:auto}
"""

# Lo que mide cada texto para encajar: se reduce de 2 en 2 px hasta su mínimo (ADR 0015)
AJUSTE = """
() => {
  const pag = document.querySelector('.ig');
  const ajustables = [...document.querySelectorAll('[data-min]')];
  const desborda = () => pag.scrollHeight > pag.clientHeight + 1 ||
    ajustables.some(el => el.scrollWidth > el.clientWidth + 1) ||
    [...document.querySelectorAll('.dibujo')].some(d => d.clientHeight < 300) ||
    [...document.querySelectorAll('.hoy')].some(c => c.scrollHeight > c.clientHeight + 1);
  let vueltas = 0;
  while (desborda() && vueltas < 80) {
    let cambio = false;
    for (const el of ajustables) {
      const t = parseFloat(getComputedStyle(el).fontSize);
      if (t - 2 >= +el.dataset.min) { el.style.fontSize = (t - 2) + 'px'; cambio = true; }
    }
    if (!cambio) break;
    vueltas++;
  }
  return !desborda();
}
"""


def cabeza():
    return (f'<!doctype html><html lang="es" data-theme="light"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{EST}/fuentes.css"><link rel="stylesheet" href="{EST}/comun.css">'
            f'<link rel="stylesheet" href="{EST}/diario.css"><style>{CSS}</style></head><body>')


def barra(d):
    sale = generar.publicacion(d["fecha"])
    f = datetime.date.fromisoformat(sale)
    corta = f'{f.day} {generar.L["meses"][f.month - 1][:3]}. {f.year}'
    return (f'<div class="cab"><b>{e(generar.L["titulo"])}</b><i><b>{e(generar.L["num"])} {d["numero"]}</b> · {e(corta)}</i></div>'
            f'<div class="filete"></div>')


def pareja(expr_t="contento", expr_a="contento", postura="abajo"):
    """Tiza y Algoritmo juntos, con el dibujo de la viñeta (vineta.py)."""
    t, _ = vineta.tiza(150, "derecha", expr_t, postura)
    a, _ = vineta.algoritmo(250, "izquierda", expr_a, postura)
    return f'<svg class="vineta" viewBox="40 150 320 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{t}{a}</svg>'


def portada(d, piezas):
    L = generar.L
    sale = generar.publicacion(d["fecha"])
    items = "".join(
        f'<li class="sec-{e(p.get("seccion") or "")}"><span class="s">{e(L["secciones"].get(p.get("seccion"), ""))}</span>'
        f'<span class="t" data-min="32">{e(p["titular"])}</span></li>' for p in piezas)
    return cabeza() + f"""<div class="ig">
<p class="cuando"><b>{e(L["num"])} {d["numero"]}</b> · {e(generar.fecha_larga(sale).capitalize())}</p>
<p class="mancheta">{e(L["titulo"])}</p>
<div class="filete"></div>
<ul class="hoy">{items}</ul>
<p class="desliza">Desliza para leer →</p>
</div></body></html>"""


def pieza(d, p, og):
    L = generar.L
    ante = f'<p class="ante" data-min="26">{e(p["antetitulo"])}</p>' if p.get("antetitulo") else ""
    entr = f'<p class="entradilla" data-min="27">{e(p["entradilla"])}</p>' if p.get("entradilla") else ""
    return cabeza() + f"""<div class="ig sec-{e(p.get("seccion") or "")}">
{barra(d)}
<p class="seccion">{generar.icono(p.get("seccion"))}{e(L["secciones"].get(p.get("seccion"), ""))}</p>
{ante}<h1 class="titular" data-min="42">{e(p["titular"])}</h1>
<figure class="dibujo ilu">{og.dibujo(d, p)}</figure>
{entr}
</div></body></html>"""


def panel_vineta(d, guion, n, origen):
    v = guion["vinetas"][n - 1]
    pie = f'<p class="origen" data-min="24">{e(origen)}</p>' if (n == 3 and origen) else ""
    return cabeza() + f"""<div class="ig sec-vineta">
{barra(d)}
<p class="vt">{e(generar.L["vineta_titulo"])} <span>{n}/3</span></p>
<div class="panel-ig vineta">{vineta.panel(v, n)}</div>
{pie}
</div></body></html>"""


def cierre():
    L = generar.L
    return cabeza() + f"""<div class="ig cierre">
{pareja("riendo", "contento", "arriba")}
<p class="mancheta">{e(L["titulo"])}</p>
<p class="lema">{e(L["lema"])}</p>
<p class="hora">Cada mañana, a las 7:00</p>
<p class="enlace">El número completo, en el enlace del perfil</p>
<p class="web">diarioiaeducativa.github.io</p>
</div></body></html>"""


def numero(fecha):
    generar.L = generar.IDIOMAS["es"]
    d = next((x for x in generar.cargar() if x["fecha"] == fecha), None)
    if not d or not d.get("numero") or not d["piezas"]:
        sys.exit(f"instagram: no hay número con las conversaciones del {fecha}")
    return d


def guion_vineta(fecha, d):
    f = RAIZ / "vinetas" / f"{fecha}.json"
    if not f.exists():
        return None, ""
    el = json.loads(f.read_text()).get("elegida")
    if not el or len(el.get("guion", {}).get("vinetas", [])) < 3:
        return None, ""
    p = next((x for x in d["piezas"] if x["id"] == el.get("pieza")), None)
    return el["guion"], (f'A partir de «{p["titular"]}»' if p else "")


def texto(d, piezas, hay_vineta):
    """La descripción: la entradilla que escribe el agente de los avisos (campo `instagram` de
    avisos/<publicación>.json) o, si falta, los titulares; y siempre la cabecera y el pie fijos."""
    L = generar.L
    sale = generar.publicacion(d["fecha"])
    cab = f'{L["titulo"]} · {L["num"]} {d["numero"]} · {generar.fecha_larga(sale).capitalize()}'
    propio = ""
    f = RAIZ / "avisos" / f"{sale}.json"
    if f.exists():
        try:
            propio = (json.loads(f.read_text()).get("instagram") or "").strip()
        except ValueError:
            propio = ""
    if not (60 <= len(propio) <= 900) or "http" in propio or "#" in propio:
        propio = "En este número:\n" + "\n".join(f"· {p['titular']}" for p in piezas)
        if hay_vineta:
            propio += "\n· La viñeta de Tiza y Algoritmo"
    pie = (f"El número completo, en el enlace del perfil.\n\n"
           f"Redactado y dibujado con IA a partir de lo que se habla en los grupos de Telegram {GRUPOS_TXT}.\n\n"
           f"{ETIQUETAS}")
    return f"{cab}\n\n{propio}\n\n{pie}"


def alt(html_txt):
    t = re.sub(r"<style.*?</style>|<svg.*?</svg>", " ", html_txt, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()[:900]


def imagenes(fecha):
    from playwright.sync_api import sync_playwright
    d = numero(fecha)
    og = _og()
    piezas = d["piezas"][:MAX_PIEZAS]
    guion, origen = guion_vineta(fecha, d)
    paginas = [portada(d, piezas)] + [pieza(d, p, og) for p in piezas]
    if guion:
        paginas += [panel_vineta(d, guion, n, origen) for n in (1, 2, 3)]
    paginas.append(cierre())
    destino = SALIDA / fecha
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    malas = []
    alts = []
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        nav = pw.chromium.launch()
        pag = nav.new_page(viewport={"width": ANCHO, "height": ALTO})
        for i, h in enumerate(paginas, 1):
            f = pathlib.Path(tmp) / f"{i}.html"
            f.write_text(h)
            pag.goto(f.as_uri())
            pag.evaluate("document.fonts.ready")
            if not pag.evaluate(AJUSTE):
                malas.append(i)
            pag.screenshot(path=str(destino / f"{i:02d}.jpg"), type="jpeg", quality=88)
            alts.append(alt(h))
        nav.close()
    (destino / "texto.txt").write_text(texto(d, piezas, bool(guion)))
    (destino / "alt.json").write_text(json.dumps(alts, ensure_ascii=False, indent=1))
    if malas:
        print(f"instagram: el texto no cabe en las imágenes {malas}; no hay carrusel", file=sys.stderr)
        (destino / "NO-CABE").write_text(" ".join(map(str, malas)))
        sys.exit(2)
    print(f"instagram: {len(paginas)} imágenes en {destino.relative_to(RAIZ)}")


# ---------- La publicación ----------

def credenciales():
    return json.loads(CREDENCIALES.read_text())


def guardar(c):
    CREDENCIALES.parent.mkdir(parents=True, exist_ok=True)
    tmp = CREDENCIALES.with_suffix(".tmp")
    tmp.write_text(json.dumps(c, indent=1))
    os.chmod(tmp, 0o600)
    tmp.replace(CREDENCIALES)


def llamada(metodo, ruta, token, **datos):
    datos["access_token"] = token
    cuerpo = urllib.parse.urlencode(datos).encode()
    api = credenciales().get("api", API) if CREDENCIALES.exists() else API
    url = f"{api}/{ruta}" if metodo == "POST" else f"{api}/{ruta}?{cuerpo.decode()}"
    req = urllib.request.Request(url, data=cuerpo if metodo == "POST" else None, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as err:
        detalle = err.read().decode(errors="replace")
        detalle = detalle.replace(token, "…")
        raise RuntimeError(f"{metodo} {ruta}: HTTP {err.code} {detalle}") from None


def subir_rama(fecha, origen=None):
    """Las imágenes, en la rama `instagram` del repositorio del sitio: un solo commit que se
    rehace cada día (push forzado), así no se acumulan en la historia."""
    origen = origen or SALIDA / fecha
    with tempfile.TemporaryDirectory() as tmp:
        g = lambda *a: subprocess.run(["git", "-C", tmp, *a], check=True, capture_output=True, text=True)  # noqa: E731
        g("init", "-q", "-b", RAMA)
        g("config", "user.name", "Diario de IA Educativa")
        g("config", "user.email", "diarioiaeducativa@users.noreply.github.com")
        dest = pathlib.Path(tmp) / fecha
        dest.mkdir()
        for f in sorted(origen.glob("*.jpg")) + sorted(origen.glob("*.mp4")):
            shutil.copy(f, dest / f.name)
        (pathlib.Path(tmp) / "README.md").write_text(
            "Imágenes del carrusel de Instagram del día. Se rehace cada mañana; no es parte del sitio.\n")
        g("add", "-A")
        g("commit", "-qm", f"Carrusel de Instagram del número del {generar.publicacion(fecha)}")
        # La misma clave de despliegue que usa el clon del sitio (/sitio en el NAS), si lo hay
        ssh = subprocess.run(["git", "-C", os.environ.get("SITIO_REPO", "/sitio"), "config", "--get", "core.sshCommand"],
                             capture_output=True, text=True).stdout.strip()
        extra = ["-c", f"core.sshCommand={ssh}"] if ssh else []
        for intento in range(8):   # GitHub rechaza a veces la conexión (ADR 0012)
            r = subprocess.run(["git", *extra, "-C", tmp, "push", "-qf", REPO_SITIO, f"{RAMA}:{RAMA}"], capture_output=True, text=True)
            if r.returncode == 0:
                return
            time.sleep(3)
        raise RuntimeError(f"no se pudieron subir las imágenes: {r.stderr.strip()}")


def esperar_url(url, minutos=10, tipo="image/jpeg"):
    tipo = "video/mp4" if url.endswith(".mp4") and tipo == "image/jpeg" else tipo
    fin = time.time() + minutos * 60
    while time.time() < fin:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
                if r.status == 200 and r.headers.get("Content-Type", "").startswith(tipo):
                    return
        except urllib.error.URLError:
            pass
        time.sleep(15)
    raise RuntimeError(f"la imagen no está en línea: {url}")


def publicar(fecha):
    estado = RAIZ / "estado" / f"{fecha}.instagram"
    if estado.exists():
        print(f"instagram: ya publicado ({estado.read_text().strip()})")
        return
    origen = SALIDA / fecha
    jpgs = sorted(origen.glob("*.jpg"))
    if not jpgs or (origen / "NO-CABE").exists():
        raise RuntimeError(f"no hay imágenes válidas en {origen}")
    alts = json.loads((origen / "alt.json").read_text()) if (origen / "alt.json").exists() else []
    c = credenciales()
    tok, uid = c["token"], c["usuario_id"]
    # El carrusel remite al diario: sin el número en la web, no se publica
    esperar_url(f"https://diarioiaeducativa.github.io/{fecha}/", minutos=15, tipo="text/html")
    subir_rama(fecha)
    urls = [f"{URL_IMAGENES}/{fecha}/{f.name}" for f in jpgs]
    for u in urls:
        esperar_url(u)
    hijos = []
    for i, u in enumerate(urls):
        datos = {"image_url": u, "is_carousel_item": "true"}
        if i < len(alts) and alts[i]:
            datos["alt_text"] = alts[i]
        try:
            hijos.append(llamada("POST", f"{uid}/media", tok, **datos)["id"])
        except RuntimeError as err:
            if "alt_text" not in datos or "alt_text" not in str(err):
                raise
            datos.pop("alt_text")   # si la API dejara de aceptar el texto alternativo, sin él
            hijos.append(llamada("POST", f"{uid}/media", tok, **datos)["id"])
    carrusel = llamada("POST", f"{uid}/media", tok, media_type="CAROUSEL", children=",".join(hijos),
                       caption=(origen / "texto.txt").read_text())["id"]
    for _ in range(30):
        st = llamada("GET", carrusel, tok, fields="status_code").get("status_code")
        if st == "FINISHED":
            break
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram no ha aceptado el carrusel ({st})")
        time.sleep(10)
    # A partir de aquí no se reintenta nada solo: un segundo intento podría publicarlo dos veces.
    estado.write_text("en marcha\n")
    media = llamada("POST", f"{uid}/media_publish", tok, creation_id=carrusel)["id"]
    enlace = llamada("GET", media, tok, fields="permalink").get("permalink", media)
    estado.write_text(enlace + "\n")
    print(f"instagram: publicado {enlace}")


def publicar_reel(fecha):
    """«La semana en vídeo» en Instagram, como reel, con su portada y el texto del guionista."""
    estado = RAIZ / "estado" / f"{fecha}.instagram-reel"
    if estado.exists():
        print(f"instagram: reel ya publicado ({estado.read_text().strip()})")
        return
    origen = SALIDA / f"reel-{fecha}"
    if not (origen / "reel.mp4").exists():
        raise RuntimeError(f"no hay reel en {origen}")
    guion = json.loads((RAIZ / "reels" / f"{fecha}.json").read_text())
    propio = (guion.get("instagram") or "").strip()
    if not (60 <= len(propio) <= 900) or "http" in propio or "#" in propio:
        propio = "Lo más destacado de la semana en el Diario de IA Educativa."
    publica = generar.publicacion(fecha)
    pie = (f"Cada noticia, completa y con sus fuentes, en el enlace del perfil.\n\n"
           f"Vídeo y música hechos por programa a partir del diario, redactado con IA a partir de lo que se "
           f"habla en los grupos de Telegram {GRUPOS_TXT}.\n\n{ETIQUETAS}")
    texto_ig = f"La semana en vídeo · {publica[8:10].lstrip('0')}/{publica[5:7].lstrip('0')}/{publica[:4]}\n\n{propio}\n\n{pie}"
    c = credenciales()
    tok, uid = c["token"], c["usuario_id"]
    subir_rama(f"reel-{fecha}", origen)
    video, portada = (f"{URL_IMAGENES}/reel-{fecha}/{n}" for n in ("reel.mp4", "portada.jpg"))
    esperar_url(video)
    esperar_url(portada)
    cont = llamada("POST", f"{uid}/media", tok, media_type="REELS", video_url=video, cover_url=portada,
                   caption=texto_ig, share_to_feed="true")["id"]
    for _ in range(60):   # el vídeo tarda en procesarse
        st = llamada("GET", cont, tok, fields="status_code").get("status_code")
        if st == "FINISHED":
            break
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram no ha aceptado el reel ({st})")
        time.sleep(10)
    else:
        raise RuntimeError("el reel sigue procesándose al cabo de 10 minutos")
    estado.write_text("en marcha\n")
    media = llamada("POST", f"{uid}/media_publish", tok, creation_id=cont)["id"]
    enlace = llamada("GET", media, tok, fields="permalink").get("permalink", media)
    estado.write_text(enlace + "\n")
    meta = RAIZ / "videos" / f"{publica}-semana.json"
    if meta.exists():   # la web enlaza el reel desde la siguiente publicación del sitio
        m = json.loads(meta.read_text())
        m["instagram"] = enlace
        meta.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    print(f"instagram: reel publicado {enlace}")


def renovar(forzar=False):
    """Un token de usuario del sistema no caduca y no se renueva. Uno de Instagram de larga duración
    dura 60 días; se renueva si tiene más de 7 (ha de tener al menos 24 horas)."""
    c = credenciales()
    if c.get("caduca") == "nunca":
        print("instagram: el permiso no caduca; no hay nada que renovar")
        return
    hecho = datetime.datetime.fromisoformat(c.get("renovado", "2000-01-01T00:00:00+00:00"))
    ahora = datetime.datetime.now(datetime.timezone.utc)
    if not forzar and ahora - hecho < datetime.timedelta(days=7):
        print(f"instagram: permiso renovado el {hecho:%Y-%m-%d}; no toca")
        return
    url = "https://graph.instagram.com/refresh_access_token?" + urllib.parse.urlencode(
        {"grant_type": "ig_refresh_token", "access_token": c["token"]})
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            nuevo = json.loads(r.read())
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"no se pudo renovar el permiso: HTTP {err.code} {err.read().decode(errors='replace').replace(c['token'], '…')}") from None
    c["token"] = nuevo["access_token"]
    c["renovado"] = ahora.isoformat(timespec="seconds")
    c["caduca"] = (ahora + datetime.timedelta(seconds=int(nuevo.get("expires_in", 0)))).isoformat(timespec="seconds")
    guardar(c)
    print(f"instagram: permiso renovado; caduca el {c['caduca'][:10]}")


def comprobar():
    c = credenciales()
    yo = llamada("GET", c["usuario_id"], c["token"], fields="id,username")
    if yo.get("username") != c.get("usuario", yo.get("username")):
        raise RuntimeError(f"el permiso es de otra cuenta: @{yo.get('username')}")
    print(f"instagram: permiso válido para @{yo.get('username')}; caduca: {c.get('caduca', '?')[:10]}")
    lim = llamada("GET", f"{c['usuario_id']}/content_publishing_limit", c["token"], fields="quota_usage,config")
    print(f"instagram: publicaciones por la API en 24 h: {json.dumps(lim.get('data', lim), ensure_ascii=False)}")


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if orden == "imagenes" and len(sys.argv) == 3:
            imagenes(sys.argv[2])
        elif orden == "publicar" and len(sys.argv) == 3:
            publicar(sys.argv[2])
        elif orden == "reel" and len(sys.argv) == 3:
            publicar_reel(sys.argv[2])
        elif orden == "renovar":
            renovar("--ya" in sys.argv)
        elif orden == "comprobar":
            comprobar()
        else:
            sys.exit(__doc__)
    except RuntimeError as err:
        sys.exit(f"instagram: {err}")
