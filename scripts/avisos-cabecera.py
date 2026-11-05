#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Añade a los avisos de la mañana la cabecera del número (ADR 0010): el título con el número,
la fecha en letra y el enlace a la portada con una marca del número, para que Telegram no
reutilice la vista previa del día anterior. El bot monta con eso el mensaje (su ADR 0029).

    scripts/avisos-cabecera.py AAAA-MM-DD   (la fecha de las conversaciones; los avisos son del día siguiente)

Sin IA. Si no encuentra el número, deja los avisos como están."""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402


def main():
    fecha = sys.argv[1]
    publica = generar.publicacion(fecha)
    f = RAIZ / "avisos" / f"{publica}.json"
    if not f.exists():
        return
    generar.L = generar.IDIOMAS["es"]   # los avisos van en castellano en los tres grupos
    d = next((x for x in generar.cargar() if x["fecha"] == fecha and x.get("numero")), None)
    if not d:
        print(f"avisos-cabecera: el {fecha} no es un número; los avisos quedan como están")
        return
    avisos = json.loads(f.read_text())
    avisos.update(titulo=f'{generar.L["titulo"]} · {generar.L["num"]} {d["numero"]}',
                  fecha_texto=generar.fecha_larga(publica).capitalize(),
                  url=f'{generar.BASE}?n={d["numero"]}')
    f.write_text(json.dumps(avisos, ensure_ascii=False, indent=2) + "\n")
    print(f"avisos-cabecera: número {d['numero']}")


if __name__ == "__main__":
    main()
