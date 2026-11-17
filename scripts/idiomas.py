#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las traducciones de la redacción (ADR 0026): los datos de cada idioma para los encargos del
traductor y la comprobación de lo traducido, sin IA.

    scripts/idiomas.py lista                          los idiomas a los que se traduce
    scripts/idiomas.py encargo PASO IDIOMA            el encargo encargos/pasos/PASO.md para ese idioma
    scripts/idiomas.py comprobar TIPO FECHA IDIOMA [--conservar] [--mirar]   comprueba lo traducido; quita lo que no vale
                                                      (con --mirar, solo lo dice)
    scripts/idiomas.py falta TIPO FECHA IDIOMA        dice lo que tenía que estar traducido y no está

TIPO: edicion (edición, viñeta y dibujos), dibujos, vineta (la de reserva, sola), biblioteca, repositorio, reportaje, hace-un-ano, comentario-semana
o multimedia (estos dos, con la semana AAAA-WW en lugar de la fecha). Lo que se
quita deja la página de ese idioma con el castellano, como cuando falta una traducción. Sale con 1
si ha quitado algo, y lo dice en una línea. `traducir.sh` repite entonces la traducción una vez, y esa segunda
vez comprueba con --conservar: si las piezas son las mismas y solo fallan algunas, el archivo se queda, con esas
piezas en castellano (`sin_traducir`) y las demás traducidas, para que un artículo no deje sin traducir el número."""
import copy
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from forma import parrafos  # noqa: E402

IDIOMAS = {
    "ca": {
        "LENGUA": "catalán", "NORMA": "estándar del IEC, natural, periodístico; «el professorat», «l'alumnat»; «soc», sin tilde; las etapas educativas, en minúscula («primària», «batxillerat»); la entradilla es «l'entradeta»",
        "MARCAS": "«(en castellà)» o «(en anglès)»", "PERSONAJES": "Guix i Algorisme", "NOTA": "automàtica amb IA",
        "ANTETITULOS": "«Nou al repositori», «La setmana del repositori» o «Del fons del repositori»",
        "REPOSITORIO": "«el Repositori de recursos de Vibe Coding Educativo»",
    },
    "gl": {
        "LENGUA": "gallego", "NORMA": "normativa de la Real Academia Galega, natural, periodístico; «o profesorado», «o alumnado»; cuida el género («o xiz») y evita castellanismos («encerado», no «pizarra»; «relatorios», no «ponencias»)",
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
        "LENGUA": "inglés", "NORMA": "inglés británico, natural, periodístico; «teachers», «students»; el diario se llama a sí mismo «the paper», nunca «the diary»; lo que en origen se dijo en inglés se copia de la fuente, no se retraduce; las comillas son las inglesas (“ ”), nunca las españolas (« »), y el porcentaje va pegado a la cifra (25%)",
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

MIRAR = False   # con --mirar, comprobar dice lo que quitaría y no toca nada (lo usa el reparador para medir)


def quitar(f):
    if not MIRAR:
        f.unlink()


def textos(x):
    """Todo el texto de un JSON, para comparar largos y enlaces."""
    if isinstance(x, str):
        return [x]
    if isinstance(x, list):
        return [t for y in x for t in textos(y)]
    if isinstance(x, dict):
        return [t for k, y in x.items() if k not in ("comprobado", "repaso", "motivo", "descartado", "ilustracion") for t in textos(y)]
    return []


def problemas_por_pieza(orig, trad, lista="piezas"):
    """Lo que no cuadra entre una lista de piezas y su traducción: None si no son las mismas piezas; si lo
    son, {id: [problemas]} con las que fallan. Los párrafos se cuentan como los cuenta el generador: un cuerpo
    que es un texto seguido vale lo mismo que su lista de párrafos (scripts/forma.py)."""
    p_o, p_t = orig.get(lista) or [], trad.get(lista) or []
    if [p.get("id") for p in p_o] != [p.get("id") for p in p_t]:
        return None
    malos = {}
    for a, b in zip(p_o, p_t):
        m = []
        for campo in ("titular", "entradilla"):
            if a.get(campo) and not str(b.get(campo) or "").strip():
                m.append(f"falta {campo}")
        if len(parrafos(a.get("cuerpo")) or []) != len(parrafos(b.get("cuerpo")) or []):
            m.append("no tiene los mismos párrafos")
        ta, tb = " ".join(textos(a)), " ".join(textos(b))
        if len(ENLACE.findall(ta)) != len(ENLACE.findall(tb)):
            m.append("no tiene los mismos enlaces")
        if ta and not 0.5 <= len(tb) / len(ta) <= 2.0:
            m.append(f"el largo no cuadra ({len(tb)} frente a {len(ta)} caracteres)")
        if valores_grafico(a) != valores_grafico(b):
            m.append("el gráfico no tiene los mismos datos")
        if m:
            malos[a["id"]] = m
    return malos


def problemas_piezas(orig, trad, lista="piezas"):
    """Lo mismo, en una lista de frases."""
    por = problemas_por_pieza(orig, trad, lista)
    return ["no tiene las mismas piezas"] if por is None else [f"{i}: {x}" for i, m in por.items() for x in m]


def valores_grafico(p):
    """Lo que no se traduce de un gráfico (ADR 0084): el tipo, la unidad, el número de etiquetas y los valores."""
    g = p.get("grafico") or {}
    return (g.get("tipo"), g.get("unidad"), len(g.get("etiquetas") or []),
            [s.get("valores") for s in g.get("series") or []]) if g else None


def leer(f):
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return None


def comprobar_json(carpeta, fecha, c, lista="piezas", conservar=False):
    """Comprueba una traducción con su original. Lo que no vale se quita; con `conservar` (el segundo intento),
    si las piezas son las mismas, el archivo se queda con las que fallan en castellano y las demás traducidas."""
    orig, f = RAIZ / carpeta / f"{fecha}.json", RAIZ / f"{carpeta}-{c}" / f"{fecha}.json"
    if not f.exists() or not orig.exists():
        return []
    nombre = f"{carpeta}-{c}/{fecha}.json"
    o, trad = leer(orig) or {}, leer(f)
    if not isinstance(trad, dict) or not isinstance(trad.get(lista) or [], list) \
            or not all(isinstance(p, dict) for p in trad.get(lista) or []):
        quitar(f)
        return [f"{nombre} quitado: " + ("no es un JSON válido" if trad is None else "no tiene la forma del original")]
    por = problemas_por_pieza(o, trad, lista)
    if por is None:
        quitar(f)
        return [f"{nombre} quitado: no tiene las mismas piezas"]
    breves_mal = carpeta == "ediciones" and len(o.get("breves") or []) != len(trad.get("breves") or [])
    malos = [f"{i}: {x}" for i, m in por.items() for x in m] + (["no tiene los mismos breves"] if breves_mal else [])
    if not malos:
        return []
    if not conservar:
        quitar(f)
        return [f"{nombre} quitado: " + "; ".join(malos)]
    for i, p in enumerate(trad.get(lista) or []):
        if p.get("id") in por:
            trad[lista][i] = dict(copy.deepcopy(o[lista][i]), sin_traducir=True)
    if breves_mal:
        trad["breves"] = copy.deepcopy(o.get("breves") or [])
    if not MIRAR:
        f.write_text(json.dumps(trad, ensure_ascii=False, indent=1) + "\n")
    return [f"{nombre}: sale en castellano solo lo que no vale ({'; '.join(malos)}); lo demás, traducido"]


# Lo que cada tipo tiene que dejar traducido: la carpeta y las claves que dicen que el original tiene algo
PRINCIPAL = {"edicion": ("ediciones", ("piezas", "breves")), "biblioteca": ("biblioteca", ("piezas",)),
             "repositorio": ("repositorio", ("piezas",)), "hace-un-ano": ("hace-un-ano", ("piezas",)),
             "reportaje": ("reportajes", ("apartados",)), "vineta": ("vinetas", ("elegida",))}


def falta(tipo, fecha, c):
    """Lo que tenía que estar traducido y no está: el traductor no lo escribió (se cortó, falló) o la
    comprobación lo quitó. Con el original vacío o sin original no falta nada."""
    pares = [PRINCIPAL[tipo]] if tipo in PRINCIPAL else []
    if tipo == "edicion":
        pares.append(PRINCIPAL["vineta"])
    salida = []
    for carpeta, claves in pares:
        o = leer(RAIZ / carpeta / f"{fecha}.json")
        if isinstance(o, dict) and any(o.get(k) for k in claves) and not (RAIZ / f"{carpeta}-{c}" / f"{fecha}.json").exists():
            salida.append(f"{carpeta}-{c}/{fecha}.json no está")
    return salida


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
        quitar(f)
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
            quitar(f)
            salida.append(f"ilustraciones-{c}/{f.name} quitado: {ex}")
    return salida


def comprobar(tipo, fecha, c, conservar=False):
    if tipo == "edicion":
        return comprobar_json("ediciones", fecha, c, conservar=conservar) + comprobar_vineta(fecha, c) + comprobar_dibujos(fecha, c)
    if tipo == "dibujos":
        return comprobar_dibujos(fecha, c)
    if tipo == "vineta":   # la viñeta de reserva, sola (ADR 0068)
        return comprobar_vineta(fecha, c)
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
                quitar(f)
                salida.append(f"reportajes-{c}/{fecha}.json quitado: " + "; ".join(malos))
        return salida
    if tipo in ("biblioteca", "repositorio"):
        return comprobar_json(tipo, fecha, c, conservar=conservar) + comprobar_dibujos(fecha, c)
    if tipo == "hace-un-ano":   # ADR 0040
        return comprobar_json(tipo, fecha, c, conservar=conservar) + comprobar_dibujos(fecha, c)
    if tipo == "comentario-semana":   # aquí «fecha» es la semana, AAAA-WW (ADR 0038)
        from comentario_semana import traduccion
        return traduccion(fecha, c)
    if tipo == "multimedia":   # el resumen del vídeo semanal de cada grupo, también por semanas (ADR 0057)
        from multimedia import traduccion
        return traduccion(fecha, c)
    raise SystemExit(f"tipo desconocido: {tipo}")


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "lista":
        print(" ".join(IDIOMAS))
    elif orden == "encargo":
        sys.stdout.write(encargo(sys.argv[2], sys.argv[3]))
    elif orden == "comprobar":
        MIRAR = "--mirar" in sys.argv[5:]
        quitado = comprobar(sys.argv[2], sys.argv[3], sys.argv[4], conservar="--conservar" in sys.argv[5:])
        for linea in quitado:
            print(f"traducción: {linea}")
        sys.exit(1 if quitado else 0)
    elif orden == "falta":
        faltan = falta(sys.argv[2], sys.argv[3], sys.argv[4])
        for linea in faltan:
            print(f"traducción: {linea}")
        sys.exit(1 if faltan else 0)
    else:
        print(__doc__)
        sys.exit(2)
