#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las piezas de reserva: el plan B para que no haya ningún día sin número (ADR 0021).

    scripts/reserva.py cuantas             cuántas piezas de reserva hay listas
    scripts/reserva.py faltan              cuántas faltan para tener OBJETIVO listas
    scripts/reserva.py clave               una clave libre para escribir la siguiente
    scripts/reserva.py guardar CLAVE       pasa a reserva/CLAVE/ lo que repositorio.sh escribió con esa clave
    scripts/reserva.py usar AAAA-MM-DD [fallo|relleno]
                                           pone una pieza de reserva en el número de esas conversaciones

Una pieza de reserva es un artículo del fondo del Repositorio de VCE («Del fondo del repositorio»):
no caduca. La escribe repositorio.sh, con su documentalista, su revisor y su traductor, con una
clave de fecha provisional (2099-01-NN) que no choca con ningún número; aquí se guarda en
reserva/CLAVE/ con su captura. Usarla no necesita IA: se cambia la clave por la fecha del día en
el JSON y en el nombre de la captura, se pasa a repositorio/ y se marca la edición con
"reserva": "fallo" o "relleno". Con «fallo» (la redacción no pudo preparar el número) la web lo
dice y la noche siguiente recupera las conversaciones de ese día (noche.sh); con «relleno» (no
había nada que contar y tampoco salió nada del repositorio) no hay nada que recuperar. Si el día
ya tiene piezas (la redacción terminó pero se atascó después), no se añade nada. En los dos casos,
si faltan los avisos de los grupos, se escriben aquí, sin IA.

