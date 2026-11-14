#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El buscador de lo publicado, para los agentes (ADR 0061): lo que el buscador de la web es para el lector.

    python3 scripts/buscar.py PALABRAS…                 piezas que tienen todas las palabras
    python3 scripts/buscar.py --alguna PALABRAS…        piezas con alguna, las que más tienen primero
    python3 scripts/buscar.py --parecidas "TEXTO"       piezas que tratan de lo mismo que un texto
    python3 scripts/buscar.py --desde AAAA-MM-DD …      solo lo publicado desde esa fecha de clave
    python3 scripts/buscar.py --max N …                 cuántos resultados (15 por omisión)

Los agentes no tienen consola: lo usan como herramienta propia, `mcp__diario__buscar`, que da
`scripts/buscar-mcp.py` (ADR 0061).

Busca en el texto entero de todo lo publicado en castellano: las piezas y los breves de cada número, la
Biblioteca, el Repositorio, los reportajes y «Hace un año». No distingue tildes ni mayúsculas y compara
raíces, así que «aplicación» encuentra «aplicaciones» y «publicó» encuentra «publica». Si una palabra no
sale en nada, prueba con las parecidas («Vilella» → «Vilela») y lo dice. Cada resultado lleva la clave
para enlazarlo (`pieza:AAAA-MM-DD/id`), la fecha en que lo vio el lector y los trozos donde aparece.

