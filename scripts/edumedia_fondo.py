#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Los candidatos para un artículo de reserva del fondo de EduMedia-IAG (ADR 0077).

    scripts/edumedia_fondo.py DATOS CLAVE        escribe edumedia-fondo-entrada/CLAVE.md

Del historial del grupo (DATOS/edumedia/mensajes.jsonl, del Bot de IA Educativa): los mensajes de hace más de
MINIMO_DIAS días con un enlace a una herramienta, un tutorial o una técnica, que el diario no ha contado ni ha
propuesto ya para la reserva. Los más comentados primero; de ellos, CUANTOS al azar (con la clave como semilla),
para que cada vez salgan otros. Sale con 3 si no queda ninguno.
"""
import datetime
import json
import pathlib
import random
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MINIMO_DIAS = 21     # lo de las últimas semanas aún puede salir como noticia
CUANTOS = 25
# Enlaces que no llevan a una herramienta ni a un tutorial: redes, el propio diario, el boletín del grupo
FUERA = ("x.com", "twitter.com", "t.me", "linkedin.com", "instagram.com", "facebook.com", "tiktok.com",
         "threads.net", "bsky.app", "diarioiaeducativa.github.io", "edumedia-iag.github.io", "share.google",
         "g.co", "chatgpt.com/share", "gemini.google.com/share", "g.page", "wa.me")
URL = re.compile(r"https?://[^\s)\]>»\"']+")


def normal(u):
    u = re.sub(r"^https?://(www\.)?", "", u.strip().rstrip(".,;:")).rstrip("/")
    return u.lower()


def publicadas():
    """Las direcciones que ya salen en algo publicado: no se proponen otra vez."""
    out = set()
    for c in ("ediciones", "biblioteca", "repositorio", "reportajes", "hace-un-ano"):
        for f in (RAIZ / c).glob("20[0-8]*.json"):
            out |= {normal(u) for u in URL.findall(f.read_text(errors="ignore"))}
    return out


def ya_vistos():
    """Los mensajes ya usados o descartados para la reserva, y los de EduMedia que ya salieron en el diario."""
    ids = set()
    for f in list((RAIZ / "reserva").glob("2099-*/ediciones.json")) + \
            list((RAIZ / "reserva" / "retiradas").glob("2099-*/ediciones.json")) + \
            list((RAIZ / "ediciones").glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except ValueError:
            continue
        for p in d.get("piezas", []) + d.get("breves", []):
            m = p.get("mensaje") or {}
            if m.get("grupo") == "edumedia" and m.get("id"):
                ids.add(int(m["id"]))
        for x in d.get("descartado", []) if isinstance(d.get("descartado"), list) else []:
            ids |= {int(n) for n in re.findall(r"mensaje (\d+)", str(x))}
    return ids


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    datos, clave = pathlib.Path(sys.argv[1]), sys.argv[2]
    mensajes = [json.loads(linea) for linea in open(datos / "edumedia" / "mensajes.jsonl", encoding="utf-8")]
    respuestas = {}
    for m in mensajes:
        if m.get("responde_a"):
            respuestas[m["responde_a"]] = respuestas.get(m["responde_a"], 0) + 1
    limite = (datetime.date.today() - datetime.timedelta(days=MINIMO_DIAS)).isoformat()
    vistos, usadas = ya_vistos(), publicadas()
    candidatos = []
    for m in mensajes:
        if str(m.get("fecha", ""))[:10] > limite or m["id"] in vistos:
            continue
        urls = [u for u in URL.findall(m.get("texto") or "")
                if not any(normal(u).startswith(f) for f in FUERA) and normal(u) not in usadas]
        if urls:
            candidatos.append((respuestas.get(m["id"], 0), m, urls))
    if not candidatos:
        print("edumedia-fondo: no queda ningún candidato")
        sys.exit(3)
    candidatos.sort(key=lambda x: -x[0])
    elegidos = random.Random(clave + datetime.date.today().isoformat()).sample(
        candidatos[:CUANTOS * 4], min(CUANTOS, len(candidatos)))
    elegidos.sort(key=lambda x: str(x[1].get("fecha")))
    lineas = [f"# Candidatos del fondo de EduMedia-IAG para la clave {clave}",
              "",
              f"Mensajes de hace más de {MINIMO_DIAS} días con un enlace que el diario no ha contado. Mira la "
              "conversación de cada uno con `mcp__diario__buscar_mensajes --contexto edumedia:ID`. Elige uno "
              "(encargos/edumedia-fondo.md).", ""]
    for n, m, urls in elegidos:
        texto = re.sub(r"\s+", " ", m.get("texto") or "").strip()
        lineas.append(f"## mensaje {m['id']} · {str(m.get('fecha'))[:10]} · {n} respuesta(s)")
        lineas.append(f"Enlace al mensaje: {m.get('enlace') or 'https://t.me/EduMediaIAG/' + str(m['id'])}")
        lineas.append("Enlaces: " + " ".join(urls))
        lineas.append(texto[:700] + ("…" if len(texto) > 700 else ""))
        lineas.append("")
    salida = RAIZ / "edumedia-fondo-entrada" / f"{clave}.md"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text("\n".join(lineas))
    print(f"edumedia-fondo: {len(elegidos)} candidatos de {len(candidatos)}")


if __name__ == "__main__":
    main()
