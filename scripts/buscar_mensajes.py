#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El buscador de los mensajes de los grupos, para los agentes (ADR 0061): todo el historial de ChatGPT-IA-edu,
Vibe Coding Educativo y EduMedia-IAG, con el mismo motor que el de lo publicado (scripts/buscar.py).

    python3 scripts/buscar_mensajes.py PALABRAS…              mensajes que tienen todas las palabras
    python3 scripts/buscar_mensajes.py --alguna PALABRAS…     con alguna, los que más tienen primero
    python3 scripts/buscar_mensajes.py --parecidas "TEXTO"    mensajes que tratan de lo mismo que un texto
    python3 scripts/buscar_mensajes.py --grupo vce …          solo un grupo (chatgpt, vce, edumedia)
    python3 scripts/buscar_mensajes.py --desde AAAA-MM-DD --hasta AAAA-MM-DD …
    python3 scripts/buscar_mensajes.py --orden fecha …        los más recientes primero, no los más pertinentes
    python3 scripts/buscar_mensajes.py --contexto vce:14875   un mensaje con lo que lo rodea en su tema y sus respuestas
    python3 scripts/buscar_mensajes.py --indexar              rehace el índice entero (lo hace noche.sh cada noche)

Lee los mensajes que guarda el Bot de IA Educativa (`$DATOS_BOT`, por omisión /bot-datos), con lo que el bot
describe de cada imagen y la vista previa de cada enlace. El índice (SQLite FTS5, sobre las raíces de las
palabras) se guarda en `cache/mensajes.sqlite`; cada consulta añade antes los mensajes nuevos, así que siempre
está al día. Cada resultado lleva el enlace directo al mensaje, que es el que se cita.

Los agentes no tienen consola: lo usan como herramientas `mcp__diario__buscar_mensajes` y
`mcp__diario__contexto_mensaje`, que da `scripts/buscar-mcp.py`.
"""
import argparse
import json
import os
import pathlib
import re
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from buscar import VACIAS, _raiz, consulta, marca, palabras, plano, raices   # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATOS = pathlib.Path(os.environ.get("DATOS_BOT", "/bot-datos"))
INDICE = RAIZ / "cache" / "mensajes.sqlite"
GRUPOS = {"chatgpt": ("ChatGPT-IA-edu", "ChatGPTedu"), "vce": ("Vibe Coding Educativo", "vceduca"),
          "edumedia": ("EduMedia-IAG", "EduMediaIAG")}
ESQUEMA = """
CREATE TABLE IF NOT EXISTS m (n INTEGER PRIMARY KEY, grupo TEXT, id INTEGER, fecha TEXT, tema TEXT, tema_nombre TEXT,
    autor TEXT, responde_a INTEGER, texto TEXT, UNIQUE(grupo, id));
