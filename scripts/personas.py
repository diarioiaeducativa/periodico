#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Quién escribe cada mensaje, en el material que leen los agentes (ADR 0066).

En los grupos, el nombre visible no distingue a las personas: el 11-11-2026 un miembro que firma «Juanjo»
compartió Eduvers y el diario lo atribuyó dos veces a Juan José de Haro, que en los grupos firma «Juanjo de
Haro». Cada mensaje del bot trae `autor_id`, el número fijo de la cuenta de Telegram, y con él se marca:
- a los autores del diario: «Juanjo de Haro [autor del diario: Juan José de Haro]»;
- a quien comparte nombre visible con otra cuenta: «Juanjo [cuenta 2 de «Juanjo»]», o con su @usuario si
  lo tiene. El número de cuenta de Telegram no aparece: el orden es el de su primer mensaje en los grupos.

Los números de cuenta de los autores del diario no van en este repositorio, que es público: están en
~/.config/diario-autores.json del contenedor (DIARIO_AUTORES), con la forma
{"<autor_id>": {"nombre": "Nombre en el diario", "en_grupos": ["Nombre visible", ...]}}.
Sin ese archivo, solo se distinguen los nombres repetidos, y `autores()` devuelve {}.
"""
import json
import os
import pathlib
from collections import defaultdict

CONFIG = pathlib.Path(os.environ.get("DIARIO_AUTORES", pathlib.Path.home() / ".config" / "diario-autores.json"))


def autores():
    """{autor_id: {"nombre": ..., "en_grupos": [...]}} de los autores del diario; {} si no está el archivo."""
    try:
        return {int(k): v for k, v in json.loads(CONFIG.read_text()).items()}
    except (OSError, ValueError):
        return {}


def _id(m):
    try:
        return int(m.get("autor_id"))
    except (TypeError, ValueError):
        return None


class Etiquetas:
    """Se construye con todos los mensajes (de todos los grupos) y da la etiqueta de cada uno."""

    def __init__(self, mensajes):
        self.autores = autores()
        cuentas = defaultdict(list)   # nombre visible -> cuentas, por orden de su primer mensaje
        self.usuario = {}
        for m in sorted(mensajes, key=lambda m: m.get("fecha") or ""):
            i = _id(m)
            if i is None:
                continue
            nombre = (m.get("autor") or "").strip()
            if i not in cuentas[nombre]:
                cuentas[nombre].append(i)
            u = str(m.get("usuario") or "")
            if u and u != "None":
                self.usuario[i] = u
        self.cuentas = cuentas

    def __call__(self, m):
        nombre = (m.get("autor") or "").strip()
        i = _id(m)
        if i is None:
            return nombre
        if i in self.autores:
            return f"{nombre} [autor del diario: {self.autores[i]['nombre']}]"
        if len(self.cuentas.get(nombre, ())) > 1:
            if i in self.usuario:
                return f"{nombre} [@{self.usuario[i]}]"
            n = self.cuentas[nombre].index(i) + 1
            if not nombre:
                return f"[sin nombre visible, cuenta {n}]"
            return f"{nombre} [cuenta {n} de «{nombre}»]"
        return nombre


def de_carpeta(base, grupos=("chatgpt", "vce", "edumedia")):
    """Las etiquetas, a partir de los mensajes.jsonl de los grupos de la carpeta de datos del bot."""
    todos = []
    for g in grupos:
        f = pathlib.Path(base) / g / "mensajes.jsonl"
        if not f.exists():
            continue
        for linea in f.open():
            try:
                todos.append(json.loads(linea))
            except ValueError:
                continue
    return Etiquetas(todos)
