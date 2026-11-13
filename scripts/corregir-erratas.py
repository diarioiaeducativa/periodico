#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Corrige, sin IA, las erratas que siguen una regla fija y avisa de los titulares largos (ADR 0059).

Son faltas que los agentes repiten y que un programa arregla sin riesgo:

- en castellano, «y» delante de una palabra que empieza por el sonido «i» («y instrucciones» → «e
  instrucciones») y «o» delante de una que empieza por «o» («o otro» → «u otro»);
- en inglés, las comillas españolas («…»), que el traductor arrastra del original: pasan a “…”.

    scripts/corregir-erratas.py                  todo lo escrito
    scripts/corregir-erratas.py --dia 2026-11-12 solo los archivos de ese día
    scripts/corregir-erratas.py --mirar          dice lo que cambiaría, sin tocar nada

Cambia solo esos caracteres dentro del archivo, sin reescribirlo: el resto queda byte a byte como estaba.
Escribe una línea por cambio. De los titulares de más de 90 caracteres solo avisa: acortarlos es cosa del
redactor. Termina siempre con 0: no impide que el número salga.

No toca: «y» ante diptongo («y hierro», «y iones»), ni ante palabras que no empiezan por el sonido «i»
aunque se escriban con ella («y iPhone», «y iOS»: la segunda letra en mayúscula las delata).
"""
import argparse
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CASTELLANO = ["ediciones", "biblioteca", "hace-un-ano", "reportajes", "repositorio", "comentario-semana",
              "vinetas", "multimedia", "reserva"]
INGLES = [c + "-en" for c in CASTELLANO if c != "reserva"] + ["ilustraciones-en"]
TITULAR_MAX = 90

# «y» + palabra en minúsculas que empieza por i o hi sin diptongo detrás
Y_ANTE_I = re.compile(r"\b([yY]) (h?i(?![aeoáéó])[a-zñáéíóúü]+)")
O_ANTE_O = re.compile(r"\b([oO]) (h?o[a-zñáéíóúü]+)")


def castellano(texto):
    cambios = []

    def pon(nueva):
        def f(m):
            letra = nueva.upper() if m.group(1).isupper() else nueva
            cambios.append(f"«{m.group(0)}» → «{letra} {m.group(2)}»")
            return f"{letra} {m.group(2)}"
        return f

    texto = Y_ANTE_I.sub(pon("e"), texto)
    texto = O_ANTE_O.sub(pon("u"), texto)
    return texto, cambios


def ingles(texto):
    n = texto.count("«") + texto.count("»")
    if not n:
        return texto, []
    return texto.replace("«", "“").replace("»", "”"), [f"{n} comillas españolas → inglesas"]


def titulares(x):
    """Los titulares de un JSON, estén donde estén."""
    if isinstance(x, dict):
        if isinstance(x.get("titular"), str):
            yield x["titular"]
        for v in x.values():
            yield from titulares(v)
    elif isinstance(x, list):
        for v in x:
            yield from titulares(v)


def archivos(carpetas, dia):
    for c in carpetas:
        for f in sorted((RAIZ / c).rglob("*")) if (RAIZ / c).is_dir() else []:
            if f.suffix in (".json", ".svg") and (not dia or dia in f.name):
                yield f


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dia", help="solo los archivos de ese día (AAAA-MM-DD)")
    ap.add_argument("--mirar", action="store_true", help="no cambia nada")
    a = ap.parse_args()
    for carpetas, arregla in ((CASTELLANO, castellano), (INGLES, ingles)):
        for f in archivos(carpetas, a.dia):
            antes = f.read_text(encoding="utf-8")
            despues, cambios = arregla(antes)
            for c in cambios:
                print(f"{'cambiaría' if a.mirar else 'corregido'}\t{f.relative_to(RAIZ)}\t{c}")
            if cambios and not a.mirar:
                f.write_text(despues, encoding="utf-8")
    for f in archivos([c for c in CASTELLANO if c != "reserva"], a.dia):
        if f.suffix != ".json":
            continue
        try:
            datos = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for t in titulares(datos):
            if len(t) > TITULAR_MAX and a.dia:   # sin día no avisa: lo publicado se acepta como salió
                print(f"titular largo\t{f.relative_to(RAIZ)}\t{len(t)} caracteres: {t}")


if __name__ == "__main__":
    main()