CREATE VIRTUAL TABLE IF NOT EXISTS t USING fts5(raices, tokenize='unicode61');
CREATE TABLE IF NOT EXISTS vocab (raiz TEXT, palabra TEXT, PRIMARY KEY (raiz, palabra)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS estado (grupo TEXT PRIMARY KEY, tam INTEGER, mtime REAL);
"""


def enlace(grupo, tema, mid):
    alias = GRUPOS[grupo][1]
    return f"https://t.me/{alias}/{tema}/{mid}" if tema and str(tema) not in ("1", "None", "") else f"https://t.me/{alias}/{mid}"


def texto_de(m, imagenes):
    partes = [m.get("texto") or ""]
    w = m.get("web") or {}
    if w.get("url"):
        partes.append(f"[enlace: {w['url']} · {w.get('titulo') or ''} · {' '.join((w.get('descripcion') or '').split())}]")
    if m.get("archivo"):
        partes.append(f"[archivo: {m['archivo']}]")
    d = imagenes / f"{m['id']}.txt"
    if d.exists():
        partes.append(f"[imagen: {d.read_text(errors='replace').strip()}]")
    return "\n".join(p for p in partes if p.strip())


def indexar(db, completo=False):
    """Añade los mensajes que faltan; con `completo`, lo rehace todo (recoge también los editados)."""
    if completo:
        db.executescript("DELETE FROM m; DELETE FROM t; DELETE FROM vocab; DELETE FROM estado;")
    nuevos = 0
    for g in GRUPOS:
        f = DATOS / g / "mensajes.jsonl"
        if not f.exists():
            continue
        st = f.stat()
        previo = db.execute("SELECT tam, mtime FROM estado WHERE grupo=?", (g,)).fetchone()
        if previo and previo[0] == st.st_size and previo[1] == st.st_mtime:
            continue
        temas = json.loads((DATOS / g / "temas.json").read_text()) if (DATOS / g / "temas.json").exists() else {}
        imagenes = DATOS / g / "imagenes"
        ya = {r[0] for r in db.execute("SELECT id FROM m WHERE grupo=?", (g,))}
        filas, vocab = [], set()
        for linea in f.open():
            try:
                m = json.loads(linea)
            except ValueError:
                continue
            mid = int(m["id"])
            if mid in ya:
                continue
            tx = texto_de(m, imagenes)
            if not tx.strip():
                continue
            tema = str(m.get("tema") or "1")
            filas.append((g, mid, m.get("fecha", ""), tema, temas.get(tema, "General"), m.get("autor") or "",
                          int(m["responde_a"]) if str(m.get("responde_a") or "").isdigit() else None, tx))
            vocab.update((_raiz(p), p) for p in palabras(tx))
        for fila in filas:
            cur = db.execute("INSERT OR IGNORE INTO m (grupo, id, fecha, tema, tema_nombre, autor, responde_a, texto) "
                             "VALUES (?,?,?,?,?,?,?,?)", fila)
            if cur.rowcount:
                db.execute("INSERT INTO t (rowid, raices) VALUES (?, ?)", (cur.lastrowid, " ".join(raices(fila[7]))))
                nuevos += 1
        db.executemany("INSERT OR IGNORE INTO vocab VALUES (?, ?)", vocab)
        db.execute("INSERT OR REPLACE INTO estado VALUES (?, ?, ?)", (g, st.st_size, st.st_mtime))
    db.commit()
    return nuevos


def abrir():
    INDICE.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(INDICE)
    db.executescript(ESQUEMA)
    indexar(db)
    return db


def variantes(db, termino):
    import difflib
    r = _raiz(plano(termino))
    if db.execute("SELECT 1 FROM vocab WHERE raiz=? LIMIT 1", (r,)).fetchone():
        return [r], []
    # Las parecidas, entre las palabras que empiezan igual (el vocabulario entero es grande)
    p = plano(termino)
    cand = [x[0] for x in db.execute("SELECT DISTINCT palabra FROM vocab WHERE palabra LIKE ? LIMIT 5000", (p[:2] + "%",))]
    cerca = difflib.get_close_matches(p, cand, n=3, cutoff=0.85)
    return sorted({_raiz(c) for c in cerca}), cerca


def recorta(texto, buscadas, largo=420):
    """El mensaje, con las palabras buscadas marcadas; si es largo, el trozo donde aparecen."""
    t = " ".join(texto.split())
    if len(t) > largo:
        ps = t.split(" ")
        i = next((k for k, w in enumerate(ps) if any(_raiz(y) in buscadas for y in palabras(w))), 0)
        a = max(0, i - 25)
        t = ("…" if a else "") + " ".join(ps[a:a + 70]) + "…"
    return " ".join(marca(w, buscadas) for w in t.split(" "))


def formato(fila, buscadas=frozenset()):
    _, g, mid, fecha, tema, tema_nombre, autor, resp, tx = fila
    cab = f"{enlace(g, tema, mid)} · {fecha[:10]} {fecha[11:16]} · {GRUPOS[g][0]}, tema «{tema_nombre}» · {autor}"
    if resp:
        cab += f" · responde a #{resp}"
    return cab + "\n    " + recorta(tx, buscadas)


def buscar_mensajes(palabras_=(), alguna=False, parecidas=None, grupo=None, desde=None, hasta=None,
                    orden="pertinencia", maximo=15):
    db = abrir()
    total = db.execute("SELECT count(*) FROM m").fetchone()[0]
    avisos, out = [], []
    if parecidas:
        cands = {_raiz(p) for p in palabras(parecidas) if p not in VACIAS and len(p) > 2}
        df = {r: db.execute("SELECT count(*) FROM t WHERE t MATCH ?", (f'"{r}"',)).fetchone()[0] for r in cands}
        clave = sorted((r for r, c in df.items() if 0 < c < total * 0.05), key=lambda r: df[r])[:30]
        grupos, todas = [[r] for r in clave], False
        if not grupos:
            return "El texto no tiene palabras que aparezcan en los mensajes: no se parece a nada.\n"
    else:
        grupos = []
        for t in palabras_:
            for p in palabras(t):
                g, cerca = variantes(db, p)
                if cerca:
                    avisos.append(f"«{p}» no sale en nada; se busca también como: {', '.join(cerca)}")
                elif not g:
                    avisos.append(f"«{p}» no sale en nada ni hay palabras parecidas")
                grupos.append(g)
        todas = not alguna
    filtro, params = [], []
    if grupo:
        filtro.append("m.grupo = ?"); params.append(grupo)
    if desde:
        filtro.append("m.fecha >= ?"); params.append(desde)
    if hasta:
        filtro.append("m.fecha < ?"); params.append(hasta + "T99")
    donde = "".join(f" AND {f}" for f in filtro)
    ordena = "m.fecha DESC" if orden == "fecha" else "bm25(t)"
    sql = (f"SELECT m.n, m.grupo, m.id, m.fecha, m.tema, m.tema_nombre, m.autor, m.responde_a, m.texto "
           f"FROM t JOIN m ON m.n = t.rowid WHERE t MATCH ?{donde} ORDER BY {ordena}")
    filas = []
    q = consulta(grupos, todas)
    if q:
        filas = db.execute(sql, [q] + params).fetchall()
        if not filas and todas and len(grupos) > 1:
            avisos.append("Ningún mensaje tiene todas las palabras; van los que tienen alguna")
            filas = db.execute(sql, [consulta(grupos, False)] + params).fetchall()
    out += [f"Aviso: {x}" for x in avisos]
    out.append(f"{len(filas)} mensajes encontrados entre {total} de los tres grupos"
               + (f" (se enseñan {maximo})" if len(filas) > maximo else "") + "\n")
    buscadas = {r for g in grupos for r in g}
    for f in filas[:maximo]:
        out += [formato(f, buscadas), ""]
    return "\n".join(out) + "\n"


def contexto(ref, antes=5, despues=10):
    """Un mensaje con los que lo rodean en su tema y todo lo que le respondieron. ref: grupo:id."""
    db = abrir()
    g, _, mid = ref.partition(":")
    if g not in GRUPOS or not mid.isdigit():
        raise ValueError("La referencia es grupo:id, por ejemplo vce:14875 (grupos: chatgpt, vce, edumedia).")
    base = db.execute("SELECT n, grupo, id, fecha, tema, tema_nombre, autor, responde_a, texto FROM m "
                      "WHERE grupo=? AND id=?", (g, int(mid))).fetchone()
    if not base:
        return f"No hay ningún mensaje {ref} (o no tiene texto).\n"
    cols = "n, grupo, id, fecha, tema, tema_nombre, autor, responde_a, texto"
    previos = db.execute(f"SELECT {cols} FROM m WHERE grupo=? AND tema=? AND id<? ORDER BY id DESC LIMIT ?",
                         (g, base[4], base[2], antes)).fetchall()[::-1]
    siguientes = db.execute(f"SELECT {cols} FROM m WHERE grupo=? AND tema=? AND id>? ORDER BY id LIMIT ?",
                            (g, base[4], base[2], despues)).fetchall()
    respuestas = db.execute(f"SELECT {cols} FROM m WHERE grupo=? AND responde_a=? ORDER BY id", (g, base[2])).fetchall()
    origen = db.execute(f"SELECT {cols} FROM m WHERE grupo=? AND id=?", (g, base[7])).fetchone() if base[7] else None
    out = []
    if origen:
        out += ["Mensaje al que responde:", formato(origen), ""]
    out += ["Antes, en el mismo tema:"] + [formato(f) for f in previos] + ["", ">>> El mensaje:", formato(base), "",
            "Después, en el mismo tema:"] + [formato(f) for f in siguientes]
    extra = [f for f in respuestas if f[0] not in {x[0] for x in siguientes}]
    if extra:
        out += ["", "Otras respuestas a este mensaje:"] + [formato(f) for f in extra]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("palabras", nargs="*")
    ap.add_argument("--alguna", action="store_true")
    ap.add_argument("--parecidas", metavar="TEXTO")
    ap.add_argument("--grupo", choices=list(GRUPOS))
    ap.add_argument("--desde", metavar="AAAA-MM-DD")
    ap.add_argument("--hasta", metavar="AAAA-MM-DD")
    ap.add_argument("--orden", choices=["pertinencia", "fecha"], default="pertinencia")
    ap.add_argument("--max", type=int, default=15)
    ap.add_argument("--contexto", metavar="GRUPO:ID")
    ap.add_argument("--indexar", action="store_true", help="rehace el índice entero")
    a = ap.parse_args()
    if a.indexar:
        INDICE.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(INDICE)
        db.executescript(ESQUEMA)
        print(f"Índice de mensajes rehecho: {indexar(db, completo=True)} mensajes")
        return
    if a.contexto:
        print(contexto(a.contexto), end="")
        return
    if not a.palabras and not a.parecidas:
        ap.error("di qué buscar")
    print(buscar_mensajes(a.palabras, a.alguna, a.parecidas, a.grupo, a.desde, a.hasta, a.orden, a.max), end="")


if __name__ == "__main__":
    main()