No necesita índice: lo construye en memoria en cada consulta (SQLite FTS5, en la biblioteca estándar).
Las raíces, con el algoritmo de Snowball para el castellano (`snowballstemmer`); sin él, quita las
terminaciones más comunes.
"""
import argparse
import datetime
import difflib
import json
import pathlib
import re
import sqlite3
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre")
# Palabras que no distinguen una pieza de otra: no cuentan al buscar parecidas
VACIAS = set("""a al algo algun alguna algunas alguno algunos ante antes aqui asi aun aunque bajo bien cada como con contra
cual cuales cuando de del desde donde dos e el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estan
estar estas este esto estos fue fueron ha habia han hasta hay la las le les lo los mas me mi mientras mismo mucho muy nada
ni no nos o otra otras otro otros para pero poco por porque puede pueden que quien se segun ser si sin sobre solo son su sus
tambien tan tanto te tiene tienen todo todos tras tu un una unas uno unos y ya diario grupo grupos pieza""".split())

try:
    import snowballstemmer
    _snow = snowballstemmer.stemmer("spanish")
    def _raiz(p):
        return _snow.stemWord(p)
except ImportError:   # sin la biblioteca, una aproximación: quita plurales, género y terminaciones frecuentes
    _FINALES = ("aciones", "uciones", "imientos", "amientos", "mente", "acion", "ucion", "imiento", "amiento",
                "idades", "idad", "istas", "ista", "ables", "ibles", "able", "ible", "aron", "ieron", "aban",
                "ando", "iendo", "ados", "idos", "adas", "idas", "ado", "ido", "ada", "ida", "ar", "er", "ir",
                "es", "as", "os", "a", "o", "e", "s")
    def _raiz(p):
        for f in _FINALES:
            if p.endswith(f) and len(p) - len(f) >= 3:
                return p[:-len(f)]
        return p


def plano(t):
    """Sin tildes ni mayúsculas (la ñ queda como n, igual en el texto y en la consulta)."""
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def palabras(t):
    return re.findall(r"[a-z0-9]+", plano(t))


def raices(t):
    return [_raiz(p) for p in palabras(t)]


def sin_marcas(t):
    """Quita el Markdown de los enlaces: queda el texto, y la dirección aparte (también se busca en ella)."""
    return re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1 (\2)", t or "")


def publicada(fecha):
    d = datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def textos(p):
    """Todo el texto de una pieza, en el orden en que se lee."""
    partes = [p.get("antetitulo"), p.get("titular"), p.get("entradilla")]
    cuerpo = p.get("cuerpo")
    partes += cuerpo if isinstance(cuerpo, list) else [cuerpo]
    for a in p.get("apartados") or []:   # reportajes
        partes += [a.get("ladillo")] + list(a.get("parrafos") or [])
    for r in p.get("recursos") or []:   # Repositorio
        partes += [r.get("titulo"), r.get("url")]
    for f in p.get("fuentes") or []:
        partes += [f.get("titulo"), f.get("url")]
    return "\n".join(sin_marcas(x) for x in partes if isinstance(x, str) and x)


def documentos():
    docs = []
    def pieza(fecha, p, donde):
        docs.append({"clave": f"pieza:{fecha}/{p['id']}", "fecha": fecha, "donde": donde,
                     "seccion": p.get("seccion") or donde, "titular": p.get("titular", ""), "texto": textos(p)})
    for f in sorted((RAIZ / "ediciones").glob("*.json")):
        d = json.loads(f.read_text())
        if not d.get("hay_edicion"):
            continue
        for p in d.get("piezas", []):
            pieza(d["fecha"], p, "número")
        for b in d.get("breves", []):
            t = sin_marcas(b.get("texto", ""))
            docs.append({"clave": "breve (sin enlace propio)", "fecha": d["fecha"],
                         "donde": "breve", "seccion": "breves", "titular": t[:110] + ("…" if len(t) > 110 else ""), "texto": t})
    for carpeta in ("biblioteca", "repositorio", "hace-un-ano"):
        for f in sorted((RAIZ / carpeta).glob("*.json")):
            d = json.loads(f.read_text())
            for p in d.get("piezas", []):
                pieza(d.get("fecha") or f.stem, p, carpeta)
    for f in sorted((RAIZ / "reportajes").glob("*.json")):
        d = json.loads(f.read_text())
        if d.get("hay_reportaje") and d.get("id"):
            pieza(f.stem, d, "reportaje")
    return docs


def indice(docs):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE VIRTUAL TABLE t USING fts5(raices, tokenize='unicode61')")
    db.executemany("INSERT INTO t(rowid, raices) VALUES (?, ?)",
                   [(i, " ".join(raices(d["titular"] + "\n" + d["texto"]))) for i, d in enumerate(docs)])
    vocab = {}
    for d in docs:
        for p in palabras(d["titular"] + "\n" + d["texto"]):
            vocab.setdefault(_raiz(p), set()).add(p)
    return db, vocab


def variantes(termino, vocab):
    """La raíz de una palabra y, si no sale en nada, las de las palabras parecidas que sí salen."""
    r = _raiz(plano(termino))
    if r in vocab:
        return [r], []
    todas = {p: rr for rr, ps in vocab.items() for p in ps}
    cerca = difflib.get_close_matches(plano(termino), list(todas), n=3, cutoff=0.85)
    return sorted({todas[p] for p in cerca}), cerca


def marca(w, buscadas):
    """Pone entre corchetes las palabras buscadas dentro de un trozo, sin la puntuación que las rodea."""
    return re.sub(r"\w+", lambda m: f"[{m.group(0)}]" if any(_raiz(y) in buscadas for y in palabras(m.group(0))) else m.group(0), w)


def trozos(doc, buscadas, n=2, ancho=14):
    """Los trozos del texto donde aparecen las palabras buscadas, marcadas entre corchetes."""
    ps = re.findall(r"\S+", doc["texto"])
    out, usado = [], -1
    for i, w in enumerate(ps):
        if i <= usado or not any(_raiz(x) in buscadas for x in palabras(w)):
            continue
        a, b = max(0, i - ancho), min(len(ps), i + ancho + 1)
        t = " ".join(marca(x, buscadas) for x in ps[a:b])
        out.append(("…" if a else "") + t + ("…" if b < len(ps) else ""))
        usado = b
        if len(out) == n:
            break
    return out


def consulta(grupos, todas):
    """grupos: una lista de raíces alternativas por cada palabra. Con `todas`, cada palabra tiene que estar."""
    exp = [("(" + " OR ".join(f'"{r}"' for r in g) + ")") for g in grupos if g]
    return (" AND " if todas else " OR ").join(exp)


def buscar(palabras_=(), alguna=False, parecidas=None, desde=None, maximo=15):
    """La búsqueda entera, devuelta como texto: la usan la orden y la herramienta de los agentes."""
    docs = documentos()
    db, vocab = indice(docs)
    avisos, out = [], []
    if parecidas:
        # Las palabras del texto que más distinguen (las menos frecuentes en lo publicado), hasta 30
        n = len(docs)
        df = {r: db.execute("SELECT count(*) FROM t WHERE t MATCH ?", (f'"{r}"',)).fetchone()[0]
              for r in {_raiz(p) for p in palabras(parecidas) if p not in VACIAS and len(p) > 2} if r in vocab}
        clave = sorted((r for r, c in df.items() if 0 < c < n * 0.3), key=lambda r: df[r])[:30]
        grupos, todas = [[r] for r in clave], False
        if not grupos:
            return "El texto no tiene palabras que aparezcan en lo publicado: no se parece a nada.\n"
    else:
        grupos = []
        for t in palabras_:
            for p in palabras(t):
                g, cerca = variantes(p, vocab)
                if cerca:
                    avisos.append(f"«{p}» no sale en nada; se busca también como: {', '.join(cerca)}")
                elif not g:
                    avisos.append(f"«{p}» no sale en nada ni hay palabras parecidas")
                grupos.append(g)
        todas = not alguna
    filas = []
    q = consulta(grupos, todas)
    if q:
        filas = db.execute("SELECT rowid, bm25(t) FROM t WHERE t MATCH ? ORDER BY bm25(t)", (q,)).fetchall()
        if not filas and todas and len(grupos) > 1:
            avisos.append("Ninguna pieza tiene todas las palabras; van las que tienen alguna")
            filas = db.execute("SELECT rowid, bm25(t) FROM t WHERE t MATCH ? ORDER BY bm25(t)",
                               (consulta(grupos, False),)).fetchall()
    if desde:
        filas = [f for f in filas if docs[f[0]]["fecha"] >= desde]
    out += [f"Aviso: {x}" for x in avisos]
    out.append(f"{len(filas)} resultados en {len(docs)} piezas y breves publicados"
               + (f" (se enseñan {maximo})" if len(filas) > maximo else "") + "\n")
    buscadas = {r for g in grupos for r in g}
    for rowid, _ in filas[:maximo]:
        d = docs[rowid]
        out.append(f"{d['clave']} · publicado el {publicada(d['fecha'])} · {d['seccion']}")
        out.append(f"  {d['titular']}")
        out += [f"    {t}" for t in trozos(d, buscadas)]
        out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("palabras", nargs="*")
    ap.add_argument("--alguna", action="store_true", help="basta con una de las palabras")
    ap.add_argument("--parecidas", metavar="TEXTO", help="piezas que tratan de lo mismo que este texto")
    ap.add_argument("--desde", metavar="AAAA-MM-DD")
    ap.add_argument("--max", type=int, default=15)
    a = ap.parse_args()
    if not a.palabras and not a.parecidas:
        ap.error("di qué buscar")
    print(buscar(a.palabras, a.alguna, a.parecidas, a.desde, a.max), end="")


if __name__ == "__main__":
    main()
