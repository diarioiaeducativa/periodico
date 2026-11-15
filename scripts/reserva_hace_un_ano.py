#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""«Hace un año» escrito por adelantado, parte del número de reserva (ADR 0068).

    scripts/reserva_hace_un_ano.py pendientes [N]   las fechas de los próximos ADELANTO días que aún no lo tienen (N como mucho)
    scripts/reserva_hace_un_ano.py guardar FECHA    pasa a reserva/hace-un-ano/FECHA/ lo que hace-un-ano.sh escribió para esa fecha
    scripts/reserva_hace_un_ano.py usar FECHA       lo pone en su sitio, si el número de esas conversaciones no lo tiene
    scripts/reserva_hace_un_ano.py caducar          quita los de fechas ya pasadas

«Hace un año» solo depende de los mensajes de hace un año, así que se puede escribir antes: reserva.sh deja escritos
los de los próximos siete días, y la noche de cada número coge el suyo (hace-un-ano.sh) en lugar de escribirlo; si no
está, lo escribe como siempre. Así, si la noche falla, el número de reserva lo lleva igual. FECHA es la de las
conversaciones del número, como en noche.sh. Se guarda con su fecha de verdad: no hay clave provisional.
"""
import datetime
import json
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SECCION = "hace-un-ano"
RESERVA = RAIZ / "reserva" / SECCION
ADELANTO = 7
TRADUCCIONES = ("ca", "gl", "eu", "en")


def carpetas():
    return [SECCION] + [f"{SECCION}-{c}" for c in TRADUCCIONES]


def dibujos():
    return ["ilustraciones"] + [f"ilustraciones-{c}" for c in TRADUCCIONES]


def tiene(fecha):
    try:
        return bool(json.loads((RAIZ / SECCION / f"{fecha}.json").read_text()).get("piezas"))
    except (OSError, ValueError):
        return False


def pendientes(n=ADELANTO, hoy=None):
    """Las fechas de conversaciones de las próximas noches (desde la de esta noche, que es la de hoy) sin «Hace un
    año» guardado."""
    hoy = hoy or datetime.date.today()
    out = []
    for i in range(ADELANTO):
        f = (hoy + datetime.timedelta(days=i)).isoformat()
        if not (RESERVA / f / f"{SECCION}.json").exists() and not tiene(f):
            out.append(f)
    return out[:n]


def guardar(fecha):
    f = RAIZ / SECCION / f"{fecha}.json"
    if not tiene(fecha):
        print(f"«Hace un año» por adelantado: {fecha} no tiene pieza que guardar", file=sys.stderr)
        return 1
    ids = [p["id"] for p in json.loads(f.read_text()).get("piezas") or []]
    dest = RESERVA / fecha
    dest.mkdir(parents=True, exist_ok=True)
    for c in carpetas():
        g = RAIZ / c / f"{fecha}.json"
        if g.exists():
            shutil.move(str(g), dest / f"{c}.json")
    for c in dibujos():
        for i in ids:
            g = RAIZ / c / f"{fecha}-{i}.svg"
            if g.exists():
                (dest / c).mkdir(exist_ok=True)
                shutil.move(str(g), dest / c / g.name)
    print(f"«Hace un año» por adelantado: guardado el del {fecha}")
    return 0


def usar(fecha):
    """Lo pone en su sitio si el número no lo tiene. Devuelve «Hace un año FECHA» o None."""
    d = RESERVA / fecha
    if tiene(fecha) or not (d / f"{SECCION}.json").exists():
        return None
    for c in carpetas():
        g = d / f"{c}.json"
        if g.exists():
            (RAIZ / c).mkdir(exist_ok=True)
            shutil.move(str(g), RAIZ / c / f"{fecha}.json")
    for c in dibujos():
        for g in (d / c).glob("*.svg") if (d / c).exists() else []:
            (RAIZ / c).mkdir(exist_ok=True)
            shutil.move(str(g), RAIZ / c / g.name)
    shutil.rmtree(d)
    print(f"«Hace un año» por adelantado: puesto el del {fecha}")
    return f"Hace un año {fecha}"


def caducar(hoy=None):
    """Los de fechas cuya noche ya pasó sin usarlos (la noche falló y la reserva no llegó a ponerlos)."""
    hoy = hoy or datetime.date.today()
    for d in sorted(RESERVA.glob("20*")):
        try:
            if datetime.date.fromisoformat(d.name) < hoy - datetime.timedelta(days=1):
                shutil.rmtree(d)
                print(f"«Hace un año» por adelantado: quitado el del {d.name}, que no llegó a usarse")
        except ValueError:
            continue


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "pendientes":
        print(" ".join(pendientes(int(sys.argv[2]) if len(sys.argv) > 2 else ADELANTO)))
    elif orden == "guardar":
        sys.exit(guardar(sys.argv[2]))
    elif orden == "usar":
        sys.exit(0 if usar(sys.argv[2]) else 4)
    elif orden == "caducar":
        caducar()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
