#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""«La semana en vídeo» (ADR 0016): el reel del domingo con lo más destacado de la semana.

    scripts/reel-semana.py AAAA-MM-DD [--prueba]

AAAA-MM-DD es la fecha de las conversaciones del sábado, la del número que sale el domingo. Lee el
guion que escribe el agente (reels/<fecha>.json: como mínimo una pieza de cada número de la semana y
como mucho MAX_PIEZAS, con su golpe, su titular corto y su dato, en castellano y catalán, y el texto
para Instagram) y hace, sin IA, un vídeo con las piezas en orden y el día en que salió cada una:

- videos/<domingo>-semana-<es|ca>.mp4 (720 × 1280) y su portada .jpg, para la web, y
  videos/<domingo>-semana.json con lo que dice en pantalla y el estilo de la música;
- instagram/reel-<fecha>/reel.mp4 (1080 × 1920) y portada.jpg, para Instagram (no se guardan
  en el repositorio).

Página animada → fotogramas con Chromium de Playwright → MP4 con ffmpeg; música de
scripts/musica.py con un estilo que no se ha usado antes. Si un texto no cabe, sale con 2 y no
hay reel esa semana. Con --prueba, solo unas capturas en /tmp para mirarlas.
"""
import datetime
import html
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))
import generar  # noqa: E402
import musica  # noqa: E402
import vineta  # noqa: E402

FPS = 30
ANCHO, ALTO = 1080, 1920
C_INTRO, C_NOT, C_CIERRE = 2, 3, 2
MAX_PIEZAS = 10    # una por número de la semana (7) y hasta tres más de los días con más (05-11-2026)
e = html.escape
TXT = {
    "es": {"la": "la", "semana": "semana", "sub": "Lo más destacado del Diario de IA Educativa",
           "todo": "Cada noticia, completa y con sus fuentes", "hora": "Cada mañana a las 7:00",
           "titulo": "La semana en vídeo", "del": "Del {a} al {b}"},
    "ca": {"la": "la", "semana": "setmana", "sub": "El més destacat del Diari d'IA Educativa",
           "todo": "Cada notícia, completa i amb les fonts", "hora": "Cada matí a les 7:00",
           "titulo": "La setmana en vídeo", "del": "Del {a} al {b}"},
}


def _og():
    spec = importlib.util.spec_from_file_location("og_numero", RAIZ / "scripts" / "og-numero.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def palabras(texto):
    return " ".join(f'<span class="w"><span>{e(p)}</span></span>' for p in texto.split())


def pareja():
    t, _ = vineta.tiza(150, "derecha", "riendo", "arriba")
    a, _ = vineta.algoritmo(250, "izquierda", "contento", "arriba")
    return f'<svg viewBox="40 150 320 200" xmlns="http://www.w3.org/2000/svg">{t}{a}</svg>'


def etiqueta_semana(publica, codigo):
    """Los números de lunes a domingo: «2 – 8 nov 2026»."""
    fin = datetime.date.fromisoformat(publica)
    ini = fin - datetime.timedelta(days=6)
    meses = generar.IDIOMAS[codigo]["meses"]
    m = lambda d: meses[d.month - 1][:3]  # noqa: E731
    if ini.month == fin.month:
        return f"{ini.day} – {fin.day} {m(fin)} {fin.year}"
    return f"{ini.day} {m(ini)} – {fin.day} {m(fin)} {fin.year}"


def dia_de(fecha, codigo):
    """El día en que salió el número de esas conversaciones, como lo ve el lector: «Lunes 2»."""
    d = datetime.date.fromisoformat(generar.publicacion(fecha))
    return f'{generar.IDIOMAS[codigo]["dias"][d.weekday()].capitalize()} {d.day}'


def pagina(codigo, guion, piezas, estilo, semana):
    generar.L = generar.IDIOMAS[codigo]
    L, T = generar.L, TXT[codigo]
    og = _og()
    compas = musica.compas_seg(estilo)
    n = len(piezas)
    total = (C_INTRO + n * C_NOT + C_CIERRE) * compas + 1.5
    est = (RAIZ / "estaticos").as_uri()
    secciones = ["herramientas", "vibecoding", "multimedia", "debates", "novedades", "biblioteca"]
    franjas = "".join(f'<i class="sec-{c}"></i>' for c in secciones)
    bloques = []
    for k, (g, (d, p)) in enumerate(zip(guion["noticias"], piezas)):
        grupo = generar.GRUPOS.get(p.get("grupo"), (p.get("grupo") or "",))[0]
        bloques.append(f"""<section class="noticia sec-{e(p.get("seccion") or "")}" id="n{k}">
  <div class="banda"></div>
  <div class="cab"><span class="chip">{generar.icono(p.get("seccion"))} {e(L["secciones"].get(p.get("seccion"), ""))}</span><span class="grupo"><b class="dia">{e(dia_de(d["fecha"], codigo))}</b><span class="g-nombre"> · {e(grupo)}</span></span></div>
  <h2 class="golpe">{palabras(g["golpe"][codigo])}</h2>
  <p class="titular-v">{palabras(g["titular"][codigo])}</p>
  <figure class="ilu tarjeta">{og.dibujo(d, p)}</figure>
  <p class="dato">{e(g["dato"][codigo])}</p>
