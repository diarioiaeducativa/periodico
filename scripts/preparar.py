#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prepara la entrada de la redacción: los mensajes de un día de los tres grupos, en Markdown.

    preparar.py <carpeta de datos del bot> <carpeta de salida> <AAAA-MM-DD> [...]

Lee <datos>/<grupo>/mensajes.jsonl y temas.json (los que guarda el Bot de IA Educativa) y
escribe <salida>/<fecha>.md con los mensajes de ese día y, como contexto, los del anterior.
Con RECUPERA=1 (el número del día anterior salió con la reserva, ADR 0021), los del anterior no
son contexto sino noticia, como los del día: así no se pierde ninguno.
Sin IA: solo ordena. Termina con código 3 si el día no tiene ningún mensaje en ningún grupo.
"""
import datetime
import os
import json
import pathlib
import sys

NOMBRES = {"chatgpt": ("ChatGPT-IA-edu", "https://t.me/ChatGPTedu"),
           "vce": ("Vibe Coding Educativo", "https://t.me/vceduca"),
           "edumedia": ("EduMedia-IAG", "https://t.me/EduMediaIAG")}


def cargar(base):
    msgs = {}
    for g in NOMBRES:
        temas = json.loads((base / g / "temas.json").read_text())
        imagenes = base / g / "imagenes"   # lo que se ve en cada imagen, lo describe el bot (su ADR 0028)
        msgs[g] = []
        for linea in (base / g / "mensajes.jsonl").open():
            m = json.loads(linea)
            m["tema_nombre"] = temas.get(str(m.get("tema")), "General")
            d = imagenes / f"{m['id']}.txt"
            if d.exists():
                m["imagen"] = d.read_text().strip()
            msgs[g].append(m)
    return msgs


def fmt(m):
    r = f" (responde a #{m['responde_a']})" if m.get("responde_a") else ""
    imagen = f"\n[imagen: {m['imagen']}]" if m.get("imagen") else ""
    # La vista previa del enlace: muchas veces es el único sitio del mensaje donde está la dirección
    w = m.get("web") or {}
    web = (f"\n[enlace: {w['url']}" + (f" · «{w['titulo']}»" if w.get("titulo") else "") +
           (f" · {' '.join(w['descripcion'].split())}" if w.get("descripcion") else "") + "]") if w.get("url") else ""
    return f"#{m['id']} · {m['fecha'][11:16]} · tema «{m['tema_nombre']}» · {m['autor']}{r}\n{(m.get('texto') or '').strip()}{web}{imagen}\n"


def main():
    base, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    msgs = cargar(base)
    vacio = False
    for dia in sys.argv[3:]:
        ant = (datetime.date.fromisoformat(dia) - datetime.timedelta(days=1)).isoformat()
        partes = [f"# Mensajes de los grupos · día {dia}\n"]
        total = 0
        for g, (nom, url) in NOMBRES.items():
            hoy = [m for m in msgs[g] if m["fecha"].startswith(dia)]
            prev = [m for m in msgs[g] if m["fecha"].startswith(ant)]
            total += len(hoy)
            if os.environ.get("RECUPERA") == "1":
                total += len(prev)
                partes.append(f"\n## Grupo {nom} ({url}) — clave {g}\n\n### RECUPERADO: día anterior ({ant}), "
                              f"{len(prev)} mensajes (su número salió con la reserva: es noticia como los de hoy)\n")
            else:
                partes.append(f"\n## Grupo {nom} ({url}) — clave {g}\n\n### Contexto: día anterior ({ant}), "
                              f"{len(prev)} mensajes (solo para entender hilos; no es noticia de hoy)\n")
            partes += [fmt(m) for m in prev]
            partes.append(f"\n### DÍA {dia}: {len(hoy)} mensajes\n")
            partes += [fmt(m) for m in hoy]
        (out / f"{dia}.md").write_text("\n".join(partes))
        print(f"{dia}: {total} mensajes del día")
        vacio = vacio or total == 0
    sys.exit(3 if vacio else 0)


if __name__ == "__main__":
    main()
