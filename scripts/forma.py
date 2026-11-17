#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La forma de las piezas, sin IA: lo que un agente deja con otra forma y tiene arreglo sin perder nada.

    scripts/forma.py ARCHIVO [ARCHIVO …]

El cuerpo de una pieza es una lista de párrafos. Si llega como un solo texto, con los párrafos separados por
líneas en blanco, se parte y se guarda como lista: con un texto, el generador pinta una letra por párrafo y la
comprobación de las traducciones las quita todas (17-11-2026, ADR 0077). Dice lo que cambia y sale con 0; un
archivo que no está o no es JSON se deja como está.
"""
import json
import pathlib
import re
import sys


def parrafos(cuerpo):
    """El cuerpo como lista de párrafos, venga como venga."""
    if isinstance(cuerpo, str):
        return [x.strip() for x in re.split(r"\n\s*\n", cuerpo) if x.strip()]
    return cuerpo


def arreglar(d):
    """Arregla las piezas de un número en el propio diccionario. Devuelve lo que ha cambiado."""
    cambios = []
    if not isinstance(d, dict):
        return cambios
    for p in d.get("piezas") or []:
        if isinstance(p, dict) and isinstance(p.get("cuerpo"), str):
            p["cuerpo"] = parrafos(p["cuerpo"])
            cambios.append(f'{p.get("id")}: el cuerpo era un texto seguido; ahora, {len(p["cuerpo"])} párrafos')
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
        if cambios:
            sangria = 1 if texto.startswith("{\n \"") else 2
            f.write_text(json.dumps(d, ensure_ascii=False, indent=sangria) + "\n")
            for c in cambios:
                print(f"forma: {nombre}: {c}")


if __name__ == "__main__":
    main()
