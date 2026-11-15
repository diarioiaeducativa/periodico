#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Que el diario no atribuya a sus autores lo que es de otra persona (ADR 0066). Sin IA.

    scripts/revisar-autoria.py --dia AAAA-MM-DD   lo escrito esa noche, en los cinco idiomas, y sus avisos
    scripts/revisar-autoria.py --todo             todo lo publicado (para medir la regla)
    scripts/revisar-autoria.py --archivos F…      solo esos archivos

El 11-11-2026 un miembro que firma «Juanjo» compartió Eduvers y el diario la atribuyó a Juan José de Haro
dos veces (la pieza, su aviso y el reportaje del 14-11). Esta comprobación busca las frases que nombran a
un autor del diario (los de ~/.config/diario-autores.json, scripts/personas.py) y avisa si en la misma
frase hay:
- un recurso (por su enlace, o por su nombre: «Eduvers» por eduvers.org) que en los grupos solo han
  compartido otras cuentas, nunca la suya. Las webs que comparte mucha gente (más de MAX_CUENTAS cuentas)
  son plataformas, no recursos de alguien, y no cuentan;
- un enlace a un mensaje de otra cuenta que firma con el mismo nombre de pila que el autor («Juanjo»).
Y avisa de la pieza que nombra a un autor y enlaza mensajes de otra cuenta con su nombre de pila, pero
ninguno suyo.
Escribe lo que encuentra, una línea por frase, y sale con 4; sin nada, con 0. Sin la lista de autores no
puede comprobar nada: lo dice y sale con 0, para no parar la noche.
"""
import json
import pathlib
import re
import sys
import urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from personas import autores  # noqa: E402

import os  # noqa: E402

DATOS = pathlib.Path(os.environ.get("DATOS_BOT", "/bot-datos"))
GRUPOS = {"chatgpt": "ChatGPTedu", "vce": "vceduca", "edumedia": "EduMediaIAG"}
SECCIONES = ("ediciones", "reportajes", "biblioteca", "hace-un-ano", "repositorio")
IDIOMAS = ("", "-ca", "-gl", "-eu", "-en")
# Lo que no se publica: notas de los agentes, la descripción para el ilustrador, la nota de corrección
INTERNOS = {"repaso", "comprobado", "correccion", "motivo", "ilustracion", "mensaje", "idea", "fuentes",
            "relacionadas", "url", "id", "fecha", "personas", "instagram", "descartado"}
MAX_CUENTAS = 5
CORRIENTE = 10   # veces que una palabra sale en minúscula en los grupos para tenerla por corriente
# Alojamientos donde cada subdominio es de alguien: la clave es el subdominio entero
COMPARTIDOS = ("github.io", "netlify.app", "vercel.app", "pages.dev", "web.app", "firebaseapp.com", "glitch.me",
               "onrender.com", "replit.app", "wordpress.com", "blogspot.com", "wixsite.com", "notion.site",
               "gitlab.io", "neocities.org", "canva.site", "my.canva.site", "hf.space")
URL = re.compile(r"https?://[^\s)\]>»\"'<]+")
TME = re.compile(r"t\.me/(ChatGPTedu|vceduca|EduMediaIAG)/(?:\d+/)?(\d+)")


def clave(u):
    """La web de un enlace: dominio (sin www), o subdominio en los alojamientos compartidos, o la cuenta en
    GitHub y Google Sites. None si no es un recurso de nadie (Telegram)."""
    try:
        p = urllib.parse.urlsplit(u.rstrip(".,;:!?"))
    except ValueError:
        return None
    host = (p.hostname or "").lower().removeprefix("www.")
    if not host or host in ("t.me", "telegram.me"):
        return None
    ruta = [x for x in p.path.split("/") if x]
    if host == "github.com" and ruta:
        return f"github.com/{ruta[0].lower()}"
    if host == "sites.google.com" and ruta:
        return "sites.google.com/" + "/".join(ruta[:2]).lower()
    if any(host == c or host.endswith("." + c) for c in COMPARTIDOS):
        return host
    partes = host.split(".")
    # el dominio que se registra: eduvers.org; para .co.uk, .com.es y parecidos, tres partes
    n = 3 if len(partes) >= 3 and partes[-2] in ("co", "com", "org", "gob", "edu", "ac", "net") else 2
    return ".".join(partes[-n:])


def nombre_de(k):
    """La palabra con que el texto puede nombrar la web («eduvers»), si es distintiva."""
    if "/" in k:
        return None
    partes = k.split(".")
    if any(k.endswith(c) for c in COMPARTIDOS):
        w = partes[0]
    else:
        w = partes[-3] if len(partes) >= 3 and partes[-2] in ("co", "com", "org", "gob", "edu", "ac", "net") else partes[-2]
    return w if len(w) >= 5 and re.fullmatch(r"[a-z][a-z0-9-]+", w) else None


def mensajes():
    """Cada mensaje por su enlace, las cuentas que han compartido cada web y cuántas veces sale cada
    palabra en minúscula fuera de los enlaces (para no tomar por nombre de una web una palabra corriente)."""
    from collections import Counter
    por_id, webs, palabras = {}, {}, Counter()
    for g, alias in GRUPOS.items():
        f = DATOS / g / "mensajes.jsonl"
        if not f.exists():
            continue
        for linea in f.open():
            try:
                m = json.loads(linea)
                i = int(m.get("autor_id"))
            except (ValueError, TypeError):
                continue
            por_id[(alias, int(m["id"]))] = m
            palabras.update(re.findall(r"\b[a-z][a-z0-9-]{4,}\b", URL.sub(" ", m.get("texto") or "")))
            urls = URL.findall(m.get("texto") or "") + [(m.get("web") or {}).get("url") or ""]
            for u in urls:
                k = clave(u) if u else None
                if k:
                    webs.setdefault(k, set()).add(i)
    return por_id, webs, palabras


def textos(o, ruta=""):
    """(ruta, texto) de lo que se publica de un JSON."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in INTERNOS:
                yield from textos(v, f"{ruta}.{k}" if ruta else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from textos(v, f"{ruta}[{i}]")
    elif isinstance(o, str) and len(o) > 3:
        yield ruta, o


def frases(t):
    return [f for f in re.split(r"(?<=[.!?])\s+(?=[«“¿¡\"(\[A-ZÁÉÍÓÚÀÈÒÇÑ])", t) if f.strip()]


MD = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
CERCA = 45   # caracteres entre el recurso y el nombre del autor, sin enlaces


def llano(fr):
    """La frase sin enlaces, y dónde quedó el texto de cada enlace: [(inicio, fin, url)]."""
    out, enlaces, i = "", [], 0
    for m in MD.finditer(fr):
        out += URL.sub("", fr[i:m.start()])
        enlaces.append((len(out), len(out) + len(m.group(1)), m.group(2)))
        out += m.group(1)
        i = m.end()
    return out + URL.sub("", fr[i:]), enlaces


def junto(texto, a, b, nombres):
    """Si el tramo entre dos posiciones es corto y no nombra a nadie más (una palabra con mayúscula que no
    sea del propio autor)."""
    tramo = texto[min(a[1], b[1]):max(a[0], b[0])] if a[0] != b[0] else ""
    if len(tramo) > CERCA:
        return False
    propias = {w for n in nombres for w in n.split()}
    return not any(w[0].isupper() and w not in propias for w in re.findall(r"[\wÀ-ÿ'-]+", tramo) if len(w) > 2)


def revisar(f, aut, por_id, webs, nombres_web):
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError):
        return []
    hallado = []
    for ruta, t in textos(d):
        for fr in frases(t):
            nombrados = {i for i, a in aut.items() if any(n in fr for n in [a["nombre"]] + list(a.get("en_grupos", [])))}
            if not nombrados:
                continue
            plano_, enlaces = llano(fr)
            # Los recursos de la frase: el texto de cada enlace (con su web) y los nombres propios de una web
            recursos = []
            for ini, fin, u in enlaces:
                k = clave(u)
                if k and k in webs:
                    recursos.append(((ini, fin), k, k))
            for m in re.finditer(r"[\wÀ-ÿ-]+", plano_):
                w = m.group(0)
                if not w[:1].isupper():
                    continue   # un nombre propio: «Eduvers», no «diario» (diario.red)
                wl = w.lower()
                # con algún sufijo corto pegado: «Eduversen», en euskera
                k = nombres_web.get(wl) or next((nombres_web[x] for x in nombres_web
                                                 if wl.startswith(x) and len(wl) - len(x) <= 3), None)
                if k:
                    recursos.append(((m.start(), m.end()), k, f"«{w}» ({k})"))
            for i in nombrados:
                a = aut[i]
                nombres = [a["nombre"]] + list(a.get("en_grupos", []))
                pila = {n.split()[0] for n in nombres if n.split()}
                lugares = [(m.start(), m.end()) for n in nombres for m in re.finditer(re.escape(n), plano_)]
                motivos = set()
                for pos, k, dicho in recursos:
                    quien = webs[k]
                    if len(quien) > MAX_CUENTAS or i in quien or quien & nombrados:
                        continue   # una plataforma, o suya, o de otro autor que la frase también nombra
                    if any(pos[0] < l[1] and l[0] < pos[1] for l in lugares):
                        continue   # el enlace es el propio nombre del autor
                    if any(junto(plano_, pos, l, nombres) for l in lugares):
                        motivos.add(f"{dicho} solo la han compartido en los grupos otras cuentas")
                for alias, mid in TME.findall(fr):
                    m = por_id.get((alias, int(mid)))
                    if not m or int(m["autor_id"]) == i:
                        continue
                    visible = (m.get("autor") or "").strip()
                    if visible.split() and visible.split()[0] in pila:
                        motivos.add(f"el mensaje {alias}/{mid} es de otra cuenta que firma «{visible}»")
                for mo in sorted(motivos):
                    hallado.append(f"{f.relative_to(RAIZ) if f.is_relative_to(RAIZ) else f} · {ruta} · atribuye a {a['nombre']}: {mo} · «{fr.strip()[:300]}»")
    return hallado


