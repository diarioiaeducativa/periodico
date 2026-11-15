#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Dos normas de estilo de Juanjo que se pueden comprobar sin IA (ADR 0067), en lo escrito cada noche.

    scripts/revisar-estilo.py --dia AAAA-MM-DD   lo escrito esa noche, en castellano y en las traducciones no inglesas
    scripts/revisar-estilo.py --todo             todo lo publicado (para medir)

1. **Sin el relativo «quien»** con el sentido de «la persona que» (15-11-2026: «no quiero que se use quien o
   quienes en este sentido»). Solo en castellano: allí el relativo no lleva tilde y el interrogativo sí
   («¿quién?»), así que basta con buscar la palabra sin tilde. Las citas literales no se tocan.
2. **Ninguna cita solo en inglés en una edición que no es inglesa** (15-11-2026: «No debe haber fragmentos solo en
   inglés en idioma no inglés»): la cita va traducida o con su traducción al lado, entre paréntesis. Una cita es
   inglesa si al menos una de cada cinco de sus palabras es de las más corrientes del inglés.
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

SECCIONES = ("ediciones", "reportajes", "biblioteca", "hace-un-ano", "repositorio")
IDIOMAS = ("", "-ca", "-gl", "-eu")   # el inglés no: allí una cita inglesa es su idioma
QUIEN = re.compile(r"\b[Qq]uien(es)?\b")
CITA = re.compile(r"«([^»]*)»|“([^”]*)”")
INGLES = set("the an and or of to in for is are was were be been will would need your you we they with not that "
             "this these those by on as it its can could may should must have has had their our from at which who "
             "what when how does did if than more most only also into about".split())
TRADUCIDA = re.compile(r"^\s*\(\s*[«“]")   # la traducción, al lado: «…» («…»)


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
