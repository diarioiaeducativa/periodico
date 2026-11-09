#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Sube a Internet Archive los vídeos del diario y sus portadas (ADR 0037).

Un elemento por año, como el boletín: diarioiaeducativa_<año> (el año del vídeo). Si no existe, se
crea con la primera subida y los metadatos de METADATOS; si existe, solo se añaden los archivos.

Para cada videos/*.json que aún no lleva «archive»: sube el vídeo y la portada de cada idioma,
espera a que Internet Archive los indexe, descarga cada archivo desde archive.org y lo compara con
el local (tamaño y MD5). Solo si todos coinciden escribe "archive": "<elemento>" en el JSON, y desde
entonces generar.py enlaza el vídeo a https://archive.org/download/<elemento>/<archivo> y deja de
copiarlo al sitio. Si algo falla, el JSON no cambia: la web sigue sirviendo la copia local y se
vuelve a probar en la siguiente vuelta. Nunca sale con error por un fallo de archive.org (código 0);
sale con 2 si queda algún vídeo sin subir, para que quien lo llama lo apunte.

    python3 scripts/subir-videos.py                  todo lo pendiente
    python3 scripts/subir-videos.py --minutos 30     sin pasar de media hora (lo normal en el NAS)
    python3 scripts/subir-videos.py --simular        solo dice qué subiría

Credenciales: ~/.config/internetarchive/ia.ini (las del boletín, montadas en el contenedor) o la
ruta de IA_CONFIG_FILE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VIDEOS = RAIZ / "videos"

METADATOS = {
    "mediatype": "movies",
    "collection": "opensource_movies",
    "title": "Diario de IA Educativa · Vídeos {anyo}",
    "creator": "Diario de IA Educativa",
    "description": (
        "Vídeos del Diario de IA Educativa (https://diarioiaeducativa.github.io/), que cuenta cada "
        "mañana lo que se habla en las comunidades docentes ChatGPT-IA-edu, Vibe Coding Educativo y "
        "EduMedia-IAG. Cada domingo, «La semana en vídeo» repasa la semana, en castellano, catalán, "
        "gallego, euskera e inglés. Los hace un programa con los textos y los dibujos del diario, sin "
        "voz y con música compuesta también por programa."),
    "subject": ["IA educativa", "inteligencia artificial", "educación", "Diario de IA Educativa"],
    "language": ["spa", "cat", "glg", "eus", "eng"],
    "licenseurl": "https://creativecommons.org/licenses/by-sa/4.0/",
    "rights": "© {anyo} Juan José de Haro y Raül Torres. CC BY-SA 4.0.",
}

# https://archive.org/developers/bots.html pide un user-agent que identifique al cliente y cómo
# contactar: basta el repositorio, sin datos personales.
AGENTE = "diario-ia-educativa/1.0 (+https://github.com/diarioiaeducativa/periodico)"
CONFIG = {"general": {"user_agent_suffix": AGENTE}}
ITEM_CONTROL = "nasa"   # existe siempre: distingue «archive.org no responde» de «el elemento no existe»


def metadatos_item(ident: str) -> str:
    """ok, ausente o caido."""
    pet = urllib.request.Request(f"https://archive.org/metadata/{ident}", headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(pet, timeout=30) as r:
            datos = json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return "caido"
    return "ok" if datos else "ausente"


def existe_item(ident: str, hasta: float) -> bool | None:
    """True, False o None si archive.org no deja saberlo antes de la hora límite."""
    ausencias = 0
    while time.time() < hasta:
        estado = metadatos_item(ident)
        if estado == "ok":
            return True
        # Durante una caída parcial un elemento que existe puede dar «{}»: tres veces seguidas, con
        # el de control respondiendo, antes de darlo por inexistente.
        if estado == "ausente" and metadatos_item(ITEM_CONTROL) == "ok":
            ausencias += 1
            if ausencias >= 3:
                return False
        else:
            ausencias = 0
        time.sleep(20)
    return None


def md5(ruta: Path) -> str:
    return hashlib.md5(ruta.read_bytes()).hexdigest()


def descarga_igual(ident: str, ruta: Path) -> bool:
    """Descarga el archivo desde archive.org, como lo hará el navegador, y lo compara con el local."""
    url = f"https://archive.org/download/{ident}/{ruta.name}"
    pet = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(pet, timeout=120) as r:
            datos = r.read()
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"  {ruta.name}: no se descarga ({error})", file=sys.stderr)
        return False
    igual = len(datos) == ruta.stat().st_size and hashlib.md5(datos).hexdigest() == md5(ruta)
    if not igual:
        print(f"  {ruta.name}: lo descargado no coincide con el local", file=sys.stderr)
    return igual


def subir_video(v: dict, ruta_json: Path, hasta: float, simular: bool) -> bool:
    from internetarchive import get_item

    anyo = v["publicado"][:4]
    ident = f"diarioiaeducativa_{anyo}"
    archivos = [VIDEOS / f for arch in v["archivos"].values() for f in (arch["video"], arch["poster"])]
    faltan = [a.name for a in archivos if not a.is_file()]
    if faltan:
        print(f"{v['id']}: faltan en local {', '.join(faltan)}; no se sube", file=sys.stderr)
        return False
    print(f"{v['id']}: {len(archivos)} archivos → https://archive.org/details/{ident}")
    if simular:
        return True

    existe = existe_item(ident, hasta)
    if existe is None:
        print(f"{v['id']}: archive.org no responde; se probará en la siguiente vuelta", file=sys.stderr)
        return False
    item = get_item(ident, config=CONFIG)
    ya = {f["name"]: f.get("md5") for f in item.files} if existe else {}
    pendientes = [a for a in archivos if ya.get(a.name) != md5(a)]
    try:
        if pendientes:
            meta = None
            if not existe:
                meta = {k: (x.format(anyo=anyo) if isinstance(x, str) else x) for k, x in METADATOS.items()}
                print(f"  el elemento {ident} no existe: se crea con esta subida")
            # checksum=True no repite lo que ya está igual; verify=True comprueba el MD5 en el servidor
            item.upload({a.name: str(a) for a in pendientes}, metadata=meta, verbose=False,
                        retries=5, retries_sleep=30, checksum=True, verify=True)
    except Exception as error:
        print(f"{v['id']}: la subida falla ({error}); se probará en la siguiente vuelta", file=sys.stderr)
        return False

    # El 200 de la subida solo dice que se ha aceptado: hasta que se indexa, la descarga da 404.
    while True:
        try:
            nombres = {f["name"] for f in get_item(ident, config=CONFIG).files}
        except Exception:
            nombres = set()
        if all(a.name in nombres for a in archivos):
            break
        if time.time() >= hasta:
            print(f"{v['id']}: subido pero aún sin indexar; se comprobará en la siguiente vuelta", file=sys.stderr)
            return False
        time.sleep(30)

    if not all(descarga_igual(ident, a) for a in archivos):
        return False
    v["archive"] = ident
    ruta_json.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
    print(f"  comprobado: se descargan bien; {ruta_json.name} enlaza ya a archive.org")
    return True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--minutos", type=float, default=60, help="tiempo máximo (60 por defecto)")
    p.add_argument("--simular", action="store_true", help="no sube nada")
    a = p.parse_args()
    hasta = time.time() + a.minutos * 60

    pendientes = []
    for f in sorted(VIDEOS.glob("*.json")):
        v = json.loads(f.read_text())
        if not v.get("archive"):
            pendientes.append((f, v))
    if not pendientes:
        print("no hay vídeos por subir")
        return 0
    try:
        import internetarchive  # noqa: F401
    except ImportError:
        print("ERROR: falta la librería internetarchive (nas/Dockerfile)", file=sys.stderr)
        return 2
    sin_subir = [v["id"] for f, v in pendientes if not subir_video(v, f, hasta, a.simular)]
    if sin_subir:
        print(f"AVISO: quedan sin subir: {', '.join(sin_subir)}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
