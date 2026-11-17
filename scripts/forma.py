#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La forma de las piezas, sin IA: lo que un agente deja con otra forma y tiene arreglo sin perder nada.

    scripts/forma.py ARCHIVO [ARCHIVO …]

El cuerpo de una pieza es una lista de párrafos. Si llega como un solo texto, con los párrafos separados por
líneas en blanco, se parte y se guarda como lista: con un texto, el generador pinta una letra por párrafo y la
comprobación de las traducciones las quita todas (17-11-2026, ADR 0077). Lo mismo si un elemento de la lista
trae dos párrafos pegados o está vacío. Lo llama `traducir` antes de cada traducción (scripts/traducir.sh).
Dice lo que cambia y lo que no sabe arreglar, y sale con 0; un archivo que no está o no es JSON se deja como está.
"""
import json
import pathlib
import re
import sys


def parrafos(cuerpo):
    """El cuerpo como lista de párrafos, venga como venga: un texto seguido se parte por las líneas en blanco, y
    en una lista de textos, también cada elemento. Lo que no es ni texto ni lista de textos vuelve como está."""
    if isinstance(cuerpo, str):
        return [x.strip() for x in re.split(r"\n\s*\n", cuerpo) if x.strip()]
    if isinstance(cuerpo, list) and all(isinstance(x, str) for x in cuerpo):
        return [y for x in cuerpo for y in parrafos(x)]
    return cuerpo


def arreglar(d):
    """Arregla las piezas de un número en el propio diccionario. Devuelve lo que ha cambiado."""
    cambios = []
    if not isinstance(d, dict):
        return cambios
    for p in d.get("piezas") or []:
        if not isinstance(p, dict) or "cuerpo" not in p:
            continue
        antes, ahora = p["cuerpo"], parrafos(p["cuerpo"])
        if ahora != antes:
            p["cuerpo"] = ahora
            como = "era un texto seguido" if isinstance(antes, str) else "traía párrafos pegados o vacíos"
            cambios.append(f'{p.get("id")}: el cuerpo {como}; ahora, {len(ahora)} párrafos')
        elif not (isinstance(ahora, list) and all(isinstance(x, str) for x in ahora)):
            cambios.append(f'{p.get("id")}: SIN ARREGLO: el cuerpo no es una lista de párrafos ({type(antes).__name__})')
    return cambios


def main():
    for nombre in sys.argv[1:]:
        f = pathlib.Path(nombre)
        try:
            texto = f.read_text()
            d = json.loads(texto)
        except (OSError, ValueError):
            continue
        cambios = arreglar(d)
        if any("SIN ARREGLO" not in c for c in cambios):
            sangria = 1 if texto.startswith("{\n \"") else 2
            f.write_text(json.dumps(d, ensure_ascii=False, indent=sangria) + "\n")
        for c in cambios:
            print(f"forma: {nombre}: {c}")


if __name__ == "__main__":
    main()
