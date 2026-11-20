#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Los buscadores del diario como herramientas de los agentes (ADR 0061): lo publicado y los mensajes de los grupos, un servidor MCP mínimo, por la
entrada y la salida estándar, sin dependencias. Los agentes del diario no tienen consola (`Bash` está
prohibido, porque leen mensajes de Telegram que escribe cualquiera); esta herramienta solo busca.

Lo carga cada agente con `--mcp-config scripts/buscar-mcp.json`, y su permiso es `mcp__diario` (todas las herramientas).
«buscar_termcat» busca en los diccionarios abiertos del TERMCAT (ADR 0094, scripts/termcat.py).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from buscar import buscar   # noqa: E402
from buscar_mensajes import buscar_mensajes, contexto   # noqa: E402
from termcat import buscar as buscar_termcat   # noqa: E402

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


MENSAJES = {
    "name": "buscar_mensajes",
    "description": (
        "Busca en todo el historial de los tres grupos de Telegram del diario (ChatGPT-IA-edu, Vibe Coding Educativo y "
        "EduMedia-IAG), no solo en los mensajes del día: el texto, lo que se ve en cada imagen y la vista previa de cada "
        "enlace. Mismo motor que «buscar» (sin tildes ni mayúsculas, variantes de cada palabra, nombres parecidos). "
        "Cada resultado trae el enlace directo al mensaje, la fecha, el grupo y el tema. Úsalo para saber si un tema "
        "ya se habló antes y cuándo, para encontrar el mensaje original exacto que se cita y, en un reportaje, para "
        "reunir lo que se ha dicho de un tema a lo largo de los meses. Para leer la conversación alrededor de un "
        "mensaje, «contexto_mensaje»."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "palabras": {"type": "string", "description": "Lo que se busca. Por omisión, mensajes que tienen todas las palabras."},
            "alguna": {"type": "boolean", "description": "Si es true, basta con una de las palabras."},
            "parecidas": {"type": "string", "description": "En lugar de palabras, un texto: devuelve los mensajes que tratan de lo mismo."},
            "grupo": {"type": "string", "enum": ["chatgpt", "vce", "edumedia"], "description": "Solo un grupo."},
            "desde": {"type": "string", "description": "Desde esta fecha (AAAA-MM-DD)."},
            "hasta": {"type": "string", "description": "Hasta esta fecha, incluida (AAAA-MM-DD)."},
            "orden": {"type": "string", "enum": ["pertinencia", "fecha"], "description": "«fecha»: los más recientes primero."},
            "maximo": {"type": "integer", "description": "Cuántos resultados, 15 por omisión."},
        },
    },
}
CONTEXTO = {
    "name": "contexto_mensaje",
    "description": ("Un mensaje de los grupos con la conversación que lo rodea en su tema (los anteriores y los "
                    "siguientes), el mensaje al que responde y todas sus respuestas, cada uno con su enlace."),
    "inputSchema": {
        "type": "object",
        "properties": {"mensaje": {"type": "string", "description": "grupo:id, por ejemplo vce:14875 (grupos: chatgpt, vce, edumedia)."}},
        "required": ["mensaje"],
    },
}


TERMCAT = {
    "name": "buscar_termcat",
    "description": (
        "Busca un término en la terminología del TERMCAT, el centro de terminología de la lengua catalana: la Neoloteca "
        "(los términos que ha normalizado su Consell Supervisor) y sus diccionarios de inteligencia artificial, de "
        "educación y de productos informáticos, descargados de su web en abierto. Se le da la palabra en inglés, en "
        "castellano o en catalán («prompt», «chatbot», «alucinación») y devuelve el término catalán, si está "
        "normalizado, sus sinónimos, los equivalentes en otras lenguas y la definición. Úsalo al traducir o escribir en "
        "catalán un término técnico: un término normalizado manda sobre cualquier otra forma. Si no sale, el Optimot."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "palabras": {"type": "string", "description": "El término que se busca, en inglés, castellano o catalán."},
            "maximo": {"type": "integer", "description": "Cuántas fichas, 8 por omisión."},
        },
        "required": ["palabras"],
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
        responde(mid, {"tools": [HERRAMIENTA, MENSAJES, CONTEXTO, TERMCAT]})
    elif metodo == "tools/call":
        par = msg.get("params") or {}
        a, nombre = par.get("arguments") or {}, par.get("name")
        try:
            if nombre == "contexto_mensaje":
                texto = contexto(a.get("mensaje") or "")
            elif nombre == "buscar_termcat":
                texto = buscar_termcat(a.get("palabras") or "", int(a.get("maximo") or 8))
            elif not a.get("palabras") and not a.get("parecidas"):
                raise ValueError("Falta qué buscar: «palabras» o «parecidas».")
            elif nombre == "buscar_mensajes":
                texto = buscar_mensajes([a.get("palabras") or ""], bool(a.get("alguna")), a.get("parecidas"),
                                        a.get("grupo"), a.get("desde"), a.get("hasta"), a.get("orden") or "pertinencia",
                                        int(a.get("maximo") or 15))
            else:
                texto = buscar([a.get("palabras") or ""], bool(a.get("alguna")), a.get("parecidas"),
                               a.get("desde"), int(a.get("maximo") or 15))
            responde(mid, {"content": [{"type": "text", "text": texto}], "isError": False})
        except Exception as x:   # el agente ve el error y puede corregir la consulta
            responde(mid, {"content": [{"type": "text", "text": f"Error: {x}"}], "isError": True})
    elif metodo == "ping":
        responde(mid, {})
    else:
        responde(mid, error={"code": -32601, "message": f"Método desconocido: {metodo}"})
