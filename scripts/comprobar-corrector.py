#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Que el corrector de estilo (encargos/pasos/36-corrector-estilo.md, ADR 0083) solo ha cambiado cómo se dice, no
lo que se dice.

    scripts/comprobar-corrector.py ANTES.json DESPUES.json
    scripts/comprobar-corrector.py --arreglar [--registro FECHA-corrector.json] ANTES.json DESPUES.json

Compara la edición de antes y la de después: los campos que no son texto (id, sección, fuentes, mensaje…) tienen
que ser iguales, y en cada texto (antetítulo, titular, entradilla, cuerpo y breves) tienen que seguir las mismas
direcciones de los enlaces, las mismas citas entre comillas y todas las cifras que había. Solo se pueden añadir las
cifras de una fecha («el 14 de noviembre», «el jueves 12»), al cambiar «hoy» o «ayer» por el día, y las que ya estaban
en otro texto del mismo artículo («Genie 4», si el titular ya lo nombraba). Sale con 0 si todo sigue igual y con 4 si
no, diciendo qué ha cambiado; quien lo llama vuelve entonces a la versión de antes.

Con --arreglar, si solo han cambiado datos dentro de algunos textos, esos textos vuelven a la redacción de antes y
los demás se quedan con la corrección: reescribe DESPUES.json, marca en el registro del corrector como «descartado» los
cambios de esos textos y sale con 3. Si ha cambiado algo que no es texto, sale con 4 sin tocar nada (ADR 0083).
"""
import argparse
import copy
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


def articulo(ruta):
    """El artículo o breve al que pertenece un texto: «piezas[2]» para «piezas[2].cuerpo»."""
    m = re.match(r"[^.\[]*\[\d+\]", ruta)
    return m.group(0) if m else ruta


def fallos_por_texto(antes, despues):
    """{ruta: [qué ha cambiado]} de los textos que han cambiado datos."""
    a, d = dict(textos(antes)), dict(textos(despues))
    del_articulo = {}   # las cifras que ya había en cada artículo, en cualquiera de sus textos
    for ruta, t in a.items():
        del_articulo.setdefault(articulo(ruta), set()).update(CIFRA.findall(t))
    fallos = {}
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
        ya = del_articulo.get(articulo(ruta), set())
        if quitadas or any(n not in fechas and n not in ya for n in nuevas):
            fallos.setdefault(ruta, []).append(f"han cambiado las cifras (quitadas {quitadas}, nuevas {nuevas})")
        for nombre, x, y in zip(("los enlaces", "las citas"), ha[1:], hd[1:]):
            if x != y:
                fallos.setdefault(ruta, []).append(f"han cambiado {nombre} ({sorted(set(x) - set(y))} → {sorted(set(y) - set(x))})")
    return fallos


def devolver(antes, despues, malas, ruta=""):
    """Pone en DESPUES la redacción de ANTES en los textos de MALAS (la estructura ya es la misma)."""
    if isinstance(despues, dict):
        for k in despues:
            r = f"{ruta}.{k}".lstrip(".")
            if k in TEXTO:
                if r in malas:
                    despues[k] = copy.deepcopy(antes[k])
            else:
                devolver(antes[k], despues[k], malas, r)
    elif isinstance(despues, list):
        for i, v in enumerate(despues):
            devolver(antes[i], v, malas, f"{ruta}[{i}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("antes")
    ap.add_argument("despues")
    ap.add_argument("--arreglar", action="store_true")
    ap.add_argument("--registro")
    o = ap.parse_args()
    antes, despues = (json.load(open(f, encoding="utf-8")) for f in (o.antes, o.despues))
    if sin_texto(antes) != sin_texto(despues):
        print("ha cambiado algo que no es texto (id, sección, fuentes, mensaje, número de piezas o breves…)")
        return 4
    fallos = fallos_por_texto(antes, despues)
    if not fallos:
        print("comprobar-corrector: solo ha cambiado la redacción")
        return 0
    print("\n".join(f"{r}: {x}" for r, xs in fallos.items() for x in xs))
    if not o.arreglar:
        return 4
    devolver(antes, despues, set(fallos))
    with open(o.despues, "w", encoding="utf-8") as f:
        json.dump(despues, f, ensure_ascii=False, indent=2)
        f.write("\n")
    descartados = 0
    if o.registro:
        try:
            cambios = json.load(open(o.registro, encoding="utf-8"))
            for c in cambios if isinstance(cambios, list) else []:
                campo = str(c.get("campo", ""))
                if any(campo == r or campo.startswith(r + "[") for r in fallos):
                    c["descartado"] = "tocaba datos: vuelve la redacción del revisor"
                    descartados += 1
            with open(o.registro, "w", encoding="utf-8") as f:
                json.dump(cambios, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except (OSError, ValueError, AttributeError):
            pass
    print(f"comprobar-corrector: vuelven a la redacción del revisor {len(fallos)} texto(s): {', '.join(fallos)}"
          + (f" ({descartados} cambio(s) del registro)" if descartados else ""))
    return 3


if __name__ == "__main__":
    sys.exit(main())
