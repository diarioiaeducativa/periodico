#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Que el corrector de estilo (encargos/pasos/36-corrector-estilo.md, ADR 0083) solo ha cambiado cómo se dice, no
lo que se dice.

    scripts/comprobar-corrector.py ANTES.json DESPUES.json

Compara la edición de antes y la de después: los campos que no son texto (id, sección, fuentes, mensaje…) tienen
que ser iguales, y en cada texto (antetítulo, titular, entradilla, cuerpo y breves) tienen que seguir las mismas
direcciones de los enlaces, las mismas citas entre comillas y todas las cifras que había; solo se pueden añadir las de
una fecha («el 14 de noviembre», «el jueves 12»), al cambiar «hoy» o «ayer» por el día. Sale con 0 si todo sigue igual y
con 4 si no, diciendo qué ha cambiado; quien lo llama vuelve entonces a la versión de antes.
"""
import json
import re
import sys

TEXTO = ("antetitulo", "titular", "entradilla", "cuerpo", "texto")
CIFRA = re.compile(r"\d+(?:[.,]\d+)*")
ENLACE = re.compile(r"\]\(([^)\s]+)\)|(https?://[^\s)\]»]+)")
CITA = re.compile(r"«([^»]*)»|“([^”]*)”")


def sin_texto(x):
    """El objeto sin los campos de texto, para comparar lo demás."""
    if isinstance(x, dict):
        return {k: sin_texto(v) for k, v in x.items() if k not in TEXTO}
    if isinstance(x, list):
        return [sin_texto(v) for v in x]
    return x


def textos(x, ruta=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in TEXTO:
                yield f"{ruta}.{k}".lstrip("."), " ".join(v) if isinstance(v, list) else str(v or "")
            else:
                yield from textos(v, f"{ruta}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from textos(v, f"{ruta}[{i}]")


MESES = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre"
FECHA = re.compile(rf"\b(\d{{1,2}}) de (?:{MESES})(?: de (\d{{4}}))?|\b(?:lunes|martes|miércoles|jueves|viernes|sábado|domingo) (\d{{1,2}})\b")


def de_fecha(t):
    return [n for m in FECHA.finditer(t) for n in m.groups() if n]


def huella(t):
    """Lo que no puede cambiar en un texto: las cifras, los enlaces y las citas (las de las citas, enteras)."""
    return (sorted(CIFRA.findall(t)), sorted(a or b for a, b in ENLACE.findall(t)),
            sorted(a or b for a, b in CITA.findall(t)))


def main():
    antes, despues = (json.load(open(f, encoding="utf-8")) for f in sys.argv[1:3])
    fallos = []
    if sin_texto(antes) != sin_texto(despues):
        fallos.append("ha cambiado algo que no es texto (id, sección, fuentes, mensaje, número de piezas o breves…)")
    a, d = dict(textos(antes)), dict(textos(despues))
    for ruta in sorted(set(a) | set(d)):
        ha, hd = huella(a.get(ruta, "")), huella(d.get(ruta, ""))
        quitadas = list(ha[0])
        for n in hd[0]:
            if n in quitadas:
                quitadas.remove(n)
        nuevas = list(hd[0])
        for n in ha[0]:
            if n in nuevas:
                nuevas.remove(n)
        fechas = de_fecha(d.get(ruta, ""))
        if quitadas or any(n not in fechas for n in nuevas):
            fallos.append(f"{ruta}: han cambiado las cifras (quitadas {quitadas}, nuevas {nuevas})")
        for nombre, x, y in zip(("los enlaces", "las citas"), ha[1:], hd[1:]):
            if x != y:
                fallos.append(f"{ruta}: han cambiado {nombre} ({sorted(set(x) - set(y))} → {sorted(set(y) - set(x))})")
    print("\n".join(fallos) if fallos else "comprobar-corrector: solo ha cambiado la redacción")
    return 4 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