def piezas(o):
    """Cada pieza de un JSON (lo que tiene titular), entera."""
    if isinstance(o, dict):
        if o.get("titular"):
            yield o
            return
        for v in o.values():
            yield from piezas(v)
    elif isinstance(o, list):
        for v in o:
            yield from piezas(v)


def revisar_piezas(f, aut, por_id):
    """Una pieza que nombra a un autor y cuyos mensajes enlazados son de otra cuenta con su mismo nombre de
    pila, sin ninguno suyo: «Su autor, Juan José de Haro…» sobre lo que compartió otro «Juanjo»."""
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError):
        return []
    hallado = []
    for p in piezas(d):
        publicado = " ".join(t for _, t in textos(p))
        todo = json.dumps(p, ensure_ascii=False)
        enlazados = [por_id.get((al, int(mid))) for al, mid in TME.findall(todo)]
        enlazados = [m for m in enlazados if m]
        for i, a in aut.items():
            nombres = [a["nombre"]] + list(a.get("en_grupos", []))
            if not any(n in publicado for n in nombres) or any(int(m["autor_id"]) == i for m in enlazados):
                continue
            pila = {n.split()[0] for n in nombres if n.split()}
            otros = sorted({(m.get("autor") or "").strip() for m in enlazados
                            if (m.get("autor") or "").split() and (m.get("autor") or "").split()[0] in pila})
            if otros:
                hallado.append(f"{f.relative_to(RAIZ) if f.is_relative_to(RAIZ) else f} · «{p['titular'][:120]}» · "
                               f"nombra a {a['nombre']}, pero sus mensajes enlazados son de otra cuenta que firma "
                               f"«{', '.join(otros)}» y ninguno suyo")
    return hallado


