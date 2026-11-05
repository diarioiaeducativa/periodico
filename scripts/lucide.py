#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prepara el repertorio de iconos de Lucide para el ilustrador (ADR 0014).

    scripts/lucide.py VERSIÓN      (por ejemplo, 1.60.0)

Baja el paquete lucide-static de npm y escribe lucide/iconos.txt, una línea por icono:
nombre, etiquetas (en inglés) y sus formas, listas para copiar dentro de un <g>. Los agentes
no tienen terminal: lo buscan con Grep. Las formas que Lucide rellena (fill="currentColor")
llevan la clase ft de la hoja de estilo, para que no haya colores escritos a mano.
"""
import io
import json
import pathlib
import sys
import tarfile
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
version = sys.argv[1]
url = f"https://registry.npmjs.org/lucide-static/-/lucide-static-{version}.tgz"
with urllib.request.urlopen(url, timeout=60) as r:
    tar = tarfile.open(fileobj=io.BytesIO(r.read()), mode="r:gz")
leer = lambda n: tar.extractfile(f"package/{n}").read().decode()
nodos = json.loads(leer("icon-nodes.json"))
etiquetas = json.loads(leer("tags.json"))
lineas = []
for nombre in sorted(nodos):
    formas = []
    for etiqueta, attrs in nodos[nombre]:
        a = {k: v for k, v in attrs.items() if k != "key"}
        clase = ' class="ft"' if a.pop("fill", None) == "currentColor" else ""
        formas.append(f"<{etiqueta}{clase} " + " ".join(f'{k}="{v}"' for k, v in a.items()) + "/>")
    lineas.append(f'{nombre} | {", ".join(etiquetas.get(nombre, []))} | {"".join(formas)}')
destino = RAIZ / "lucide"
destino.mkdir(exist_ok=True)
(destino / "iconos.txt").write_text(
    f"# Lucide {version} (https://lucide.dev), licencia ISC: véase LICENSE. Una línea por icono:\n"
    "# nombre | etiquetas | formas (en una cuadrícula de 24 × 24)\n" + "\n".join(lineas) + "\n")
(destino / "LICENSE").write_text(leer("LICENSE"))
print(f"lucide/iconos.txt: {len(lineas)} iconos de Lucide {version}")
