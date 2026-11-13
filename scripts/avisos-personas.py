#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Añade a los avisos de la mañana a quién avisa el bot por privado (ADR 0052): cada persona que ha
aportado algo que sale en el número, con las piezas que lo cuentan, en los cinco idiomas.

    scripts/avisos-personas.py AAAA-MM-DD   (la fecha de las conversaciones; los avisos son del día siguiente)

Quién ha aportado cada pieza, sin IA y con los datos del bot (DATOS_BOT, /bot-datos):
- Biblioteca: quien la subió, el «Aportado por Nombre (@usuario)» del mensaje que publicó el bot,
  o quien escribió el mensaje si lo publicó una persona.
- Recursos del repositorio de VCE: quien dio de alta cada recurso con el bot (catalogo.json).
- Piezas del redactor: quien escribió el mensaje de la pieza, solo si la pieza lo nombra (es el
  autor del recurso que se cuenta; a quien opina o pregunta no se le nombra, encargos/redaccion.md).
El bot decide si puede escribirle (solo a quien ha hablado alguna vez con él) y respeta a quien ha
pedido no recibirlos. Si algo falla, los avisos quedan como estaban."""
import json
import pathlib
import re
import sys
import urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
import generar  # noqa: E402

DATOS = pathlib.Path(__import__("os").environ.get("DATOS_BOT", "/bot-datos"))
GRUPOS = ("chatgpt", "vce", "edumedia")
IDIOMAS = ("es", "ca", "gl", "eu", "en")
FUERA = {"hace-un-ano"}   # mensajes de hace un año: no se avisa por lo que ya pasó
# En el diario se firma con el nombre completo aunque en los grupos se use otro (encargos/redaccion.md)
OTROS_NOMBRES = {"Juanjo de Haro": ["Juan José de Haro"]}


def mensajes():
    """{grupo: {id: mensaje}} y {usuario en minúsculas: id de Telegram} de los tres grupos."""
    por_grupo, por_usuario, por_nombre = {}, {}, {}
    for g in GRUPOS:
        por_grupo[g] = {}
        try:
            lineas = (DATOS / g / "mensajes.jsonl").open()
        except OSError:
            continue
        for linea in lineas:
            try:
                m = json.loads(linea)
            except ValueError:
                continue
            por_grupo[g][str(m.get("id"))] = m
            if es_persona(m):
                if m.get("usuario") and m["usuario"] != "None":
                    por_usuario[m["usuario"].lower()] = int(m["autor_id"])
                por_nombre.setdefault(m.get("autor", "").strip(), set()).add(int(m["autor_id"]))
    return por_grupo, por_usuario, por_nombre


def es_persona(m):
    usuario = str(m.get("usuario") or "")
    return bool(m.get("autor_id")) and str(m.get("autor_id")).lstrip("-").isdigit() \
        and not usuario.lower().endswith("bot") and int(m["autor_id"]) > 0


def nombra(p, nombre):
    # Solo lo que lee el público: «comprobado» es una nota interna y puede nombrar a quien no sale
    texto = " ".join(str(p.get(k) or "") for k in ("antetitulo", "titular", "entradilla", "cuerpo"))
    return any(n and n in texto for n in [nombre] + OTROS_NOMBRES.get(nombre, []))


def de_la_biblioteca(m, por_usuario, por_nombre):
    if not m:
        return None
    if es_persona(m):
        return int(m["autor_id"])
    a = re.search(r"Aportado por (.+?)(?:\s*\(@(\w+)\))?\s*$", m.get("texto", ""), re.M)
    if not a:
        return None
    if a.group(2) and a.group(2).lower() in por_usuario:
        return por_usuario[a.group(2).lower()]
    ids = por_nombre.get(a.group(1).strip(), set())
    return next(iter(ids)) if len(ids) == 1 else None   # un nombre repetido no basta para saber quién es


def dueno_recurso(r, recursos):
    """Quien dio de alta el recurso con el bot: el catálogo guarda la dirección tal como está en la hoja,
    que es la de la ficha (?ids=…); si no, la del recurso."""
    candidatos = []
    ids = urllib.parse.parse_qs(urllib.parse.urlparse(r.get("ficha", "")).query).get("ids", [])
    candidatos += ids
    candidatos.append(r.get("url", ""))
    for c in candidatos:
        uid = recursos.get(c.strip().lower().rstrip("/"))
        if uid:
            return int(uid)
    return None


def titulares(fecha, pid):
    """El titular de la pieza en cada idioma (si una traducción falta, el castellano)."""
    salida = {}
    for c in IDIOMAS:
        suf = "" if c == "es" else f"-{c}"
        for carpeta in ("ediciones", "biblioteca", "repositorio"):
            f = RAIZ / f"{carpeta}{suf}" / f"{fecha}.json"
            try:
                p = next((x for x in json.loads(f.read_text()).get("piezas", []) if x.get("id") == pid), None)
            except (OSError, ValueError):
                p = None
            if p and p.get("titular"):
                salida[c] = p["titular"]
                break
    return salida


def main():
    fecha = sys.argv[1]
    publica = generar.publicacion(fecha)
    f = RAIZ / "avisos" / f"{publica}.json"
    if not f.exists():
        return
    generar.L = generar.IDIOMAS["es"]
    d = next((x for x in generar.cargar() if x["fecha"] == fecha and x.get("numero")), None)
    if not d:
        return
    por_grupo, por_usuario, por_nombre = mensajes()
    try:
        recursos = json.loads((DATOS / "catalogo.json").read_text()).get("recursos", {})
    except (OSError, ValueError):
        recursos = {}
    personas = {}   # id de Telegram -> ids de pieza, en el orden del número
    for p in d["piezas"]:
        if p.get("seccion") in FUERA:
            continue
        quienes = set()
        msg = p.get("mensaje") or {}
        m = por_grupo.get(msg.get("grupo"), {}).get(str(msg.get("id")))
        if p.get("seccion") == "biblioteca":
            quienes.add(de_la_biblioteca(m, por_usuario, por_nombre))
        for r in p.get("recursos") or []:
            quienes.add(dueno_recurso(r, recursos))
        if p.get("seccion") != "biblioteca":
            # Un recurso del repositorio entre las fuentes: lo cuenta la pieza, y su autor lo dio de alta
            for x in p.get("fuentes") or []:
                quienes.add(dueno_recurso({"url": x.get("url", "")}, recursos))
            if m and es_persona(m) and nombra(p, m.get("autor", "").strip()):
                quienes.add(int(m["autor_id"]))
            # El anuncio del bot de un recurso nuevo: «Nombre (@usuario) ha creado…», si la pieza lo nombra
            elif m and not es_persona(m):
                for nombre, usuario in re.findall(r"([^\n()]+?)\s*\(@(\w+)\)", m.get("texto", "")):
                    if usuario.lower() in por_usuario and nombra(p, nombre.strip()):
                        quienes.add(por_usuario[usuario.lower()])
        for uid in quienes - {None}:
            if p["id"] not in personas.setdefault(uid, []):
                personas[uid].append(p["id"])
    salida = []
    for uid, ids in personas.items():
        piezas = []
        for pid in ids:
            t = titulares(fecha, pid)
            piezas.append({c: {"titular": t.get(c) or t.get("es", ""),
                               "url": f"{generar.BASE}{'' if c == 'es' else c + '/'}{fecha}/{pid}.html"}
                           for c in IDIOMAS})
        salida.append({"id": uid, "piezas": piezas})
    avisos = json.loads(f.read_text())
    avisos["personas"] = salida
    f.write_text(json.dumps(avisos, ensure_ascii=False, indent=2) + "\n")
    print(f"avisos-personas: {len(salida)} persona(s), {sum(len(x['piezas']) for x in salida)} pieza(s)")


if __name__ == "__main__":
    main()
