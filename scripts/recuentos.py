#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Los rótulos con número de los dibujos y la comprobación de lo que dice de ellos el revisor (ADR 0089).

Un programa no sabe qué cuenta un número («Cuatro ámbitos» puede no ser lo que hay dibujado encima), así que
eso lo juzga el revisor visual (encargos/pasos/2b-revision-dibujos.md). Lo que hace este programa es obligarle a
juzgarlo y comprobar que lo ha hecho: saca del SVG los rótulos con número, y de la respuesta del revisor mira
que estén todos, que la frase que cita para cada uno esté de verdad en el texto de la pieza y que, si dice que el
número cuenta objetos del dibujo, el número de objetos coincida.

    recuentos.py rotulos ARCHIVO.svg     los rótulos con número de un dibujo
    recuentos.py comprobar FECHA         comprueba revision/FECHA/visual.json contra revision/FECHA/es.json;
                                         deja revision/FECHA/recuentos.json ({"faltan": {id: [...]},
                                         "errores": {id: [...]}}) y escribe en una línea los id con algo;
                                         sale con 3 si el revisor ha dejado algo sin comprobar, 4 si solo hay
                                         recuentos que no cuadran y 0 si todo está bien
    recuentos.py inventario              los dibujos en castellano publicados y de reserva con rótulos con número
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# «un», «una» y «uno» no: salen en rótulos que no cuentan nada («Una columna»)
PALABRAS = {
    "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19, "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
    "cien": 100, "ciento": 100, "doscientos": 200, "quinientos": 500, "mil": 1000, "doble": None, "triple": None,
}
NUMERO = re.compile(r"\d+|\b(" + "|".join(PALABRAS) + r")\b", re.I)
# Lo que lleva cifras pero no cuenta nada: años, versiones (5.2, v3), horas (7:00), ordinales (4.º), «3D», «360p», «MP3»
NO_CUENTA = re.compile(r"\b(19|20)\d\d\b|\d+[.,]\d+|\d+:\d+|\d+\.[ºª]|\b\d+[A-Za-z]+\b|\b[A-Za-z]+\d+\b")


def cuenta_algo(rotulo):
    """Si el rótulo lleva un número que puede contar algo, una vez quitado lo que no cuenta nada."""
    return bool(NUMERO.search(NO_CUENTA.sub(" ", rotulo)))


def numero(rotulo):
    """El número de un rótulo: el entero si es una cifra o una palabra de número; None si no lo es exacto."""
    m = NUMERO.search(NO_CUENTA.sub(" ", rotulo))
    if not m:
        return None
    t = m.group(0).lower()
    return int(t) if t.isdigit() else PALABRAS.get(t)


def rotulos(svg):
    """Los rótulos de un SVG que llevan un número, en el orden en que aparecen (sin repetir)."""
    try:
        raiz = ET.fromstring(pathlib.Path(svg).read_text())
    except (ET.ParseError, OSError):
        return []
    out = []
    for el in raiz.iter():
        if el.tag.rsplit("}", 1)[-1] != "text":
            continue
        t = " ".join("".join(el.itertext()).split())
        if t and cuenta_algo(t) and t not in [r["rotulo"] for r in out]:
            out.append({"rotulo": t, "numero": numero(t)})
    return out


def normal(s):
    """Para comparar una cita con el texto: sin enlaces ni marcas, sin comillas, en minúscula y con un solo espacio."""
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s or "")
    s = re.sub(r"[*_`«»“”\"‘’']", "", s)
    return " ".join(s.lower().split())


def texto(p):
    """Todo el texto que lee el público de una pieza, del titular a las claves del reportaje."""
    partes = [p.get("antetitulo"), p.get("titular"), p.get("entradilla")]
    cuerpo = p.get("cuerpo")
    partes += cuerpo if isinstance(cuerpo, list) else [cuerpo]
    for a in p.get("apartados") or []:
        partes += [a.get("ladillo")] + list(a.get("parrafos") or [])
    for c in p.get("claves") or []:
        partes += [json.dumps(c, ensure_ascii=False) if isinstance(c, dict) else c]
    return normal(" ".join(x for x in partes if isinstance(x, str)))


