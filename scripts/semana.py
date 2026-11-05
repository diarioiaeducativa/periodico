#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prepara la entrada del reportaje del domingo: los mensajes de siete días de los tres grupos.

    semana.py <carpeta de datos del bot> <carpeta de salida> <AAAA-MM-DD>

Escribe <salida>/<fecha>.md con los mensajes de los siete días que acaban en <fecha> (el sábado,
cuyo número sale el domingo), día a día y grupo a grupo, sin repetir el contexto de cada día.
Sin IA: solo ordena. Termina con código 3 si la semana no tiene ningún mensaje.
"""
import datetime
import pathlib
import sys

from preparar import NOMBRES, cargar, fmt

DIAS = 7


def main():
    base, out, fin = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), datetime.date.fromisoformat(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    msgs = cargar(base)
    dias = [(fin - datetime.timedelta(days=i)).isoformat() for i in range(DIAS - 1, -1, -1)]
    partes = [f"# Mensajes de los grupos · semana del {dias[0]} al {dias[-1]}\n"]
    total = 0
    for g, (nom, url) in NOMBRES.items():
        partes.append(f"\n## Grupo {nom} ({url}) — clave {g}\n")
        for dia in dias:
            hoy = [m for m in msgs[g] if m["fecha"].startswith(dia)]
            total += len(hoy)
            partes.append(f"\n### {dia}: {len(hoy)} mensajes\n")
            partes += [fmt(m) for m in hoy]
    (out / f"{fin.isoformat()}.md").write_text("\n".join(partes))
    print(f"semana del {dias[0]} al {dias[-1]}: {total} mensajes")
    sys.exit(3 if total == 0 else 0)


if __name__ == "__main__":
    main()