«usar» sale con 0 si ha puesto la reserva, con 4 si el día ya tenía piezas (no hace falta) y con 3
si no queda ninguna.
"""
import datetime
import json
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESERVA = RAIZ / "reserva"
OBJETIVO = 3          # piezas de reserva que tiene que haber siempre listas
PREFIJO = "2099-01-"  # las claves provisionales: una fecha que nunca será un número


def listas():
    """Las reservas con alguna pieza, la más antigua primero."""
    out = []
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        f = d / "repositorio.json"
        try:
            if json.loads(f.read_text()).get("piezas"):
                out.append(d)
        except (OSError, ValueError):
            pass
    return out


def clave_libre():
    usadas = {d.name for d in RESERVA.glob(PREFIJO + "*")} | \
             {f.stem for c in ("repositorio", "repositorio-borrador") for f in (RAIZ / c).glob(PREFIJO + "*.json")}
    for n in range(1, 32):
        k = f"{PREFIJO}{n:02d}"
        if k not in usadas:
            return k
    raise SystemExit("reserva: no quedan claves libres")


def guardar(clave):
    """De repositorio/ a reserva/CLAVE/. Lo que el documentalista descartó se guarda igual, para que
    repositorio.py no vuelva a proponerlo (cuenta todo reserva/ como ya contado)."""
    dest = RESERVA / clave
    dest.mkdir(parents=True, exist_ok=True)
    for origen, nombre in (("repositorio", "repositorio.json"), ("repositorio-ca", "repositorio-ca.json")):
        f = RAIZ / origen / f"{clave}.json"
        if f.exists():
            shutil.move(str(f), dest / nombre)
    for f in (RAIZ / "repositorio" / "capturas").glob(f"{clave}-*.jpg"):
        (dest / "capturas").mkdir(exist_ok=True)
        shutil.move(str(f), dest / "capturas" / f.name)
    for c in ("repositorio-borrador", "repositorio-entrada"):
        for f in (RAIZ / c).glob(f"{clave}.*"):
            f.unlink()
    ok = (dest / "repositorio.json").exists() and json.loads((dest / "repositorio.json").read_text()).get("piezas")
    print(f"reserva: {clave} {'guardada' if ok else 'sin pieza (solo descartes)'}; listas: {len(listas())}")
    return 0 if ok else 2


def piezas_del_dia(fecha):
    n = 0
    f = RAIZ / "ediciones" / f"{fecha}.json"
    if f.exists():
        d = json.loads(f.read_text())
        n += len(d.get("piezas", [])) if d.get("hay_edicion") else 0
    for c in ("biblioteca", "repositorio"):
        g = RAIZ / c / f"{fecha}.json"
        if g.exists():
            n += len(json.loads(g.read_text()).get("piezas", []))
    return n


def titulares(fecha):
    out = []
    for c in ("ediciones", "biblioteca", "repositorio"):
        g = RAIZ / c / f"{fecha}.json"
        if g.exists():
            d = json.loads(g.read_text())
            if c != "ediciones" or d.get("hay_edicion"):
                out += [p.get("titular", "").rstrip(".") for p in d.get("piezas", []) if p.get("titular")]
    return out


def avisos(fecha, fallo):
    """Los avisos de los grupos sin IA, si el agente no los escribió: los titulares del número y, si
    la redacción falló, que las noticias de ayer salen mañana. El bot les pone la cabecera, el
    enlace y la imagen del número."""
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    f = RAIZ / "avisos" / f"{publica}.json"
    try:
        if json.loads(f.read_text()).get("avisos"):
            return
    except (OSError, ValueError):
        pass
    puntos = titulares(fecha)[:3 if not fallo else 2]
    if fallo:
        puntos.append("Las noticias de los grupos de ayer no han podido salir hoy por un fallo de la redacción del diario: salen mañana, junto con las de hoy")
    if len(puntos) < 2:
        puntos.append("Todas las piezas, con sus fuentes, en el diario")
    f.parent.mkdir(exist_ok=True)
    f.write_text(json.dumps({"fecha": publica, "avisos": {g: {"saludo": "Buenos días.", "puntos": puntos}
                                                           for g in ("chatgpt", "vce", "edumedia")}},
                            ensure_ascii=False, indent=2) + "\n")


def usar(fecha, motivo="fallo"):
    if piezas_del_dia(fecha):
        avisos(fecha, False)
        print(f"reserva: el número del {fecha} ya tiene piezas; no hace falta la reserva")
        return 4
    hay = listas()
    if not hay:
        print("reserva: no queda ninguna pieza de reserva", file=sys.stderr)
        return 3
    r = hay[0]
    clave = r.name
    nuevas = []
    for nombre, destino in (("repositorio.json", "repositorio"), ("repositorio-ca.json", "repositorio-ca")):
        f = r / nombre
        if not f.exists():
            continue
        d = json.loads(f.read_text().replace(clave, fecha))   # la fecha y el nombre de la captura
        d["fecha"] = fecha
        g = RAIZ / destino / f"{fecha}.json"
        if g.exists():   # el día ya tenía un archivo (solo descartes): se le añaden las piezas
            viejo = json.loads(g.read_text())
            viejo["piezas"] = viejo.get("piezas", []) + d.get("piezas", [])
            d = viejo
        g.parent.mkdir(exist_ok=True)
        g.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        if destino == "repositorio":
            nuevas = d.get("piezas", [])
    for f in (r / "capturas").glob("*.jpg"):
        (RAIZ / "repositorio" / "capturas").mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), RAIZ / "repositorio" / "capturas" / f.name.replace(clave, fecha))
    ed = RAIZ / "ediciones" / f"{fecha}.json"
    d = json.loads(ed.read_text()) if ed.exists() else {"fecha": fecha, "hay_edicion": False, "piezas": [], "breves": []}
    d["reserva"] = motivo
    d["motivo"] = (d.get("motivo") + " · " if d.get("motivo") else "") + f"número con la pieza de reserva {clave} ({motivo})"
    ed.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    avisos(fecha, motivo == "fallo")
    shutil.rmtree(r)
    print(f"reserva: el número del {fecha} sale con la reserva {clave} ({', '.join(p['id'] for p in nuevas)}); quedan {len(listas())}")
    return 0


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "cuantas":
        print(len(listas()))
    elif orden == "faltan":
        print(max(0, OBJETIVO - len(listas())))
    elif orden == "clave":
        print(clave_libre())
    elif orden == "guardar" and len(sys.argv) == 3:
        sys.exit(guardar(sys.argv[2]))
    elif orden == "usar" and len(sys.argv) in (3, 4) and (sys.argv[3:] or ["fallo"])[0] in ("fallo", "relleno"):
        sys.exit(usar(sys.argv[2], (sys.argv[3:] or ["fallo"])[0]))
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
