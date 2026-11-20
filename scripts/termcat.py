#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La terminología del TERMCAT para los agentes (ADR 0094), sin IA.

La web del TERMCAT (el Cercaterm) tiene una protección contra los programas puesta a propósito, que no se salta. El
propio TERMCAT remite en su robots.txt a la «Terminologia oberta» (https://www.termcat.cat/ca/terminologia-oberta):
sus diccionarios, para descargarlos enteros en XML, con la licencia Creative Commons de cada uno. El diario solo los
consulta: no publica nada de ellos.

    scripts/termcat.py descargar [--si-toca]   baja los diccionarios y rehace el índice (--si-toca: solo si tiene más
                                               de 30 días); si falla una descarga, se queda el índice anterior
    scripts/termcat.py buscar PALABRAS         busca un término en catalán, inglés o castellano

El índice va en cache/termcat/, fuera del repositorio. Los agentes lo consultan con la herramienta «buscar_termcat»
(scripts/buscar-mcp.py).
"""
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "cache" / "termcat"
INDICE = CARPETA / "indice.json"
URL = "https://www.termcat.cat/Thor/files/diccionaris/{}.xml"
# La Neoloteca son los términos que ha normalizado el Consell Supervisor del TERMCAT; los otros tres, los de lo que
# más trata el diario
DICCIONARIOS = ("neolotecaambcriteris", "intelligenciaartificial", "educacio", "productesinformatics")
DIAS = 30
JERARQUIA = {"terme pral.": "", "sin. compl.": "sinònim complementari", "sigla": "sigla", "abrev.": "abreviació",
             "var. ling.": "variant", "alt. sin.": "sinònim", "den. com.": "denominació comercial",
             "den. desest.": "DESESTIMAT"}
LENGUAS = {"en": "anglès", "es": "castellà", "fr": "francès", "it": "italià", "pt": "portuguès", "de": "alemany"}


def plano(t):
    """Sin tildes, sin punto volado y en minúsculas, para comparar."""
    t = unicodedata.normalize("NFD", t.lower().replace("·", "").replace("l.l", "ll"))
    return re.sub(r"\s+", " ", "".join(c for c in t if unicodedata.category(c) != "Mn")).strip()


def leer(nombre, xml):
    raiz = ET.fromstring(xml)
    titulo = (raiz.findtext("titol") or nombre).strip()
    fichas = []
    for f in raiz.iter("fitxa"):
        den, normalizado = [], False
        for d in f.findall("denominacio"):
            texto = (d.text or "").strip()
            if d.get("llengua") == "cod":
                normalizado = normalizado or texto.startswith("**Motiu de normalització")
                continue
            den.append([d.get("llengua"), texto, d.get("jerarquia") or "", d.get("tipus") or "", d.get("categoria") or ""])
        if not any(x[0] == "ca" for x in den):
            continue
        defi = next(((d.text or "").strip() for d in f.findall("definicio") if d.get("llengua") == "ca"), "")
        areas = [(a.text or "").strip() for a in f.findall("areatematica") if not (a.text or "").startswith("**")]
        notas = [(n.text or "").strip() for n in f.findall("nota") if (n.text or "").strip()]
        fichas.append({"d": nombre, "den": den, "def": defi, "area": areas[:1], "notas": notas[:2],
                       "norm": normalizado or nombre == "neolotecaambcriteris"})
    return titulo, fichas


def descargar(si_toca=False):
    if si_toca and INDICE.exists() and time.time() - INDICE.stat().st_mtime < DIAS * 86400:
        return 0
    CARPETA.mkdir(parents=True, exist_ok=True)
    titulos, fichas = {}, []
    for nombre in DICCIONARIOS:
        pet = urllib.request.Request(URL.format(nombre), headers={"User-Agent": "Mozilla/5.0 (compatible; consulta)"})
        try:
            with urllib.request.urlopen(pet, timeout=120) as r:
                titulos[nombre], fs = leer(nombre, r.read())
        except Exception as x:
            print(f"termcat: no se pudo bajar {nombre} ({x}); queda el índice anterior", file=sys.stderr)
            return 1
        fichas += fs
    tmp = INDICE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"fecha": time.strftime("%Y-%m-%d"), "titulos": titulos, "fichas": fichas},
                              ensure_ascii=False), encoding="utf-8")
    tmp.replace(INDICE)
    print(f"termcat: {len(fichas)} fichas de {len(titulos)} diccionarios")
    return 0


def ficha_texto(f, titulos):
    ca = [x for x in f["den"] if x[0] == "ca"]
    principal = next((x for x in ca if x[3] == "principal"), ca[0])
    linea = f"«{principal[1]}»" + (f" ({principal[4]})" if principal[4] else "")
    linea += ", terme normalitzat pel Consell Supervisor del TERMCAT" if f["norm"] else ", terme recomanat pel TERMCAT"
    out = [linea]
    altres = [f"«{x[1]}» ({JERARQUIA.get(x[2], x[2]) or 'també'})" for x in ca if x is not principal]
    if altres:
        out.append("  En català, també: " + ", ".join(altres))
    for c, nom in LENGUAS.items():
        eq = [x[1] + (f" ({JERARQUIA.get(x[2], x[2])})" if JERARQUIA.get(x[2]) else "") for x in f["den"] if x[0] == c]
        if eq:
            out.append(f"  {nom}: " + "; ".join(eq))
    if f["def"]:
        out.append("  Definició: " + f["def"])
    for n in f["notas"]:
        out.append("  Nota: " + n[:400])
    out.append(f"  Font: TERMCAT, {titulos.get(f['d'], f['d'])}" + (f" ({f['area'][0]})" if f["area"] else ""))
    return "\n".join(out)


def principal(f):
    ca = [x for x in f["den"] if x[0] == "ca"]
    return plano(next((x for x in ca if x[3] == "principal"), ca[0])[1])


def buscar(palabras, maximo=8):
    if not INDICE.exists():
        raise RuntimeError("Encara no hi ha l'índex del TERMCAT; consulta l'Optimot.")
    datos = json.loads(INDICE.read_text(encoding="utf-8"))
    q = plano(palabras)
    if not q:
        raise ValueError("Falta el terme que es busca.")
    exactas, enteras, parte = [], [], []
    for f in datos["fichas"]:
        noms = [plano(x[1]) for x in f["den"]]
        if q in noms:
            exactas.append(f)
        elif any(re.search(rf"(?<!\w){re.escape(q)}(?!\w)", n) for n in noms):
            enteras.append(f)
        elif len(q) > 3 and any(q in n for n in noms):
            parte.append(f)
    # Primero las normalizadas, y una ficha repetida en dos diccionarios (la del de IA y la de la Neoloteca), una vez
    # (mismo término catalán y algún equivalente inglés en común: el mismo concepto)
    res = []
    for f in sorted(exactas, key=lambda f: not f["norm"]) + enteras + parte:
        ca, en = principal(f), {plano(x[1]) for x in f["den"] if x[0] == "en"}
        if not any(principal(g) == ca and (en & {plano(x[1]) for x in g["den"] if x[0] == "en"} or not en) for g in res):
            res.append(f)
    if not res:
        return (f"No hi ha cap fitxa del TERMCAT amb «{palabras}» als diccionaris consultats "
                f"({', '.join(datos['titulos'].values())}). Consulta l'Optimot.")
    total = len(res)
    cab = f"{total} {'fitxa' if total == 1 else 'fitxes'} del TERMCAT (índex del {datos['fecha']})" + (
        f"; se'n mostren {maximo}" if total > maximo else "") + ":"
    return cab + "\n\n" + "\n\n".join(ficha_texto(f, datos["titulos"]) for f in res[:maximo])


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "descargar":
        return descargar("--si-toca" in sys.argv[2:])
    if orden == "buscar" and len(sys.argv) > 2:
        print(buscar(" ".join(sys.argv[2:])))
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
