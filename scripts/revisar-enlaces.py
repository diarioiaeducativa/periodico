#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Busca enlaces caídos en lo ya publicado (ADR 0056). Sin IA.

Un diario enlaza cada dato a su fuente, y las fuentes desaparecen: un repositorio que se borra, una web que
cierra. Este programa abre, una vez por semana, los enlaces externos de todas las piezas (las fuentes y los
del texto, en la edición en castellano, que son los mismos en las demás) y apunta los que ya no existen.

    scripts/revisar-enlaces.py              comprueba y escribe el resultado
    scripts/revisar-enlaces.py --avisar     además, avisa de los que llevan dos pasadas seguidas caídos
    scripts/revisar-enlaces.py --max 30     solo los primeros 30 (para probar)

Qué cuenta como caído: la página responde 404 o 410, o el dominio ya no existe. Un 403, un 429, un error
del servidor o una espera agotada no cuentan: muchas webs oficiales rechazan la lectura automática, y eso
no se salta ni se da por caída. Para avisar hacen falta dos pasadas seguidas, por si era un fallo de un día.
De cada enlace caído se mira si hay copia en la Wayback Machine, para ponerla en la nota de la pieza.

No toca las piezas: la nota («Actualización del…», ADR 0055) va en los cinco idiomas y la escribe quien
corrige. Va despacio a propósito (una petición cada 3 segundos al mismo servidor) para no molestar a nadie.
"""
import argparse
import datetime
import json
import pathlib
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESTADO = RAIZ / "estado" / "enlaces.json"
CARPETAS = ("ediciones", "biblioteca", "hace-un-ano", "reportajes")
ENLACE_MD = re.compile(r"\]\((https?://[^)\s]+)\)")
# No se comprueban: los mensajes de los grupos (son la propia fuente y Telegram limita las lecturas), el
# propio diario y las copias archivadas
FUERA = ("t.me", "telegram.me", "diarioiaeducativa.github.io", "web.archive.org", "archive.org")
AGENTE = "Mozilla/5.0 (compatible; revisor-de-enlaces; +https://diarioiaeducativa.github.io/redaccion.html)"
PAUSA = 3.0   # segundos entre dos peticiones al mismo servidor


def textos(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from textos(y)
    elif isinstance(x, dict):
        for k, y in x.items():
            if k not in ("comprobado", "repaso", "motivo", "descartado"):
                yield from textos(y)


ANOTADAS = set()   # las piezas que ya llevan una nota con la copia archivada: de esas no se vuelve a avisar


def enlaces():
    """{url: [pieza, …]} de todo lo publicado en castellano."""
    out = {}
    for carpeta in CARPETAS:
        for f in sorted((RAIZ / carpeta).glob("20??-??-??.json")):
            try:
                d = json.loads(f.read_text())
            except ValueError:
                continue
            piezas = [d] if carpeta == "reportajes" else d.get("piezas", [])
            for n, b in enumerate(d.get("breves", []) if carpeta == "ediciones" else [], 1):
                piezas = piezas + [dict(b, id=f"breve-{n}")]
            for p in piezas:
                if not p.get("id"):
                    continue
                clave = f"{f.stem}/{p['id']}"
                if "web.archive.org" in (p.get("correccion") or ""):
                    ANOTADAS.add(clave)
                urls = {x.get("url") for x in p.get("fuentes", []) if isinstance(x, dict)} | {p.get("url")}
                urls |= {u for t in textos(p) for u in ENLACE_MD.findall(t)}
                urls.add((p.get("documento") or {}).get("url"))
                for u in urls:
                    if u and u.startswith("http") and urllib.parse.urlsplit(u).hostname not in FUERA:
                        out.setdefault(u.rstrip(".,;"), []).append(clave)
    return out


def abrir(url):
    """'ok', 'caido' o 'dudoso' (no se puede saber), y el detalle."""
    pet = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": "*/*", "Range": "bytes=0-2047"})
    try:
        with urllib.request.urlopen(pet, timeout=25) as r:
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        return ("caido" if e.code in (404, 410) else "dudoso"), str(e.code)
    except urllib.error.URLError as e:
        r = e.reason
        if isinstance(r, socket.gaierror):
            return "caido", "el dominio no existe"
        return "dudoso", str(r)[:80]
    except Exception as e:   # noqa: BLE001  (una web rara no puede parar la pasada)
        return "dudoso", type(e).__name__


def copia_archivada(url):
    try:
        pet = urllib.request.Request("https://archive.org/wayback/available?url=" + urllib.parse.quote(url.split("://", 1)[-1], safe="/"),
                                     headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(pet, timeout=25) as r:
            c = (json.load(r).get("archived_snapshots") or {}).get("closest") or {}
        return c.get("url", "").replace("http://", "https://", 1) if c.get("available") else ""
    except Exception:   # noqa: BLE001
        return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--avisar", action="store_true", help="avisa de los que llevan dos pasadas caídos")
    ap.add_argument("--max", type=int, help="solo los primeros N enlaces (para probar)")
    a = ap.parse_args()
    todos = enlaces()
    urls = sorted(todos)[: a.max] if a.max else sorted(todos)
    try:
        antes = json.loads(ESTADO.read_text())
    except (OSError, ValueError):
        antes = {}
    caidos_antes = antes.get("caidos", {})
    ultima, caidos, dudosos = {}, {}, 0
    for u in urls:
        host = urllib.parse.urlsplit(u).hostname or ""
        espera = PAUSA - (time.time() - ultima.get(host, 0))
        if espera > 0:
            time.sleep(espera)
        estado, detalle = abrir(u)
        ultima[host] = time.time()
        if estado == "dudoso":
            dudosos += 1
        elif estado == "caido":
            previo = caidos_antes.get(u, {})
            caidos[u] = {"detalle": detalle, "piezas": sorted(set(todos[u])), "veces": previo.get("veces", 0) + 1,
                         "avisado": previo.get("avisado", False) or set(todos[u]) <= ANOTADAS, "copia": previo.get("copia") or copia_archivada(u)}
    hoy = datetime.date.today().isoformat()
    print(f"{hoy}: {len(urls)} enlaces; {len(caidos)} caídos; {dudosos} que no dejan comprobarse")
    nuevos = [u for u, c in caidos.items() if c["veces"] >= 2 and not c["avisado"]]
    for u, c in sorted(caidos.items()):
        print(f"  caído ({c['detalle']}, {c['veces']} pasadas{', ya anotado o avisado' if c['avisado'] else ''}): {u}  en {', '.join(c['piezas'])}"
              + (f"  copia: {c['copia']}" if c["copia"] else "  sin copia archivada"))
    if a.avisar and nuevos:
        lineas = [f"{', '.join(caidos[u]['piezas'])}: {u}" + (f" (copia: {caidos[u]['copia']})" if caidos[u]["copia"] else " (sin copia archivada)")
                  for u in nuevos[:6]]
        texto = (f"Enlaces caídos en piezas ya publicadas del diario ({len(nuevos)}): " + " · ".join(lineas)
                 + (" · y más, en el registro" if len(nuevos) > 6 else "")
                 + ". A cada pieza le falta una nota de actualización en los cinco idiomas. Registro: registro/enlaces.log")
        try:
            subprocess.run(["avisar-juanjo", "--de", "Diario de IA Educativa", texto], check=True, timeout=60,
                           stdout=subprocess.DEVNULL)
            for u in nuevos:
                caidos[u]["avisado"] = True
        except Exception as e:   # noqa: BLE001
            print(f"  no se pudo avisar: {e}")
    if not a.max:
        ESTADO.parent.mkdir(exist_ok=True)
        ESTADO.write_text(json.dumps({"fecha": hoy, "caidos": caidos}, ensure_ascii=False, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
