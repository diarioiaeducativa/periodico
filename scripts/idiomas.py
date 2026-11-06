#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las traducciones de la redacción (ADR 0026): los datos de cada idioma para los encargos del
traductor y la comprobación de lo traducido, sin IA.

    scripts/idiomas.py lista                          los idiomas a los que se traduce
    scripts/idiomas.py encargo PASO IDIOMA            el encargo encargos/pasos/PASO.md para ese idioma
    scripts/idiomas.py comprobar TIPO FECHA IDIOMA    comprueba lo traducido; quita lo que no vale

TIPO: edicion (edición, viñeta y dibujos), dibujos, biblioteca, repositorio o reportaje. Lo que se
quita deja la página de ese idioma con el castellano, como cuando falta una traducción. Sale con 1
si ha quitado algo, y lo dice en una línea."""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent

IDIOMAS = {
    "ca": {
        "LENGUA": "catalán", "NORMA": "estándar del IEC, natural, periodístico; «el professorat», «l'alumnat»",
        "MARCAS": "«(en castellà)» o «(en anglès)»", "PERSONAJES": "Guix i Algorisme", "NOTA": "automàtica amb IA",
        "ANTETITULOS": "«Nou al repositori», «La setmana del repositori» o «Del fons del repositori»",
        "REPOSITORIO": "«el Repositori de recursos de Vibe Coding Educativo»",
    },
    "gl": {
        "LENGUA": "gallego", "NORMA": "normativa de la Real Academia Galega, natural, periodístico; «o profesorado», «o alumnado»",
        "MARCAS": "«(en castelán)» o «(en inglés)»", "PERSONAJES": "Xiz e Algoritmo", "NOTA": "automática con IA",
        "ANTETITULOS": "«Novo no repositorio», «A semana do repositorio» o «Do fondo do repositorio»",
        "REPOSITORIO": "«o Repositorio de recursos de Vibe Coding Educativo»",
    },
    "eu": {
        "LENGUA": "euskera", "NORMA": "euskera batua según Euskaltzaindia, natural, periodístico; «irakasleak», «ikasleak»; "
                                      "«inteligencia artificial» es «adimen artifiziala» (AA)",
        "MARCAS": "«(gaztelaniaz)» o «(ingelesez)»", "PERSONAJES": "Klarion eta Algoritmo", "NOTA": "itzulpen automatikoa AArekin",
        "ANTETITULOS": "«Berria biltegian», «Biltegiaren astea» o «Biltegiaren fondotik»",
        "REPOSITORIO": "«Vibe Coding Educativoren Baliabideen biltegia»",
    },
    "en": {
        "LENGUA": "inglés", "NORMA": "inglés británico, natural, periodístico; «teachers», «students»",
        "MARCAS": "«(in Spanish)» o «(in Catalan)»", "PERSONAJES": "Chalk and Algorithm", "NOTA": "automatic AI translation",
        "ANTETITULOS": "«New in the repository», «The repository's week» o «From the repository's back catalogue»",
        "REPOSITORIO": "«the Vibe Coding Educativo resource repository»",
    },
}


def encargo(paso, c):
    t = (RAIZ / "encargos" / "pasos" / f"{paso}.md").read_text()
    datos = dict(IDIOMAS[c], SUF=f"-{c}")
    for k, v in datos.items():
        t = t.replace("{" + k + "}", v)
    return t


ENLACE = re.compile(r"\]\((?:https?://|pieza:)")


def textos(x):
    """Todo el texto de un JSON, para comparar largos y enlaces."""
    if isinstance(x, str):
        return [x]
    if isinstance(x, list):
        return [t for y in x for t in textos(y)]
    if isinstance(x, dict):
        return [t for k, y in x.items() if k not in ("comprobado", "repaso", "motivo", "descartado", "ilustracion") for t in textos(y)]
    return []


def problemas_piezas(orig, trad, lista="piezas"):
    """Lo que no cuadra entre una lista de piezas y su traducción."""
    p_o, p_t = orig.get(lista) or [], trad.get(lista) or []
    if [p.get("id") for p in p_o] != [p.get("id") for p in p_t]:
        return ["no tiene las mismas piezas"]
    malos = []
    for a, b in zip(p_o, p_t):
        for campo in ("titular", "entradilla"):
            if a.get(campo) and not (b.get(campo) or "").strip():
                malos.append(f'{a["id"]}: falta {campo}')
        if len(a.get("cuerpo") or []) != len(b.get("cuerpo") or []):
            malos.append(f'{a["id"]}: no tiene los mismos párrafos')
        ta, tb = " ".join(textos(a)), " ".join(textos(b))
        if len(ENLACE.findall(ta)) != len(ENLACE.findall(tb)):
            malos.append(f'{a["id"]}: no tiene los mismos enlaces')
        if ta and not 0.5 <= len(tb) / len(ta) <= 2.0:
            malos.append(f'{a["id"]}: el largo no cuadra ({len(tb)} frente a {len(ta)} caracteres)')
    return malos


def leer(f):
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return None


def comprobar_json(carpeta, fecha, c, lista="piezas"):
    orig, f = RAIZ / carpeta / f"{fecha}.json", RAIZ / f"{carpeta}-{c}" / f"{fecha}.json"
    if not f.exists() or not orig.exists():
        return []
    trad = leer(f)
    malos = ["no es un JSON válido"] if trad is None else problemas_piezas(leer(orig) or {}, trad, lista)
    if carpeta == "ediciones" and trad is not None:
        o = leer(orig) or {}
        if len(o.get("breves") or []) != len(trad.get("breves") or []):
            malos.append("no tiene los mismos breves")
    if malos:
        f.unlink()
        return [f"{carpeta}-{c}/{fecha}.json quitado: " + "; ".join(malos)]
    return []


def comprobar_vineta(fecha, c):
    orig, f = RAIZ / "vinetas" / f"{fecha}.json", RAIZ / f"vinetas-{c}" / f"{fecha}.json"
    if not f.exists():
        return []
    o, t = leer(orig) or {}, leer(f)
    malos = []
    if t is None:
        malos.append("no es un JSON válido")
    else:
        vo = (((o.get("elegida") or {}).get("guion")) or {}).get("vinetas") or []
        vt = (((t.get("elegida") or {}).get("guion")) or {}).get("vinetas") or []
        if len(vo) != len(vt):
            malos.append("no tiene las mismas viñetas")
        else:
            for i, (a, b) in enumerate(zip(vo, vt), 1):
                if len(a.get("bocadillos") or []) != len(b.get("bocadillos") or []):
                    malos.append(f"viñeta {i}: no tiene los mismos bocadillos")
                if any(not (x.get("texto") or "").strip() for x in b.get("bocadillos") or []):
                    malos.append(f"viñeta {i}: un bocadillo vacío")
    if malos:
        f.unlink()
        return [f"vinetas-{c}/{fecha}.json quitado: " + "; ".join(malos)]
    return []


def comprobar_dibujos(fecha, c):
    salida = []
    for f in sorted((RAIZ / f"ilustraciones-{c}").glob(f"{fecha}-*.svg")):
        try:
            raiz = ET.parse(f).getroot()
            if not raiz.tag.endswith("svg"):
                raise ValueError("no es un SVG")
        except (ET.ParseError, ValueError) as ex:
            f.unlink()
            salida.append(f"ilustraciones-{c}/{f.name} quitado: {ex}")
    return salida


def comprobar(tipo, fecha, c):
    if tipo == "edicion":
        return comprobar_json("ediciones", fecha, c) + comprobar_vineta(fecha, c) + comprobar_dibujos(fecha, c)
    if tipo == "dibujos":
        return comprobar_dibujos(fecha, c)
    if tipo == "reportaje":
        orig, f = RAIZ / "reportajes" / f"{fecha}.json", RAIZ / f"reportajes-{c}" / f"{fecha}.json"
        salida = comprobar_dibujos(fecha, c)
        if f.exists() and orig.exists():
            o, t = leer(orig) or {}, leer(f)
            malos = []
            if t is None:
                malos.append("no es un JSON válido")
            else:
                if len(o.get("apartados") or []) != len(t.get("apartados") or []):
                    malos.append("no tiene los mismos apartados")
                ta, tb = " ".join(textos(o)), " ".join(textos(t))
                if len(ENLACE.findall(ta)) != len(ENLACE.findall(tb)):
                    malos.append("no tiene los mismos enlaces")
                if ta and not 0.5 <= len(tb) / len(ta) <= 2.0:
                    malos.append(f"el largo no cuadra ({len(tb)} frente a {len(ta)} caracteres)")
            if malos:
                f.unlink()
                salida.append(f"reportajes-{c}/{fecha}.json quitado: " + "; ".join(malos))
        return salida
    if tipo in ("biblioteca", "repositorio"):
        return comprobar_json(tipo, fecha, c) + comprobar_dibujos(fecha, c)
    raise SystemExit(f"tipo desconocido: {tipo}")


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "lista":
        print(" ".join(IDIOMAS))
    elif orden == "encargo":
        sys.stdout.write(encargo(sys.argv[2], sys.argv[3]))
    elif orden == "comprobar":
        quitado = comprobar(sys.argv[2], sys.argv[3], sys.argv[4])
        for linea in quitado:
            print(f"traducción: {linea}")
        sys.exit(1 if quitado else 0)
    else:
        print(__doc__)
        sys.exit(2)
