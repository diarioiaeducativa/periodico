#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El reportaje de reserva: el domingo siempre hay reportaje (ADR 0028).

    scripts/reserva_reportaje.py cuantos         cuántos reportajes de reserva hay listos y vigentes
    scripts/reserva_reportaje.py faltan          cuántos faltan para tener OBJETIVO
    scripts/reserva_reportaje.py clave           una clave libre para escribir el siguiente
    scripts/reserva_reportaje.py guardar CLAVE   pasa a reserva/reportajes/CLAVE/ lo que reportaje.sh escribió con esa clave
    scripts/reserva_reportaje.py caducar         retira los que pasan de CADUCA días (se escribirá otro)
    scripts/reserva_reportaje.py usar AAAA-MM-DD pone uno en el número del domingo de ese sábado, si no tiene reportaje

Un reportaje de reserva lo escribe reportaje.sh con RESERVA=1, con el mismo jefe de reportajes,
reportero, verificador, ilustrador y traductores que cada sábado, sobre un tema que no caduque en
semanas, con una clave de fecha provisional (2099-02-NN) que no choca con ningún número. Usarlo no
necesita IA: se cambia la clave por la fecha en los JSON y en el nombre de los dibujos. Antes se
comprueba que sus fuentes siguen respondiendo; si demasiadas fallan, se descarta y se usa el
siguiente. Sale con 0 si lo ha puesto, con 4 si ese sábado ya tenía reportaje y con 3 si no queda
ninguno que valga."""
import datetime
import json
import pathlib
import shutil
import sys
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESERVA = RAIZ / "reserva" / "reportajes"
OBJETIVO = 1         # reportajes de reserva que tiene que haber siempre listos
CADUCA = 28          # días: a partir de aquí se descarta y se escribe otro (Juanjo, 06-11-2026)
PREFIJO = "2099-02-"
TRADUCCIONES = ("ca", "gl", "eu", "en")


def escrito(d):
    """La fecha en que se escribió (escrito.txt; si falta, la del archivo)."""
    f = d / "escrito.txt"
    try:
        return datetime.date.fromisoformat(f.read_text().strip())
    except (OSError, ValueError):
        return datetime.date.fromtimestamp((d / "reportajes.json").stat().st_mtime)


def listos(hoy=None):
    """Los reportajes de reserva válidos y vigentes, el más antiguo primero."""
    hoy = hoy or datetime.date.today()
    out = []
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        try:
            if json.loads((d / "reportajes.json").read_text()).get("hay_reportaje") and (hoy - escrito(d)).days <= CADUCA:
                out.append(d)
        except (OSError, ValueError):
            pass
    return out


def clave_libre():
    usadas = {d.name for d in RESERVA.glob(PREFIJO + "*")} | \
             {f.stem.split("-tema")[0] for c in ("reportajes", "reportajes-borrador") for f in (RAIZ / c).glob(PREFIJO + "*.json")}
    for n in range(1, 29):
        k = f"{PREFIJO}{n:02d}"
        if k not in usadas:
            return k
    raise SystemExit("reserva de reportajes: no quedan claves libres")


def guardar(clave):
    """De reportajes/ e ilustraciones/ (y sus traducciones) a reserva/reportajes/CLAVE/."""
    origen = RAIZ / "reportajes" / f"{clave}.json"
    if not origen.exists() or not json.loads(origen.read_text()).get("hay_reportaje"):
        print(f"reserva de reportajes: {clave} no tiene reportaje que guardar", file=sys.stderr)
        for f in [origen] + [RAIZ / f"reportajes-{c}" / f"{clave}.json" for c in TRADUCCIONES]:
            f.unlink(missing_ok=True)
        return 1
    dest = RESERVA / clave
    dest.mkdir(parents=True, exist_ok=True)
    for carpeta in ["reportajes"] + [f"reportajes-{c}" for c in TRADUCCIONES]:
        f = RAIZ / carpeta / f"{clave}.json"
        if f.exists():
            shutil.move(str(f), dest / f"{carpeta}.json")
    for carpeta in ["ilustraciones"] + [f"ilustraciones-{c}" for c in TRADUCCIONES]:
        for f in (RAIZ / carpeta).glob(f"{clave}-*.svg"):
            (dest / carpeta).mkdir(exist_ok=True)
            shutil.move(str(f), dest / carpeta / f.name)
    (dest / "escrito.txt").write_text(datetime.date.today().isoformat() + "\n")
    for f in (RAIZ / "reportajes-borrador").glob(f"{clave}*"):
        f.unlink()
    (RAIZ / "semanas" / f"{clave}.md").unlink(missing_ok=True)
    print(f"reserva de reportajes: guardado {clave}; hay {len(listos())}")
    return 0


def retirar(d, motivo):
    viejo = RESERVA / "retirados" / d.name
    viejo.parent.mkdir(exist_ok=True)
    shutil.rmtree(viejo, ignore_errors=True)
    shutil.move(str(d), viejo)
    (viejo / "motivo.txt").write_text(f"{datetime.date.today().isoformat()}: {motivo}\n")
    print(f"reserva de reportajes: {d.name} retirado ({motivo})")


def caducar():
    hoy = datetime.date.today()
    for d in sorted(RESERVA.glob(PREFIJO + "*")):
        if (d / "reportajes.json").exists() and (hoy - escrito(d)).days > CADUCA:
            retirar(d, f"escrito el {escrito(d)}, pasa de {CADUCA} días")


def responde(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (diario de IA Educativa)"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status < 400
    except Exception:  # noqa: BLE001 — algunas webs no aceptan HEAD: se prueba GET
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (diario de IA Educativa)"})
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.status < 400
        except Exception:  # noqa: BLE001
            return False


def vigente(d):
    """Que sus fuentes sigan ahí: si falla más de una de cada cinco, el tema puede haber cambiado."""
    r = json.loads((d / "reportajes.json").read_text())
    urls = [f["url"] for f in r.get("fuentes", []) if f.get("url", "").startswith("http")][:12]
    if not urls:
        return True, ""
    malas = [u for u in urls if not responde(u)]
    return len(malas) * 5 <= len(urls), f"{len(malas)} de {len(urls)} fuentes no responden"


def usar(fecha):
    """fecha: el sábado (la del número que sale el domingo)."""
    actual = RAIZ / "reportajes" / f"{fecha}.json"
    try:
        if json.loads(actual.read_text()).get("hay_reportaje"):
            print(f"reserva de reportajes: el {fecha} ya tiene reportaje")
            return 4
    except (OSError, ValueError):
        pass
    caducar()
    for d in listos():
        ok, motivo = vigente(d)
        if not ok:
            retirar(d, motivo)
            continue
        clave = d.name
        for f in d.glob("reportajes*.json"):
            r = json.loads(f.read_text().replace(clave, fecha))
            r["fecha"] = fecha
            r["reserva"] = f"escrito el {escrito(d)} como reportaje de reserva ({clave})"
            destino = RAIZ / f.stem / f"{fecha}.json"
            destino.parent.mkdir(exist_ok=True)
            destino.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n")
        for carpeta in d.glob("ilustraciones*"):
            for f in carpeta.glob("*.svg"):
                (RAIZ / carpeta.name).mkdir(exist_ok=True)
                shutil.copy(f, RAIZ / carpeta.name / f.name.replace(clave, fecha))
        shutil.rmtree(d)
        print(f"reserva de reportajes: el domingo del {fecha} sale con el reportaje de reserva {clave}; quedan {len(listos())}")
        return 0
    print("reserva de reportajes: no queda ninguno que valga", file=sys.stderr)
    return 3


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "cuantos":
        print(len(listos()))
    elif orden == "faltan":
        print(max(0, OBJETIVO - len(listos())))
    elif orden == "clave":
        print(clave_libre())
    elif orden == "guardar":
        sys.exit(guardar(sys.argv[2]))
    elif orden == "caducar":
        caducar()
    elif orden == "usar":
        sys.exit(usar(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
