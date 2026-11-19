#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las normas del libro de estilo (encargos/estilo.md) que se pueden comprobar sin IA (ADR 0067 y 0083), en lo
escrito cada noche.

    scripts/revisar-estilo.py --dia AAAA-MM-DD   lo escrito esa noche, en castellano y en las traducciones no inglesas
    scripts/revisar-estilo.py --todo             todo lo publicado (para medir)

1. **Sin el relativo «quien»** con el sentido de «la persona que» (15-11-2026: «no quiero que se use quien o
   quienes en este sentido»). Solo en castellano: allí el relativo no lleva tilde y el interrogativo sí
   («¿quién?»), así que basta con buscar la palabra sin tilde. Las citas literales no se tocan.
2. **Ninguna cita solo en inglés en una edición que no es inglesa** (15-11-2026: «No debe haber fragmentos solo en
   inglés en idioma no inglés»): la cita va traducida o con su traducción al lado, entre paréntesis. Una cita es
   inglesa si al menos una de cada cinco de sus palabras es de las más corrientes del inglés.
3. **Vocabulario y forma** (ADR 0083), solo en castellano y fuera de las citas y las direcciones: «hoy», «ayer» y
   «esta semana» (salvo en «Hace un año», que compara con el presente, y en los avisos, que salen ese mismo día);
   «pieza» ante el lector; «el diario cuenta» o «contó»; «app», «online» y «link» en minúscula (los nombres propios
   van con mayúscula); «la AI»; el condicional de rumor («habría lanzado»), y el porcentaje sin espacio («25%»).
   Lo que es otro sentido o un nombre propio lo deja el corrector, que lo dice.
Escribe una línea por frase, con la norma, y sale con 4; sin nada, con 0.
"""
import datetime
import importlib.util
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("autoria", RAIZ / "scripts" / "revisar-autoria.py")
autoria = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(autoria)

SECCIONES = ("ediciones", "reportajes", "biblioteca", "hace-un-ano", "repositorio", "columnas")
IDIOMAS = ("", "-ca", "-gl", "-eu")   # el inglés no: allí una cita inglesa es su idioma
QUIEN = re.compile(r"\b[Qq]uien(es)?\b")
CITA = re.compile(r"«([^»]*)»|“([^”]*)”")
INGLES = set("the an and or of to in for is are was were be been will would need your you we they with not that "
             "this these those by on as it its can could may should must have has had their our from at which who "
             "what when how does did if than more most only also into about".split())
TRADUCIDA = re.compile(r"^\s*\(\s*[«“]")   # la traducción, al lado: «…» («…»)
# Las normas de vocabulario y forma del libro de estilo (ADR 0083): (nombre, expresión, carpetas donde no vale)
NORMAS = [
    ("«hoy», «ayer» o «esta semana»: mejor la fecha o el día", re.compile(r"\b(?:[Hh]oy(?! en día)|[Aa]yer|[Ee]sta semana)\b"),
     ("hace-un-ano", "avisos")),
    ("«pieza»: ante el lector, «artículo»", re.compile(r"\b[Pp]iezas?\b"), ()),
    ("«el diario cuenta»: mejor «publica» o «recoge»",
     re.compile(r"\b(?:[Ee]l|[Ee]ste) diario (?:cuenta|contó|contaba|ha contado|contará)\b"), ()),
    ("«app», «online» o «link»: mejor «aplicación», «en línea», «enlace»", re.compile(r"\b(?:apps?|online|links?)\b"), ()),
    ("«AI»: en castellano, «IA»", re.compile(r"\b(?:la|una|de la|con la|por la) AI\b"), ()),
    ("condicional de rumor: mejor «según…, ha…»",
     re.compile(r"\bhabrían? (?:lanzado|presentado|anunciado|publicado|desarrollado|comprado|adquirido|filtrado|cerrado|despedido)\b"), ()),
    ("porcentaje sin espacio: «25 %»", re.compile(r"\d%"), ()),
]
URL = re.compile(r"\]\([^)]*\)|https?://\S+|pieza:\S+")


def inglesa(t):
    """Una frase inglesa: no el título enlazado de una obra («[The components…](…)»), que va en su idioma, ni
    un nombre propio con una sola palabra corriente («Ask the Three Questions»)."""
    if t.lstrip().startswith("["):
        return False
    p = re.findall(r"[A-Za-z']+", t)
    comunes = sum(x.lower() in INGLES for x in p)
    return len(p) >= 3 and comunes >= 2 and comunes / len(p) >= 0.2 and not re.search(r"[áéíóúñçàèòïül·]", t.lower())


def revisar(f, castellano):
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError):
        return []
    out = []
    for ruta, t in autoria.textos(d):
        for fr in autoria.frases(t):
            if castellano and QUIEN.search(CITA.sub("", fr)):
                out.append(f"{f.relative_to(RAIZ)} · {ruta} · «quien» relativo · «{fr.strip()[:300]}»")
            if castellano:
                limpio = URL.sub(" ", CITA.sub("", fr))
                for nombre, expr, fuera in NORMAS:
                    if f.parent.name not in fuera and expr.search(limpio):
                        out.append(f"{f.relative_to(RAIZ)} · {ruta} · {nombre} · «{fr.strip()[:300]}»")
            for m in CITA.finditer(fr):
                cita = m.group(1) or m.group(2) or ""
                if inglesa(cita) and not TRADUCIDA.match(fr[m.end():]):
                    out.append(f"{f.relative_to(RAIZ)} · {ruta} · cita solo en inglés: {m.group(0)[:120]} · «{fr.strip()[:300]}»")
    return out


def main():
    if "--todo" in sys.argv:
        fs = sorted(f for s in SECCIONES for c in IDIOMAS for f in (RAIZ / f"{s}{c}").glob("20*.json"))
        fs += sorted((RAIZ / "avisos").glob("20*.json"))
    else:
        fecha = sys.argv[sys.argv.index("--dia") + 1]
        sig = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
        fs = [RAIZ / f"{s}{c}" / f"{fecha}.json" for s in SECCIONES for c in IDIOMAS] + [RAIZ / "avisos" / f"{sig}.json"]
        fs = [f for f in fs if f.exists()]
    hallado = [h for f in fs for h in revisar(f, castellano=f.parent.name in SECCIONES or f.parent.name == "avisos")]
    print("\n".join(hallado) if hallado else f"revisar-estilo: nada que corregir ({len(fs)} archivos)")
    return 4 if hallado else 0


if __name__ == "__main__":
    sys.exit(main())
