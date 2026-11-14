#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Añade a los avisos de la mañana la cabecera del número (ADR 0010): el título con el número,
la fecha en letra, el enlace a la portada con una marca del número, para que Telegram no
reutilice la vista previa del día anterior, y la captura de la portada como imagen. El bot monta
con eso el mensaje (sus ADR 0029 y 0037).

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
                  url=f'{generar.BASE}?n={d["numero"]}',
                  # La portada del número como imagen del aviso, la misma en los tres grupos (ADR 0053; ADR 0037
                  # del bot). La hace portadas.py justo después; el bot comprueba que ya está en la web.
                  imagen=f'{generar.BASE}portadas/{fecha}-es.jpg')
    # Cada grupo, su página de entrada con su imagen (n/<número>-<grupo>.html), si ese día la tiene;
    # si no, el aviso lleva el enlace general de arriba (ADR 0010).
    for g, aviso in (avisos.get("avisos") or {}).items():
        if isinstance(aviso, dict) and (RAIZ / "og" / "numeros" / f"{fecha}-es-{g}.png").exists() \
                and generar.pieza_de_grupo(d, g):
            aviso["url"] = f'{generar.BASE}n/{d["numero"]}-{g}.html'
    f.write_text(json.dumps(avisos, ensure_ascii=False, indent=2) + "\n")
    print(f"avisos-cabecera: número {d['numero']}")


if __name__ == "__main__":
    main()
