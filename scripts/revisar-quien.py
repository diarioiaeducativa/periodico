#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El relativo «quien» o «quienes» con el sentido de «la persona que», en lo escrito en castellano (ADR 0067). Sin IA.

    scripts/revisar-quien.py --dia AAAA-MM-DD   lo escrito esa noche en castellano, y sus avisos
    scripts/revisar-quien.py --todo             todo lo publicado en castellano (para medir)

Juanjo no lo usa (15-11-2026: «no quiero que se use quien o quienes en este sentido»). En castellano el relativo
no lleva tilde y el interrogativo sí («¿quién?», «no se sabe quién»), así que basta con buscar la palabra sin
tilde. Las citas literales («…» o “…”) no se tocan. Escribe una línea por frase y sale con 4; sin nada, con 0.
"""
import datetime
import importlib.util
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("autoria", RAIZ / "scripts" / "revisar-autoria.py")
autoria = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(autoria)

SECCIONES = ("ediciones", "reportajes", "biblioteca", "hace-un-ano", "repositorio")
QUIEN = re.compile(r"\b[Qq]uien(es)?\b")
CITA = re.compile(r"«[^»]*»|“[^”]*”")


def revisar(f):
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError):
        return []
    out = []
    for ruta, t in autoria.textos(d):
        for fr in autoria.frases(t):
            if QUIEN.search(CITA.sub("", fr)):
                out.append(f"{f.relative_to(RAIZ)} · {ruta} · «{fr.strip()[:300]}»")
    return out


def main():
    if "--todo" in sys.argv:
        fs = sorted(f for s in SECCIONES for f in (RAIZ / s).glob("20*.json")) + sorted((RAIZ / "avisos").glob("20*.json"))
    else:
        fecha = sys.argv[sys.argv.index("--dia") + 1]
        sig = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
        fs = [f for f in [RAIZ / s / f"{fecha}.json" for s in SECCIONES] + [RAIZ / "avisos" / f"{sig}.json"] if f.exists()]
    hallado = [h for f in fs for h in revisar(f)]
    print("\n".join(hallado) if hallado else f"revisar-quien: ningún «quien» relativo ({len(fs)} archivos)")
    return 4 if hallado else 0


if __name__ == "__main__":
    sys.exit(main())
