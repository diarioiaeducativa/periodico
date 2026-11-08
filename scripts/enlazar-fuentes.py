#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Enlaza en el texto, en su primera mención, las fuentes que solo estaban al pie (ADR 0031).

Uso, en el contenedor y desde /proyecto: python3 scripts/enlazar-fuentes.py archivo.json [...]
Sirve para ediciones, Biblioteca, Repositorio y reportajes, en cualquier idioma.
Un agente propone dónde va cada enlace; el programa solo acepta su propuesta si el texto,
quitados los enlaces nuevos, es idéntico carácter a carácter al original y los enlaces nuevos
son de las fuentes de la pieza. Si no, la pieza queda como estaba y se anota.
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

MODELO = "claude-sonnet-5-5"
LINK = re.compile(r"\[([^\[\]]+)\]\((https?://[^)\s]+)\)")

ENCARGO = """Te paso los párrafos de una pieza de un diario y sus fuentes. Enlaza en el texto, con
Markdown [texto](url), cada fuente que el texto nombre y que todavía no esté enlazada: el
documento, artículo, herramienta, web, anuncio u organismo que la fuente es.

- Solo en su primera mención, y el texto del enlace es el nombre tal como aparece (el título,
  el nombre de la herramienta o de quien lo publica), sin comillas angulares si las hay alrededor.
- No cambies ningún otro carácter: ni palabras, ni signos, ni espacios. Solo añades [ ](url).
- Si el texto no nombra una fuente, no la enlaces. No enlaces dentro de un enlace que ya existe.
- Cada fuente, una vez como mucho en toda la pieza.

Responde solo con JSON: {"parrafos": [...]} con el mismo número de párrafos.

"""


def textos(p):
    """Devuelve (lista de párrafos, función para guardarlos) de una pieza."""
    if isinstance(p.get("cuerpo"), list):
        def poner(v): p["cuerpo"] = v
        return list(p["cuerpo"]), poner
    if isinstance(p.get("apartados"), list):
        tam = [len(a.get("parrafos", [])) for a in p["apartados"]]
        planos = [x for a in p["apartados"] for x in a.get("parrafos", [])]
        def poner(v):
            i = 0
            for a, n in zip(p["apartados"], tam):
                a["parrafos"] = v[i:i + n]; i += n
        return planos, poner
    return None, None


def fuentes(p):
    fs = [{"titulo": f.get("titulo", ""), "url": f["url"]} for f in p.get("fuentes", []) if f.get("url")]
    d = p.get("documento") or {}
    if d.get("url"):
        fs.append({"titulo": d.get("titulo", ""), "url": d["url"]})
    return fs


def valida(orig, nuevo, permitidas):
    if not isinstance(nuevo, list) or len(nuevo) != len(orig) or not all(isinstance(x, str) for x in nuevo):
        return "número de párrafos distinto"
    vistas = set()
    for o, n in zip(orig, nuevo):
        enl_o = LINK.findall(o)
        enl_n = LINK.findall(n)
        quita = lambda t, urls: LINK.sub(lambda m: m.group(1) if m.group(2) in urls else m.group(0), t)
        nuevas = [u for _, u in enl_n if u not in [x for _, x in enl_o]]
        if quita(n, set(nuevas)) != o:
            return "el texto cambia"
        for u in nuevas:
            if u not in permitidas:
                return f"enlace ajeno a las fuentes: {u}"
            if u in vistas:
                return f"enlace repetido: {u}"
            vistas.add(u)
    return None


def pide(orig, fs):
    entrada = json.dumps({"parrafos": orig, "fuentes": fs}, ensure_ascii=False, indent=1)
    r = subprocess.run(["claude", "-p", "--model", MODELO, "--tools", "", "--output-format", "text"],
                       input=ENCARGO + entrada, capture_output=True, text=True, timeout=300, cwd="/tmp")
    t = r.stdout.strip()
    t = t[t.find("{"):t.rfind("}") + 1]
    return json.loads(t)["parrafos"]


def trata(tarea):
    archivo, idx, orig, fs = tarea
    juntos = " ".join(orig)
    faltan = [f for f in fs if f["url"] not in juntos]
    if not faltan:
        return archivo, idx, None, "ya enlazadas"
    for intento in range(2):
        try:
            nuevo = pide(orig, faltan)
        except Exception as ex:
            fallo = f"respuesta no válida ({ex})"; continue
        fallo = valida(orig, nuevo, {f["url"] for f in faltan})
        if not fallo:
            n = sum(len(LINK.findall(x)) for x in nuevo) - sum(len(LINK.findall(x)) for x in orig)
            return archivo, idx, nuevo, f"{n} de {len(faltan)} enlazadas"
    return archivo, idx, None, "RECHAZADA: " + fallo


def main(archivos):
    datos, tareas, poner = {}, [], {}
    for a in archivos:
        j = json.load(open(a, encoding="utf-8"))
        datos[a] = j
        piezas = j.get("piezas") if isinstance(j.get("piezas"), list) else [j]
        for i, p in enumerate(piezas):
            orig, pon = textos(p)
            fs = fuentes(p)
            if orig and fs:
                tareas.append((a, i, orig, fs)); poner[(a, i)] = pon
    with ThreadPoolExecutor(6) as ex:
        resultados = list(ex.map(trata, tareas))
    cambiados = set()
    for a, i, nuevo, nota in resultados:
        print(f"{a} #{i}: {nota}", flush=True)
        if nuevo:
            poner[(a, i)](nuevo); cambiados.add(a)
    for a in cambiados:
        with open(a, "w", encoding="utf-8") as f:
            json.dump(datos[a], f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
