#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Escribe publicado.txt: lo ya publicado, para que la redacción no repita temas y enlace lo
relacionado. Cada pieza va con su clave de enlace (`pieza:AAAA-MM-DD/id`), que generar.py
convierte en el enlace a su página (encargos/enlaces.md). Incluye las piezas de la redacción,
de la Biblioteca, del Repositorio de VCE (con sus recursos, ADR 0008) y los reportajes."""
import datetime
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
dias = {}


def apunta(fecha, linea):
    dias.setdefault(fecha, []).append(linea)


for f in sorted((RAIZ / "ediciones").glob("*.json")):
    d = json.loads(f.read_text())
    if not d.get("hay_edicion"):
        continue
    for p in d.get("piezas", []):
        apunta(d["fecha"], f'pieza:{d["fecha"]}/{p["id"]} ({p.get("seccion")}) {p["titular"]}')
    for b in d.get("breves", []):
        apunta(d["fecha"], f'breve: {b["texto"][:90]}')
for carpeta in ("biblioteca", "repositorio"):
    for f in sorted((RAIZ / carpeta).glob("*.json")):
        d = json.loads(f.read_text())
        fecha = d.get("fecha") or f.stem
        for p in d.get("piezas", []):
            recursos = "; ".join(f'{r.get("titulo")} ({r.get("url")})' for r in p.get("recursos", []))
            apunta(fecha, f'pieza:{fecha}/{p["id"]} ({carpeta}) {p["titular"]}'
                   + (f' — recursos con artículo: {recursos}' if recursos else ""))
for f in sorted((RAIZ / "reportajes").glob("*.json")):
    d = json.loads(f.read_text())
    if d.get("hay_reportaje") and d.get("id"):
        apunta(f.stem, f'pieza:{f.stem}/{d["id"]} (reportaje) {d.get("titular", "")}')
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre")
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


def publicada(fecha):
    """La clave lleva la fecha de las conversaciones; el número sale al día siguiente, y esa es la
    fecha que ve el lector (la de cada pieza, la del archivo y la de la hemeroteca)."""
    d = datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]} de {d.year}"


lineas = ["# Lo ya publicado. Para enlazar una pieza en un texto: [texto que dice de qué trata](pieza:AAAA-MM-DD/id)",
          "# La fecha de la clave es la de las conversaciones: si dices cuándo lo contó el diario,",
          "# usa la de publicación que va en el encabezado de cada día («publicado el …»)."]
for fecha in sorted(dias):
    lineas.append(f"\n## {fecha} (publicado el {publicada(fecha)})")
    lineas += [f"- {x}" for x in dias[fecha]]
(RAIZ / "publicado.txt").write_text("\n".join(lineas) + "\n")
print(f"publicado.txt: {len(dias)} días")