</section>""")
    letras = "".join(f'<span class="l">{c}</span>' for c in T["semana"])
    return total, f"""<!doctype html><html lang="{codigo}" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="{est}/fuentes.css"><link rel="stylesheet" href="{est}/comun.css"><link rel="stylesheet" href="{est}/diario.css">
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;width:{ANCHO}px;height:{ALTO}px;overflow:hidden;background:var(--papel);color:var(--tinta);font-family:Newsreader,Georgia,serif}}
.w{{display:inline-block;overflow:hidden;vertical-align:top;padding:.16em 0 .08em;margin:-.16em 0 -.08em}}
.w>span{{display:inline-block}}
.hud{{position:absolute;z-index:5;left:64px;right:64px;top:58px;display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.barras{{position:absolute;z-index:5;left:64px;right:64px;top:112px;display:flex;gap:10px}}
.barras b{{flex:1;height:6px;background:currentColor;opacity:.25;position:relative;overflow:hidden}}
.barras b i{{position:absolute;inset:0;background:currentColor;opacity:1;transform-origin:left;transform:scaleX(0)}}
.intro{{position:absolute;inset:0}}
.franjas{{position:absolute;left:0;right:0;top:300px;height:300px;display:flex;flex-direction:column}}
.franjas i{{flex:1;background:var(--sec);transform-origin:left;transform:scaleX(0)}}
.la{{position:absolute;left:64px;top:660px;font-size:120px;font-weight:800;font-style:italic;color:var(--tinta-2);margin:0}}
.semana-g{{position:absolute;left:52px;right:0;top:760px;font-size:240px;line-height:.9;font-weight:800;letter-spacing:-.04em;margin:0;font-variation-settings:"opsz" 72;white-space:nowrap}}
.semana-g .l{{display:inline-block}}
.sub-intro{{position:absolute;left:64px;right:150px;top:1080px;font-size:56px;line-height:1.15;margin:0}}
.fecha-intro{{position:absolute;left:64px;top:1300px;display:inline-block;padding:12px 26px;background:var(--tinta);color:var(--papel);font-size:40px;font-weight:700;letter-spacing:.06em}}
.noticia{{position:absolute;inset:0;visibility:hidden}}
.banda{{position:absolute;inset:0;background:var(--sec);clip-path:inset(100% 0 0 0)}}
.cab{{position:absolute;left:64px;right:150px;top:190px;display:flex;align-items:center;gap:24px;color:#fff}}
.chip{{display:inline-flex;align-items:center;gap:12px;padding:10px 24px 10px 18px;background:rgba(255,255,255,.18);border:2px solid rgba(255,255,255,.7);font-size:32px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}}
.chip .ico{{width:36px;height:36px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.grupo{{font-size:34px;font-style:italic;white-space:nowrap}}
.grupo .dia{{font-style:normal;font-weight:800;letter-spacing:.02em}}
.golpe{{position:absolute;left:64px;right:150px;top:300px;margin:0;color:#fff;font-size:150px;line-height:.92;font-weight:800;letter-spacing:-.03em;text-transform:uppercase;transform-origin:left top;font-variation-settings:"opsz" 72}}
.titular-v{{position:absolute;left:64px;right:150px;top:760px;margin:0;font-size:80px;line-height:1.04;font-weight:800;letter-spacing:-.015em;text-wrap:balance;font-variation-settings:"opsz" 72}}
.tarjeta{{position:absolute;left:90px;right:170px;top:1040px;height:440px;margin:0;padding:24px;background:var(--sec-tinte,var(--papel-2));border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.tarjeta svg,.tarjeta img{{display:block;max-width:100%;max-height:100%;width:auto;height:100%}}
.tarjeta svg.ico{{width:40%;height:auto;color:var(--sec)}}
.dato{{position:absolute;left:64px;right:150px;top:1530px;margin:0;padding-left:26px;border-left:10px solid var(--sec);font-size:46px;line-height:1.2;font-weight:600}}
.cierre{{position:absolute;inset:0;visibility:hidden;text-align:center}}
.cierre .personajes{{position:absolute;left:50%;top:330px;width:560px;margin:0 0 0 -280px;padding:0;border:0}}
.cierre .personajes svg{{width:100%;height:auto}}
.cierre .todo{{position:absolute;left:100px;right:100px;top:880px;margin:0;font-size:72px;font-weight:800;line-height:1.05;letter-spacing:-.02em}}
.cierre .url{{position:absolute;left:0;right:0;top:1130px;margin:0;font-size:64px;font-weight:800;color:var(--azul)}}
.cierre .hora{{position:absolute;left:0;right:0;top:1250px;margin:0;font-size:44px;font-style:italic;color:var(--tinta-2)}}
.cierre .franjas{{top:1420px;height:120px}}
</style></head><body>
<div class="hud" id="hud"><span>{e(L["titulo"])}</span><span>{e(T["titulo"].split(" en ")[0])}</span></div>
<div class="barras" id="barras">{"".join("<b><i></i></b>" for _ in range(n))}</div>
<section class="intro" id="intro">
  <div class="franjas">{franjas}</div>
  <p class="la">{e(T["la"])}</p>
  <h1 class="semana-g">{letras}</h1>
  <p class="sub-intro">{palabras(T["sub"])}</p>
  <p class="fecha-intro">{e(semana)}</p>
</section>
{"".join(bloques)}
<section class="cierre" id="cierre">
  <div class="vineta personajes">{pareja()}</div>
  <p class="todo">{palabras(T["todo"])}</p>
  <p class="url">diarioiaeducativa.github.io</p>
  <p class="hora">{e(T["hora"])}</p>
  <div class="franjas">{franjas}</div>
</section>
<script>
window.desbordes = [];
function montar() {{
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
// Cada texto, lo más grande que quepa en su sitio; lo que no quepa ni al mínimo, se apunta
const ajusta = (el, max, min, cabe) => {{ let fs = max; el.style.fontSize = fs + 'px';
  while (!cabe() && fs > min) {{ fs -= 2; el.style.fontSize = fs + 'px'; }} if (!cabe()) window.desbordes.push(el.className + ': ' + el.textContent.trim().slice(0, 40)); }};
const anchos = el => [...el.querySelectorAll('.w')].every(w => w.getBoundingClientRect().right <= el.getBoundingClientRect().right + 1);
$$('.noticia').forEach(n => {{ n.style.visibility = 'visible';
  const g = $('.golpe', n), t = $('.titular-v', n), d = $('.dato', n), c = $('.cab', n);
  ajusta(g, 150, 70, () => anchos(g) && g.offsetHeight <= parseFloat(g.style.fontSize) * 1.95);
  ajusta(t, 80, 50, () => anchos(t) && t.offsetTop + t.offsetHeight <= 1010);
  ajusta(d, 46, 32, () => d.offsetTop + d.offsetHeight <= 1700);
  // Si la cabecera no cabe, se queda el día y se quita el nombre del grupo
  if (c.scrollWidth > c.clientWidth + 1) {{ const gn = $('.g-nombre', n); if (gn) gn.remove(); }}
  if (c.scrollWidth > c.clientWidth + 1) window.desbordes.push('cabecera: ' + c.textContent.trim());
  n.style.visibility = ''; }});
const sg = $('.semana-g'); if (sg.scrollWidth > {ANCHO} - 52) {{ let fs = 240; while (sg.scrollWidth > {ANCHO} - 80 && fs > 150) {{ fs -= 6; sg.style.fontSize = fs + 'px'; }} }}
const C = {compas}, P = C / 4, N = {n}, I0 = {C_INTRO} * C, D = {C_NOT} * C, F0 = I0 + N * D, TOTAL = {total};
const EZ = 'cubic-bezier(.16,1,.3,1)', REB = 'cubic-bezier(.34,1.56,.64,1)';
const a = (el, kf, t, d, o = {{}}) => el.animate(kf, {{delay: t * 1000, duration: d * 1000, fill: o.fill || 'both', easing: o.ease || EZ}});
const sale = (el, kf, t, d, ease) => a(el, kf, t, d, {{fill: 'forwards', ease: ease || 'cubic-bezier(.7,0,.84,0)'}});
const muestra = (el, t0, t1) => a(el, [{{visibility: 'visible'}}, {{visibility: 'visible'}}], t0, t1 - t0, {{fill: 'none'}});
[$('#hud'), $('#barras')].forEach(h => {{ a(h, [{{color: 'var(--tinta)'}}, {{color: '#fff'}}], I0, .25); sale(h, [{{color: '#fff'}}, {{color: 'var(--tinta)'}}], F0, .25, 'linear'); }});
$$('#barras i').forEach((b, k) => a(b, [{{transform: 'scaleX(0)'}}, {{transform: 'scaleX(1)'}}], I0 + k * D, D, {{ease: 'linear'}}));
const intro = $('#intro');
$$('.franjas i', intro).forEach((f, k) => {{ a(f, [{{transform: 'scaleX(0)'}}, {{transform: 'scaleX(1)'}}], .05 + k * .07, .5);
  sale(f, [{{transform: 'scaleX(1)', transformOrigin: 'right'}}, {{transform: 'scaleX(0)', transformOrigin: 'right'}}], I0 - 1.4 + k * .05, .45); }});
a($('.la'), [{{opacity: 0, transform: 'translateX(-60px)'}}, {{opacity: 1, transform: 'none'}}], .45, .4);
$$('.semana-g .l').forEach((l, k) => a(l, [{{opacity: 0, transform: 'translateY(60px) scale(1.5)', filter: 'blur(14px)'}}, {{opacity: 1, transform: 'none', filter: 'blur(0)'}}], .6 + k * P / 2, .45, {{ease: REB}}));
$$('.sub-intro .w>span').forEach((w, k) => a(w, [{{transform: 'translateY(110%)'}}, {{transform: 'none'}}], I0 * .48 + k * .05, .5));
a($('.fecha-intro'), [{{clipPath: 'inset(0 100% 0 0)'}}, {{clipPath: 'inset(0 0 0 0)'}}], I0 * .62, .45);
sale(intro, [{{transform: 'none', opacity: 1}}, {{transform: 'scale(1.25)', opacity: 0}}], I0 - .3, .3);
$$('.noticia').forEach((n, k) => {{
  const S = I0 + k * D, fin = S + D, q = s => $(s, n), qq = s => $$(s, n);
  muestra(n, S, fin + .2);
  a(q('.banda'), [{{clipPath: 'inset(100% 0 0 0)'}}, {{clipPath: 'inset(0 0 0 0)'}}], S, .35);
  sale(q('.banda'), [{{clipPath: 'inset(0 0 0 0)'}}, {{clipPath: 'inset(0 0 63% 0)'}}], S + 2 * P, .5, EZ);
  a(q('.cab'), [{{opacity: 0, transform: 'translateY(-30px)'}}, {{opacity: 1, transform: 'none'}}], S + .15, .4);
  a(q('.golpe'), [{{transform: 'translateY(380px)'}}, {{transform: 'translateY(380px)'}}], S, .01);
  qq('.golpe .w>span').forEach((w, i) => a(w, [{{transform: 'translateY(105%) rotate(4deg)'}}, {{transform: 'none'}}], S + .2 + i * .07, .5));
  sale(q('.golpe'), [{{transform: 'translateY(380px) scale(1)'}}, {{transform: 'translateY(0) scale(.62)'}}], S + 2 * P, .55, EZ);
  qq('.titular-v .w>span').forEach((w, i) => a(w, [{{transform: 'translateY(110%)'}}, {{transform: 'none'}}], S + 2 * P + .25 + i * .045, .5));
  a(q('.tarjeta'), [{{opacity: 0, transform: 'translateY(120px) scale(.86) rotate(-2deg)'}}, {{opacity: 1, transform: 'none'}}], S + 4 * P, .7, {{ease: REB}});
  qq('.tarjeta .t, .tarjeta .a, .tarjeta .r').forEach((p, i) => {{ if (!p.getTotalLength) return; p.setAttribute('pathLength', 1); p.style.strokeDasharray = 1;
    a(p, [{{strokeDashoffset: 1}}, {{strokeDashoffset: 0}}], S + 4 * P + .2 + i * .03, 1.1, {{ease: 'ease-in-out'}}); }});
  qq('.tarjeta [class^=f], .tarjeta text').forEach(p => a(p, [{{opacity: 0}}, {{opacity: 1}}], S + 4 * P + .9, .5));
  a(q('.tarjeta > *'), [{{transform: 'scale(1)'}}, {{transform: 'scale(1.06)'}}], S + 4 * P + .5, D - 4 * P - .5, {{ease: 'linear'}});
  a(q('.dato'), [{{opacity: 0, transform: 'translateX(-80px)', clipPath: 'inset(0 100% 0 0)'}}, {{opacity: 1, transform: 'none', clipPath: 'inset(0 0 0 0)'}}], S + 5 * P, .6);
  for (let b = 8; b < 12; b++) a(q('.tarjeta'), [{{transform: 'scale(1.015)'}}, {{transform: 'scale(1)'}}], S + b * P, P * .9, {{fill: 'none', ease: 'ease-out'}});
  if (k < N - 1) sale(n, [{{transform: 'none'}}, {{transform: 'translateY(-140px)'}}], fin - .25, .3);
}});
const ci = $('#cierre');
muestra(ci, F0, TOTAL + 1);
a(ci, [{{clipPath: 'circle(0% at 50% 50%)'}}, {{clipPath: 'circle(150% at 50% 50%)'}}], F0, .5);
a($('.personajes', ci), [{{opacity: 0, transform: 'translateY(160px) scale(.7)'}}, {{opacity: 1, transform: 'none'}}], F0 + .3, .8, {{ease: REB}});
$$('.todo .w>span', ci).forEach((w, k) => a(w, [{{transform: 'translateY(110%)'}}, {{transform: 'none'}}], F0 + .7 + k * .05, .5));
a($('.url', ci), [{{opacity: 0, transform: 'scale(.8)'}}, {{opacity: 1, transform: 'none'}}], F0 + 1.4, .6, {{ease: REB}});
a($('.hora', ci), [{{opacity: 0}}, {{opacity: 1}}], F0 + 2, .5);
$$('.franjas i', ci).forEach((f, k) => a(f, [{{transform: 'scaleX(0)'}}, {{transform: 'scaleX(1)'}}], F0 + 1.6 + k * .07, .5));
sale(document.body, [{{opacity: 1}}, {{opacity: 0}}], TOTAL - .6, .6, 'linear');
document.getAnimations().forEach(x => x.pause());
window.irA = s => document.getAnimations().forEach(x => x.currentTime = s * 1000);
}}
document.fonts.ready.then(montar);
</script></body></html>"""


def validar(guion, eds, fecha):
    """Un resumen de verdad: al menos una pieza de cada número de la semana, en orden de días."""
    desde = (datetime.date.fromisoformat(fecha) - datetime.timedelta(days=6)).isoformat()
    dias = sorted({d["fecha"] for d in eds if desde <= d["fecha"] <= fecha and d["piezas"]})
    noticias = guion.get("noticias", [])
    if not len(dias) <= len(noticias) <= MAX_PIEZAS:
        raise ValueError(f"el guion ha de tener de {len(dias)} a {MAX_PIEZAS} noticias: una por número de la semana como mínimo")
    faltan = [x for x in dias if x not in {g.get("fecha") for g in noticias}]
    if faltan:
        raise ValueError("falta una pieza de cada uno de estos números: " + ", ".join(faltan))
    noticias.sort(key=lambda g: g.get("fecha", ""))   # en orden de días; dentro de un día, como las eligió
    por_id = {(d["fecha"], p["id"]): (d, p) for d in eds for p in d["piezas"]}
    piezas = []
    for g in guion["noticias"]:
        dp = por_id.get((g.get("fecha"), g.get("id")))
        if not dp:
            raise ValueError(f'no existe la pieza {g.get("fecha")}/{g.get("id")}')
        for campo in ("golpe", "titular", "dato"):
            for c in ("es", "ca"):
                if not (g.get(campo) or {}).get(c, "").strip():
                    raise ValueError(f'falta {campo}.{c} en {g["id"]}')
        piezas.append(dp)
    return piezas


def estilos_usados():
    usados = [musica.PRIMERO]
    for f in sorted((RAIZ / "videos").glob("*.json")):
        x = json.loads(f.read_text()).get("estilo")
        if x:
            usados.append(x)
    return usados


def main():
    fecha = sys.argv[1]
    prueba = "--prueba" in sys.argv
    publica = generar.publicacion(fecha)
    generar.L = generar.IDIOMAS["es"]
    eds = generar.cargar()
    guion = json.loads((RAIZ / "reels" / f"{fecha}.json").read_text())
    piezas = validar(guion, eds, fecha)
    vid = f"{publica}-semana"
    previo = RAIZ / "videos" / f"{vid}.json"
    estilo = json.loads(previo.read_text())["estilo"] if previo.exists() else \
        musica.elegir(estilos_usados(), int(fecha.replace("-", "")))
    from playwright.sync_api import sync_playwright
    resultados = {}
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        tmp = pathlib.Path(tmp)
        nav = pw.chromium.launch()
        for codigo in ("es", "ca"):
            semana = etiqueta_semana(publica, codigo)
            total, h = pagina(codigo, guion, piezas, estilo, semana)
            f = tmp / f"{codigo}.html"
            f.write_text(h)
            pag = nav.new_page(viewport={"width": ANCHO, "height": ALTO})
            pag.goto(f.as_uri())
            pag.wait_for_function("window.irA !== undefined")
            malos = pag.evaluate("window.desbordes")
            if malos:
                print(f"reel-semana: no cabe ({codigo}): {malos}", file=sys.stderr)
                sys.exit(2)
            compas = musica.compas_seg(estilo)
            n = len(piezas)
            i0, d = C_INTRO * compas, C_NOT * compas
            if prueba:
                for s in [i0 - .6] + [i0 + k * d + d - .3 for k in range(n)] + [total - 1.2]:
                    pag.evaluate(f"irA({s})")
                    pag.screenshot(path=f"/tmp/reel-{codigo}-{s:05.2f}.jpg", type="jpeg", quality=80)
                pag.close()
                continue
            fot = tmp / f"fot-{codigo}"
            fot.mkdir()
            for k in range(int(total * FPS)):
                pag.evaluate(f"irA({k / FPS})")
                pag.screenshot(path=str(fot / f"{k:05d}.jpg"), type="jpeg", quality=90)
            pag.close()
            resultados[codigo] = (fot, total, i0)
        nav.close()
        if prueba:
            print("reel-semana: capturas en /tmp/reel-*.jpg; estilo", json.dumps(estilo, ensure_ascii=False))
            return
        n = len(piezas)
        wav = tmp / "musica.wav"
        musica.componer(wav, C_INTRO, n, C_NOT, C_CIERRE, estilo)
        (RAIZ / "videos").mkdir(exist_ok=True)
        ig = RAIZ / "instagram" / f"reel-{fecha}"
        if ig.exists():
            shutil.rmtree(ig)
        ig.mkdir(parents=True)
        audio = ["-af", "volume=-3dB,loudnorm=I=-14:TP=-3:LRA=11", "-ar", "48000", "-c:a", "aac", "-cutoff", "20000"]
        for codigo, (fot, total, i0) in resultados.items():
            entrada = ["-framerate", str(FPS), "-i", str(fot / "%05d.jpg"), "-i", str(wav)]
            if codigo == "es":   # Instagram: 1080 × 1920
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrada, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                                "-preset", "medium", "-crf", "20", *audio, "-b:a", "256k", "-shortest", "-movflags", "+faststart",
                                str(ig / "reel.mp4")], check=True)
                shutil.copy(fot / f"{int((i0 - .6) * FPS):05d}.jpg", ig / "portada.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrada, "-vf", "scale=720:-2", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "28", *audio, "-b:a", "96k", "-shortest",
                            "-movflags", "+faststart", str(RAIZ / "videos" / f"{vid}-{codigo}.mp4")], check=True)
            # La portada en la web: la primera noticia ya montada, con su color y su dibujo
            cartel = fot / f"{int((i0 + C_NOT * musica.compas_seg(estilo) - .4) * FPS):05d}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(cartel),
                            "-vf", "scale=720:-2", "-q:v", "4", str(RAIZ / "videos" / f"{vid}-{codigo}.jpg")], check=True)
    meta = {
        "id": vid, "tipo": "semana", "publicado": publica, "dia": fecha, "duracion": round(total),
        "titulo": {c: f'{TXT[c]["titulo"]}: {etiqueta_semana(publica, c)}' for c in ("es", "ca")},
        "descripcion": guion.get("descripcion") or {c: TXT[c]["sub"] for c in ("es", "ca")},
        "pantalla": {c: [f'{TXT[c]["la"].capitalize()} {TXT[c]["semana"]}. {TXT[c]["sub"]}. {etiqueta_semana(publica, c)}.']
                     + [f'{dia_de(g["fecha"], c)}. {g["golpe"][c]}. {g["titular"][c]}. {g["dato"][c]}' for g in guion["noticias"]]
                     + [f'{TXT[c]["todo"]}. diarioiaeducativa.github.io. {TXT[c]["hora"]}.'] for c in ("es", "ca")},
        "archivos": {c: {"video": f"{vid}-{c}.mp4", "poster": f"{vid}-{c}.jpg"} for c in ("es", "ca")},
        "piezas": [{"fecha": g["fecha"], "id": g["id"]} for g in guion["noticias"]],
        "estilo": estilo,
    }
    if previo.exists():   # el enlace de Instagram, si ya se publicó, se conserva
        viejo = json.loads(previo.read_text())
        if viejo.get("instagram"):
            meta["instagram"] = viejo["instagram"]
    previo.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(f"reel-semana: {vid} ({round(total)} s, {estilo['tempo']} ppm, {estilo['tonica']} {estilo['modo']}, {estilo['progresion']})")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError) as err:
        sys.exit(f"reel-semana: {err}")
