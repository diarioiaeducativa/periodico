#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El buscador de lo publicado como herramienta de los agentes (ADR 0061): un servidor MCP mínimo, por la
entrada y la salida estándar, sin dependencias. Los agentes del diario no tienen consola (`Bash` está
prohibido, porque leen mensajes de Telegram que escribe cualquiera); esta herramienta solo busca.

Lo carga cada agente con `--mcp-config scripts/buscar-mcp.json`, y su permiso es `mcp__diario__buscar`.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from buscar import buscar   # noqa: E402

HERRAMIENTA = {
    "name": "buscar",
    "description": (
        "Busca en el texto entero de todo lo que ha publicado el Diario de IA Educativa en castellano: piezas, "
        "breves, Biblioteca, Repositorio, reportajes y «Hace un año». No distingue tildes ni mayúsculas, compara "
        "raíces (encuentra plurales, femeninos y otras formas de la palabra) y, si una palabra no sale, prueba "
        "con las parecidas. Cada resultado trae la clave para enlazarlo (pieza:AAAA-MM-DD/id), la fecha de "
        "publicación y los trozos donde aparece. Úsalo antes de presentar a una persona, herramienta, proyecto "
        "o sitio, y antes de escribir sobre un tema, para no repetir y para enlazar lo ya publicado."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "palabras": {"type": "string", "description": "Lo que se busca: un nombre, una herramienta, unas palabras. Por omisión, piezas que tienen todas."},
            "alguna": {"type": "boolean", "description": "Si es true, basta con una de las palabras; van primero las que tienen más."},
            "parecidas": {"type": "string", "description": "En lugar de palabras, un texto (un titular y su entradilla, un párrafo): devuelve las piezas que tratan de lo mismo, la más parecida primero."},
            "desde": {"type": "string", "description": "Solo lo publicado desde esta fecha de clave (AAAA-MM-DD)."},
            "maximo": {"type": "integer", "description": "Cuántos resultados, 15 por omisión."},
        },
    },
}


def responde(mid, resultado=None, error=None):
    m = {"jsonrpc": "2.0", "id": mid}
    m.update({"error": error} if error else {"result": resultado})
    sys.stdout.write(json.dumps(m, ensure_ascii=False) + "\n")
    sys.stdout.flush()


for linea in sys.stdin:
    try:
        msg = json.loads(linea)
    except ValueError:
        continue
    metodo, mid = msg.get("method"), msg.get("id")
    if mid is None:
        continue   # una notificación (notifications/initialized…): no lleva respuesta
    if metodo == "initialize":
        version = (msg.get("params") or {}).get("protocolVersion", "2025-06-18")
        responde(mid, {"protocolVersion": version, "capabilities": {"tools": {}},
                       "serverInfo": {"name": "diario", "version": "1.0.0"}})
    elif metodo == "tools/list":
        responde(mid, {"tools": [HERRAMIENTA]})
    elif metodo == "tools/call":
        a = (msg.get("params") or {}).get("arguments") or {}
        try:
            if not a.get("palabras") and not a.get("parecidas"):
                raise ValueError("Falta qué buscar: «palabras» o «parecidas».")
            texto = buscar([a.get("palabras") or ""], bool(a.get("alguna")), a.get("parecidas"),
                           a.get("desde"), int(a.get("maximo") or 15))
            responde(mid, {"content": [{"type": "text", "text": texto}], "isError": False})
        except Exception as x:   # el agente ve el error y puede corregir la consulta
            responde(mid, {"content": [{"type": "text", "text": f"Error: {x}"}], "isError": True})
    elif metodo == "ping":
        responde(mid, {})
    else:
        responde(mid, error={"code": -32601, "message": f"Método desconocido: {metodo}"})