def piezas(fecha, base=RAIZ):
    """Las piezas de un día con su id, como las busca revisar-dibujos.py."""
    out = []
    for carpeta in ("ediciones", "biblioteca", "hace-un-ano"):
        f = base / carpeta / f"{fecha}.json"
        if f.exists():
            d = json.loads(f.read_text())
            out += d.get("piezas", []) + ([d["editorial"]] if d.get("editorial") else [])
    rep = base / "reportajes" / f"{fecha}.json"
    if rep.exists():
        r = json.loads(rep.read_text())
        if r.get("hay_reportaje"):
            out.append(r)
    return out


def comprobar(fecha):
    d = RAIZ / "revision" / fecha
    prog = json.loads((d / "es.json").read_text())["dibujos"]
    try:
        vis = {x["id"]: x for x in json.loads((d / "visual.json").read_text())["dibujos"]}
    except Exception:
        vis = {}
    textos = {p["id"]: texto(p) for p in piezas(fecha)}
    faltan, errores = {}, {}
    for x in prog:
        lista = rotulos(RAIZ / x["svg"])
        # Sin respuesta del revisor (no ha llegado a ejecutarse: límite de uso, fallo), como antes del ADR 0089:
        # el dibujo no se retira por eso
        if not lista or x["id"] not in vis:
            continue
        dichos = {normal(r.get("rotulo")): r for r in (vis.get(x["id"], {}).get("recuentos") or []) if isinstance(r, dict)}
        t = textos.get(x["id"], "")
        for r in lista:
            v = dichos.get(normal(r["rotulo"]))
            if not v:
                faltan.setdefault(x["id"], []).append(f"el revisor no ha comprobado el rótulo «{r['rotulo']}» con el texto")
                continue
            frase = normal(v.get("frase"))
            if len(frase) < 12 or frase not in t:
                faltan.setdefault(x["id"], []).append(
                    f"la frase citada para el rótulo «{r['rotulo']}» no está en el texto de la pieza: «{v.get('frase', '')}»")
                continue
            objetos = v.get("objetos")
            if isinstance(objetos, int) and r["numero"] is not None and objetos != r["numero"]:
                errores.setdefault(x["id"], []).append(
                    f"el rótulo «{r['rotulo']}» dice {r['numero']}, pero el dibujo muestra {objetos} "
                    f"({v.get('cuenta') or 'sin decir qué cuenta'}): o se dibujan {r['numero']} o el rótulo nombra lo que se ve")
    (d / "recuentos.json").write_text(json.dumps({"faltan": faltan, "errores": errores}, ensure_ascii=False, indent=1))
    return faltan, errores


def inventario():
    """Cada dibujo en castellano con rótulos con número: lo publicado y lo de la reserva."""
    out = []
    for svg in sorted((RAIZ / "ilustraciones").glob("*.svg")) + sorted((RAIZ / "reserva").glob("**/ilustraciones/*.svg")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.svg$", svg.name)
        if not m:
            continue
        lista = rotulos(svg)
        if lista:
            out.append({"svg": str(svg.relative_to(RAIZ)), "fecha": m.group(1), "id": m.group(2), "rotulos": lista})
    return out


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "rotulos" and len(sys.argv) == 3:
        print(json.dumps(rotulos(sys.argv[2]), ensure_ascii=False))
    elif orden == "comprobar" and len(sys.argv) == 3:
        faltan, errores = comprobar(sys.argv[2])
        for i, m in list(faltan.items()) + list(errores.items()):
            print(f"recuentos {i}: " + "; ".join(m), file=sys.stderr)
        print(" ".join(sorted(set(faltan) | set(errores))))
        return 3 if faltan else 4 if errores else 0
    elif orden == "inventario":
        print(json.dumps(inventario(), ensure_ascii=False, indent=1))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
