#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El comentario de la semana (ADR 0038): lo más importante de lo que contó el diario en una semana, uno
general y uno de cada grupo.

    scripts/comentario_semana.py entrada SEMANA            prepara comentario-semana-entrada/SEMANA.md
    scripts/comentario_semana.py comprobar SEMANA          comprueba comentario-semana/SEMANA.json
    scripts/comentario_semana.py traduccion SEMANA IDIOMA  comprueba la traducción; si no vale, la quita

SEMANA es la ISO, AAAA-WW, la de los mensajes, como las páginas semana/AAAA-WW/. Sin IA: solo ordena
y comprueba. «comprobar» sale con 1 y dice qué falla; «traduccion», con 1 si ha quitado el archivo."""
import datetime
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MIN_PALABRAS, MAX_PALABRAS = 150, 250
MIN_GRUPO_CORTO = 80   # el de un grupo con una o dos piezas en la semana
MAX_ENLACES = 6
PIEZA = re.compile(r"\]\(pieza:(\d{4}-\d{2}-\d{2})/([\w-]+)\)")
ENLACE = re.compile(r"\]\((?:https?://|pieza:)")
GRUPOS = {"chatgpt": "ChatGPT-IA-edu", "vce": "Vibe Coding Educativo", "edumedia": "EduMedia-IAG"}


def dias(sem):
    y, w = map(int, sem.split("-"))
    lunes = datetime.date.fromisocalendar(y, w, 1)
    return [(lunes + datetime.timedelta(days=i)).isoformat() for i in range(7)]


def leer(f):
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return None


def piezas_semana(sem):
    """[(fecha, pieza)] de la semana: las del número, la Biblioteca, el Repositorio y el reportaje."""
    salida = []
    for fecha in dias(sem):
        for carpeta in ("ediciones", "biblioteca", "repositorio"):
            d = leer(RAIZ / carpeta / f"{fecha}.json") or {}
            if carpeta == "ediciones" and not d.get("hay_edicion"):
                continue
            salida += [(fecha, p) for p in d.get("piezas") or []]
        r = leer(RAIZ / "reportajes" / f"{fecha}.json") or {}
        if r.get("hay_reportaje") and r.get("id"):
            salida.append((fecha, dict(r, seccion="reportaje")))
    return salida


def entrada(sem):
    ps = piezas_semana(sem)
    d = dias(sem)
    partes = [f"# Lo que contó el diario de la semana {sem} (mensajes del {d[0]} al {d[-1]})\n",
              "Cada pieza con su clave para enlazarla, su sección, el grupo del que sale y su importancia "
              "en el número (1, la que lo abría; 3, la menor). El texto completo está en "
              "ediciones/, biblioteca/, repositorio/ y reportajes/, con el nombre de la fecha.\n"]
    fecha_ant = None
    for fecha, p in ps:
        if fecha != fecha_ant:
            partes.append(f"\n## Mensajes del {fecha}\n")
            fecha_ant = fecha
        grupo = GRUPOS.get(grupo_de(p), "—")
        partes.append(f'- pieza:{fecha}/{p["id"]} · {p.get("seccion") or "—"} · {grupo} · importancia {p.get("importancia", "—")}\n'
                      f'  {p.get("titular", "")}\n  {p.get("entradilla", "")}')
    for fecha in d:
        for b in (leer(RAIZ / "ediciones" / f"{fecha}.json") or {}).get("breves") or []:
            partes.append(f'- breve del {fecha}: {b.get("texto", "")[:300]}')
    cuenta = {g: sum(1 for _, p in ps if grupo_de(p) == g) for g in GRUPOS}
    partes.insert(2, "Piezas de cada grupo esta semana: " + ", ".join(f"{GRUPOS[g]} (`{g}`), {n}" for g, n in cuenta.items())
                  + ". Las que no son de ningún grupo (el reportaje) solo van en el general.\n")
    destino = RAIZ / "comentario-semana-entrada" / f"{sem}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n".join(partes) + "\n")
    print(f"semana {sem}: {len(ps)} piezas")
    return 0 if ps else 3


def texto(c):
    return " ".join(c.get("parrafos") or [])


def palabras(t):
    t = re.sub(r"\]\([^)]*\)", "]", t)   # el destino de los enlaces no cuenta
    return len(re.findall(r"\w+", t))


def bloques(c):
    """[(clave, bloque)]: el general y el de cada grupo que lo tenga."""
    salida = [("general", c["general"])] if c.get("general") else []
    return salida + [(g, b) for g, b in (c.get("grupos") or {}).items() if b]


def grupo_de(p):
    return p.get("grupo") or (p.get("mensaje") or {}).get("grupo")


def minimo(n_piezas):
    """150 palabras; un grupo con una o dos piezas en la semana no da para tanto sin rellenar."""
    return MIN_PALABRAS if n_piezas >= 3 else MIN_GRUPO_CORTO


def comprobar_bloque(nombre, b, validas, n_piezas):
    malos = []
    if not (b.get("titulo") or "").strip():
        malos.append("falta el título")
    pars = b.get("parrafos") or []
    if not 1 <= len(pars) <= 4 or not all(isinstance(p, str) and p.strip() for p in pars):
        malos.append("tiene que tener de uno a cuatro párrafos")
    n, mi = palabras(texto(b)), minimo(n_piezas)
    if not mi <= n <= MAX_PALABRAS:
        malos.append(f"tiene {n} palabras (de {mi} a {MAX_PALABRAS})")
    claves = PIEZA.findall(texto(b))
    if not claves:
        malos.append("no enlaza ninguna pieza")
    if len(ENLACE.findall(texto(b))) > MAX_ENLACES:
        malos.append(f"más de {MAX_ENLACES} enlaces")
    fuera = [f"{f}/{i}" for f, i in claves if (f, i) not in validas]
    if fuera:
        malos.append("enlaza piezas que no le tocan: " + ", ".join(fuera))
    return [f"{nombre}: {m}" for m in malos]


def comprobar(sem):
    c = leer(RAIZ / "comentario-semana" / f"{sem}.json")
    if c is None:
        return ["no está o no es un JSON válido"]
    if not c.get("hay_comentario"):
        return []
    ps = piezas_semana(sem)
    malos = [] if c.get("general") else ["falta el general"]
    for nombre, b in bloques(c):
        if nombre != "general" and nombre not in GRUPOS:
            malos.append(f"{nombre}: no es un grupo")
            continue
        suyas = [(f, p) for f, p in ps if nombre == "general" or grupo_de(p) == nombre]
        malos += comprobar_bloque(nombre, b, {(f, p["id"]) for f, p in suyas}, len(suyas))
    for g in GRUPOS:   # cada grupo con piezas en la semana tiene el suyo
        if any(grupo_de(p) == g for _, p in ps) and not (c.get("grupos") or {}).get(g):
            malos.append(f"falta el de {g}")
    return malos


def traduccion(sem, idioma):
    orig, f = RAIZ / "comentario-semana" / f"{sem}.json", RAIZ / f"comentario-semana-{idioma}" / f"{sem}.json"
    if not f.exists() or not orig.exists():
        return []
    o, t = leer(orig) or {}, leer(f)
    malos = []
    if t is None:
        malos.append("no es un JSON válido")
    else:
        bt = dict(bloques(t))
        for nombre, b in bloques(o):
            x = bt.get(nombre)
            if not x:
                malos.append(f"{nombre}: falta")
                continue
            if not (x.get("titulo") or "").strip():
                malos.append(f"{nombre}: falta el título")
            if len(b.get("parrafos") or []) != len(x.get("parrafos") or []):
                malos.append(f"{nombre}: no tiene los mismos párrafos")
            if sorted(PIEZA.findall(texto(b))) != sorted(PIEZA.findall(texto(x))):
                malos.append(f"{nombre}: no tiene los mismos enlaces")
            ta, tb = texto(b), texto(x)
            if ta and not 0.5 <= len(tb) / len(ta) <= 2.0:
                malos.append(f"{nombre}: el largo no cuadra ({len(tb)} frente a {len(ta)} caracteres)")
    if malos:
        f.unlink()
        return [f"comentario-semana-{idioma}/{sem}.json quitado: " + "; ".join(malos)]
    return []


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "entrada":
        sys.exit(entrada(sys.argv[2]))
    elif orden == "comprobar":
        m = comprobar(sys.argv[2])
        for linea in m:
            print(f"comentario de la semana: {linea}")
        sys.exit(1 if m else 0)
    elif orden == "traduccion":
        m = traduccion(sys.argv[2], sys.argv[3])
        for linea in m:
            print(f"traducción: {linea}")
        sys.exit(1 if m else 0)
    print(__doc__)
    sys.exit(2)