def archivos(fecha):
    out = [RAIZ / f"{s}{c}" / f"{fecha}.json" for s in SECCIONES for c in IDIOMAS]
    if fecha:
        import datetime
        sig = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
        out.append(RAIZ / "avisos" / f"{sig}.json")
    return [f for f in out if f.exists()]


def main():
    aut = autores()
    if not aut:
        print("revisar-autoria: sin la lista de autores del diario (~/.config/diario-autores.json), no se comprueba nada")
        return 0
    por_id, webs, palabras = mensajes()
    nombres_web = {}
    for k in webs:
        w = nombre_de(k)
        if w and palabras[w] <= CORRIENTE:   # «diario» (diario.red) es una palabra, no el nombre de una web
            nombres_web.setdefault(w, k)
    if "--todo" in sys.argv:
        fs = sorted(f for s in SECCIONES for c in IDIOMAS for f in (RAIZ / f"{s}{c}").glob("20*.json"))
        fs += sorted((RAIZ / "avisos").glob("20*.json"))
    elif "--archivos" in sys.argv:
        fs = [pathlib.Path(x).resolve() for x in sys.argv[sys.argv.index("--archivos") + 1:]]
    else:
        fs = archivos(sys.argv[sys.argv.index("--dia") + 1])
    hallado = [h for f in fs for h in revisar(f, aut, por_id, webs, nombres_web) + revisar_piezas(f, aut, por_id)]
    print("\n".join(hallado) if hallado else f"revisar-autoria: nada que atribuya a los autores lo de otra cuenta ({len(fs)} archivos)")
    return 4 if hallado else 0


if __name__ == "__main__":
    sys.exit(main())
