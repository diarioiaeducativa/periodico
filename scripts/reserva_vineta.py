#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La viñeta de reserva, parte del número de reserva (ADR 0068).

    scripts/reserva_vineta.py cuantas             cuántas viñetas de reserva hay listas
    scripts/reserva_vineta.py faltan              1 si no queda ninguna vigente (toca escribir otra), 0 si no
    scripts/reserva_vineta.py clave               una clave libre para escribir la siguiente
    scripts/reserva_vineta.py guardar CLAVE       pasa a reserva/vinetas/CLAVE/ lo que vineta-reserva.sh escribió con esa clave
    scripts/reserva_vineta.py caducar             retira las que pasan de CADUCA días
    scripts/reserva_vineta.py usar AAAA-MM-DD     la pone en el número de esas conversaciones, si no tiene viñeta

Una tira de Tiza y Algoritmo sobre un asunto que no caduca, escrita con antelación (encargos/pasos/30-vineta-reserva.md)
y traducida, que no sale de ninguna noticia: la web no pone «A partir de…» (lleva "reserva": true). Se usa el día
en que fallan el guionista o el juez, o en que no hay piezas de las que sacar una. Usarla no necesita IA.
"""
import datetime
import json
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESERVA = RAIZ / "reserva" / "vinetas"
CADUCA = 60          # días sin usarse: se retira y se escribe otra, como las piezas de reserva
PREFIJO = "2099-03-"  # las claves provisionales: una fecha que nunca será un número
TRADUCCIONES = ("ca", "gl", "eu", "en")


def escrito(d):
    try:
        return datetime.date.fromisoformat((d / "escrito.txt").read_text().strip())
    except (OSError, ValueError):
        return datetime.date.fromtimestamp((d / "vinetas.json").stat().st_mtime)


def valida(f):
    try:
        return bool(json.loads(f.read_text()).get("elegida"))
    except (OSError, ValueError):
        return False


def listas(hoy=None):
    """Las vigentes, la más antigua primero (se gasta antes la que más lleva esperando)."""
    hoy = hoy or datetime.date.today()
    return [d for d in sorted(RESERVA.glob(PREFIJO + "*"), key=escrito)
            if valida(d / "vinetas.json") and (hoy - escrito(d)).days <= CADUCA]


def clave_libre():
    usadas = {d.name for d in RESERVA.glob(PREFIJO + "*")} | {f.stem for f in (RAIZ / "vinetas").glob(PREFIJO + "*.json")}
    for n in range(1, 29):
        k = f"{PREFIJO}{n:02d}"
        if k not in usadas:
            return k
    raise SystemExit("reserva de viñetas: no quedan claves libres")


def guardar(clave):
    origen = RAIZ / "vinetas" / f"{clave}.json"
    if not valida(origen):
        print(f"reserva de viñetas: {clave} no tiene viñeta que guardar", file=sys.stderr)
        for c in [""] + [f"-{x}" for x in TRADUCCIONES]:
            (RAIZ / f"vinetas{c}" / f"{clave}.json").unlink(missing_ok=True)
        return 1
    dest = RESERVA / clave
    dest.mkdir(parents=True, exist_ok=True)
    for c in [""] + [f"-{x}" for x in TRADUCCIONES]:
        f = RAIZ / f"vinetas{c}" / f"{clave}.json"
        if f.exists():
            shutil.move(str(f), dest / f"vinetas{c}.json")
    (dest / "escrito.txt").write_text(datetime.date.today().isoformat() + "\n")
    print(f"reserva de viñetas: guardada {clave}; hay {len(listas())}")
    return 0


def caducar():
    hoy = datetime.date.today()
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        if not valida(d / "vinetas.json") or (hoy - escrito(d)).days > CADUCA:
            viejo = RESERVA / "retiradas" / d.name
            viejo.parent.mkdir(parents=True, exist_ok=True)
            shutil.rmtree(viejo, ignore_errors=True)
            shutil.move(str(d), viejo)
            print(f"reserva de viñetas: {d.name} retirada")


def usar(fecha):
    """Pone la viñeta de reserva si el número no tiene una. Devuelve «viñeta CLAVE» o None."""
    if valida(RAIZ / "vinetas" / f"{fecha}.json"):
        return None
    caducar()
    ls = listas()
    if not ls:
        print("reserva de viñetas: el número sale sin viñeta y no queda ninguna de reserva", file=sys.stderr)
        return None
    d = ls[0]
    clave = d.name
    for c in [""] + [f"-{x}" for x in TRADUCCIONES]:
        f = d / f"vinetas{c}.json"
        if f.exists():
            v = json.loads(f.read_text().replace(clave, fecha))
            v["fecha"] = fecha
            v["reserva"] = True
            g = RAIZ / f"vinetas{c}" / f"{fecha}.json"
            g.parent.mkdir(exist_ok=True)
            g.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
    shutil.rmtree(d)
    print(f"reserva de viñetas: el número del {fecha} sale con la viñeta de reserva {clave}")
    return f"viñeta {clave}"


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "cuantas":
        print(len(listas()))
    elif orden == "faltan":
        caducar()
        print(0 if listas() else 1)
    elif orden == "clave":
        print(clave_libre())
    elif orden == "guardar":
        sys.exit(guardar(sys.argv[2]))
    elif orden == "caducar":
        caducar()
    elif orden == "usar":
        sys.exit(0 if usar(sys.argv[2]) else 4)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
