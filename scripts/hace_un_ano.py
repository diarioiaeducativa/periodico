#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""«Hace un año» (ADR 0040): lo que se hablaba en los grupos el mismo día del año anterior y lo que ha
cambiado desde entonces.

    scripts/hace_un_ano.py entrada <datos del bot> FECHA    prepara hace-un-ano-entrada/FECHA.md
    scripts/hace_un_ano.py comprobar FECHA                  comprueba hace-un-ano/FECHA.json

FECHA es la de las conversaciones del número, como en noche.sh; el número sale al día siguiente, y
«hace un año» se cuenta desde ese día, el que ve el lector: para FECHA 2026-11-09, sale el 10 y mira los
mensajes del 10 de noviembre de 2025. Van también los del día anterior y el siguiente, por si ese día no
da para nada. Sin IA: solo ordena y comprueba. «entrada» sale con 3 si los tres días están vacíos;
«comprobar», con 1 y lo que falla."""
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from preparar import NOMBRES, cargar, fmt  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MIN_PALABRAS, MAX_PALABRAS = 150, 250
SECCION = "hace-un-ano"
DIAS_SIN_REPETIR = 30


def objetivo(fecha):
    """El mismo día del año anterior al de publicación (el 29 de febrero, el 28)."""
    sale = datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)
    try:
        return sale.replace(year=sale.year - 1)
    except ValueError:
        return sale.replace(year=sale.year - 1, day=28)


def entrada(base, fecha):
    msgs = cargar(pathlib.Path(base))
    dia = objetivo(fecha)
    dias = [(dia, "HACE UN AÑO JUSTO: el día que toca"),
            (dia - datetime.timedelta(days=1), "el día anterior, solo si el día justo no da para nada"),
            (dia + datetime.timedelta(days=1), "el día siguiente, solo si el día justo no da para nada")]
    partes = [f"# Mensajes de los grupos de hace un año, para el número que sale el "
              f"{(datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()}\n"]
    total = 0
    for d, nota in dias:
        partes.append(f"\n# {d.isoformat()} — {nota}\n")
        for g, (nom, url) in NOMBRES.items():
            hoy = [m for m in msgs[g] if m["fecha"].startswith(d.isoformat())]
            total += len(hoy)
            partes.append(f"\n## {nom} ({url}) — clave {g} — {len(hoy)} mensajes\n")
            partes += [fmt(m) for m in hoy]
    # Lo ya contado en «Hace un año» el último mes, para no repetir tema: en dos días seguidos se puede estar
    # hablando de lo mismo (en la prueba del 09-11-2026, dos piezas seguidas sobre Veo y Gemini Omni)
    hoy = datetime.date.fromisoformat(fecha)
    ya = []
    for f in sorted((RAIZ / SECCION).glob("*.json")):
        try:
            if not 0 < (hoy - datetime.date.fromisoformat(f.stem)).days <= DIAS_SIN_REPETIR:
                continue
            for p in json.loads(f.read_text()).get("piezas") or []:
                ya.append(f'- {f.stem}: {p.get("titular", "")} — {p.get("entradilla", "")}')
        except (ValueError, OSError):
            continue
    partes.insert(1, "\n# Ya contado en «Hace un año» el último mes: no repitas su tema ni su producto\n\n"
                  + ("\n".join(ya) if ya else "(nada todavía)") + "\n")
    destino = RAIZ / "hace-un-ano-entrada" / f"{fecha}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n".join(partes))
    print(f"hace un año ({dia.isoformat()} ±1): {total} mensajes")
    return 0 if total else 3


def palabras(t):
    t = re.sub(r"\]\([^)]*\)", "]", t)   # el destino de los enlaces no cuenta
    return len(re.findall(r"\w+", t))


def comprobar(fecha):
    try:
        d = json.loads((RAIZ / SECCION / f"{fecha}.json").read_text())
    except (OSError, ValueError):
        return ["no está o no es un JSON válido"]
    if not d.get("hay_pieza"):
        return []
    ps = d.get("piezas") or []
    if len(ps) != 1:
        return ["tiene que haber una sola pieza"]
    p, malos = ps[0], []
    for campo in ("id", "titular", "entradilla", "fecha_original"):
        if not (p.get(campo) or "").strip():
            malos.append(f"falta {campo}")
    if p.get("seccion") != SECCION:
        malos.append(f"la sección tiene que ser {SECCION}")
    if p.get("grupo") not in NOMBRES:
        malos.append("falta el grupo")
    m = p.get("mensaje") or {}
    if m.get("grupo") not in NOMBRES or not m.get("id"):
        malos.append("falta el mensaje de hace un año")
    cuerpo = p.get("cuerpo") or []
    if not cuerpo or not all(isinstance(x, str) and x.strip() for x in cuerpo):
        malos.append("falta el cuerpo")
    n = palabras(" ".join([p.get("entradilla", "")] + cuerpo))
    if not MIN_PALABRAS <= n <= MAX_PALABRAS:
        malos.append(f"tiene {n} palabras (de {MIN_PALABRAS} a {MAX_PALABRAS}, con la entradilla)")
    try:
        lejos = abs((datetime.date.fromisoformat(p.get("fecha_original", "")) - objetivo(fecha)).days)
        if lejos > 1:
            malos.append("la fecha original no es de hace un año (±1 día)")
    except ValueError:
        malos.append("la fecha original no es una fecha")
    return malos


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "entrada":
        sys.exit(entrada(sys.argv[2], sys.argv[3]))
    if orden == "comprobar":
        m = comprobar(sys.argv[2])
        for linea in m:
            print(f"hace un año: {linea}")
        sys.exit(1 if m else 0)
    print(__doc__)
    sys.exit(2)
