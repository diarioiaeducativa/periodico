#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La columna de opinión de los miércoles (ADR 0092), sin IA: el material del columnista, la comprobación de lo
que escribe y la columna de reserva.

  columna.py preparar FECHA [--reserva]   el encargo con el material y la forma de la respuesta en columnas-trabajo/FECHA/
                                          (reserva-FECHA/ con --reserva)
  columna.py importar FECHA AUTOR [--reserva]   columnas-trabajo/FECHA/columna.json → columnas-borrador/FECHA.json
  columna.py comprobar ARCHIVO            dice si vale (sale con 1 y el motivo si no)
  columna.py reserva                      la ruta de la columna de reserva, si la hay
  columna.py guardar FECHA                columnas-borrador/reserva-FECHA-verificada.json → reserva/columnas/FECHA.json
  columna.py usar FECHA                   la de reserva pasa a columnas/FECHA.json (y deja de estar en reserva)
  columna.py descartar                    quita la de reserva

FECHA es la de las conversaciones del número del miércoles (el martes), como en noche.sh.
"""
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RESERVA = RAIZ / "reserva" / "columnas"
PALABRAS = (550, 850)   # el encargo pide de 600 a 800; el margen evita repetir por diez palabras
MAX_TITULAR = 90

MODO_SEMANA = """Esta es la columna del miércoles {PUBLICA}: el material son los mensajes de los grupos de los siete
días que acaban el {FECHA} y lo que el diario publicó esos días. Elige el debate más vivo de esa semana."""
MODO_RESERVA = """Esta es la **columna de reserva**: sale un miércoles en que la de la semana no valga, quizá dentro de
varias semanas. Elige un debate de las últimas semanas que siga abierto y no dependa de la actualidad de unos
días: que se pueda leer igual dentro de un mes. Escribe sin referencias temporales («esta semana», «ayer»)."""


def principios():
    """La línea de la opinión, del apartado de las normas públicas (docs/como-se-hace.md, ADR 0092): un solo texto
    para el lector y para el columnista."""
    t = (RAIZ / "docs" / "como-se-hace.md").read_text()
    m = re.search(r"^## \d+\. La línea de la opinión\n(.*?)(?=^## )", t, re.S | re.M)
    if not m:
        raise SystemExit("columna: no encuentro «La línea de la opinión» en docs/como-se-hace.md")
    return m.group(1).split("**Quién los aplica**")[0].strip()


def dias(fecha, n):
    f = datetime.date.fromisoformat(fecha)
    return [(f - datetime.timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


def palabras(p):
    texto = " ".join(p.get("cuerpo") or [])
    texto = re.sub(r"\]\([^)]*\)", "]", texto)   # sin las direcciones de los enlaces
    return len(re.findall(r"\w+", texto))


def anteriores():
    lineas = []
    for f in sorted((RAIZ / "columnas").glob("*.json")) + sorted(RESERVA.glob("*.json")):
        d = json.loads(f.read_text())
        for p in d.get("piezas") or []:
            de = "reserva" if f.parent == RESERVA else f"publicada con el número del {f.stem}"
            lineas.append(f"- {p.get('titular')} ({de}): {p.get('entradilla')}")
    return "# Columnas anteriores\n\n" + ("\n".join(lineas) if lineas else "Todavía no hay ninguna.") + "\n"


def nombre(fecha, reserva):
    """La de reserva trabaja aparte: la mañana del miércoles se escribe con la fecha del martes, la de la semana."""
    return f"reserva-{fecha}" if reserva else fecha


ESQUEMA = {   # la respuesta del columnista, comprobada por Codex con --output-schema (como el agente de noticias)
    "type": "object", "additionalProperties": False,
    "required": ["hay_pieza", "motivo", "id", "antetitulo", "titular", "entradilla", "cuerpo", "fuentes", "nota"],
    "properties": {
        "hay_pieza": {"type": "boolean"}, "motivo": {"type": "string"}, "id": {"type": "string"},
        "antetitulo": {"type": "string"}, "titular": {"type": "string"}, "entradilla": {"type": "string"},
        "cuerpo": {"type": "array", "items": {"type": "string"}},
        "fuentes": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["titulo", "url"],
                                               "properties": {"titulo": {"type": "string"}, "url": {"type": "string"}}}},
        "nota": {"type": "string"},
    },
}


def mensajes(texto):
    """Los mensajes de un día sin el «Contexto: día anterior» de cada grupo, que ya está en el día de antes."""
    return re.sub(r"### Contexto:.*?(?=\n## |\n### (?!Contexto)|\Z)", "", texto, flags=re.S)


def preparar(fecha, reserva):
    """El encargo con todo el material dentro (prompt.md) y la forma de la respuesta (esquema.json): el columnista
    no tiene terminal ni archivos, solo la búsqueda en la web (ADR 0092)."""
    t = RAIZ / "columnas-trabajo" / nombre(fecha, reserva)
    shutil.rmtree(t, ignore_errors=True)
    t.mkdir(parents=True)
    partes, hay = [], 0
    for d in dias(fecha, 7):
        f = RAIZ / "dias" / f"{d}.md"
        if f.exists():
            partes.append(mensajes(f.read_text()))
            hay += 1
    if not hay:
        sys.exit(f"columna: no hay mensajes de los grupos en dias/ para {fecha}")
    publicado = []   # lo que publicó el diario: titular, entradilla y fuentes, con la clave para enlazarlo
    for d in dias(fecha, 28 if reserva else 7):
        f = RAIZ / "ediciones" / f"{d}.json"
        for p in (json.loads(f.read_text()).get("piezas") or []) if f.exists() else []:
            fuentes = "; ".join(x.get("url", "") for x in p.get("fuentes") or [])
            publicado.append(f"- pieza:{d}/{p.get('id')} · {p.get('seccion')} · {p.get('titular')}. {p.get('entradilla')}"
                             + (f" Fuentes: {fuentes}" if fuentes else ""))
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    modo = (MODO_RESERVA if reserva else MODO_SEMANA).replace("{FECHA}", fecha).replace("{PUBLICA}", publica)
    encargo = (RAIZ / "encargos" / "columna.md").read_text().replace("{MODO}", modo)
    claves = (RAIZ / "publicado.txt").read_text() if (RAIZ / "publicado.txt").exists() else ""
    prompt = (encargo + "\n\n# MATERIAL\n\n## Los mensajes de los grupos\n\n" + "\n\n".join(partes)
              + "\n\n## Lo que publicó el diario\n\n" + "\n".join(publicado)
              + "\n\n## Todo lo publicado, con su clave (solo se puede enlazar lo que está aquí)\n\n" + claves
              + "\n\n" + anteriores()
              + "\n\n## Los principios del diario\n\n" + principios()
              + "\n\n## El libro de estilo del diario\n\n" + (RAIZ / "encargos" / "estilo.md").read_text())
    (t / "prompt.md").write_text(prompt)
    (t / "esquema.json").write_text(json.dumps(ESQUEMA, ensure_ascii=False, indent=1))
    print(f"columna: encargo con {hay} días de mensajes ({len(prompt) // 1000} kB) en {t.relative_to(RAIZ)}")


def importar(fecha, autor, reserva):
    """La respuesta del columnista (columna.json, la que devuelve Codex) → columnas-borrador/, con la forma de las
    piezas del diario."""
    t = RAIZ / "columnas-trabajo" / nombre(fecha, reserva)
    r = json.loads((t / "columna.json").read_text())
    if r.get("hay_pieza"):
        cuerpo = r.get("cuerpo") or []
        if len(cuerpo) == 1:
            cuerpo = [x.strip() for x in re.split(r"\n\s*\n", cuerpo[0]) if x.strip()]
        d = {"fecha": fecha, "hay_pieza": True, "piezas": [{
            "id": r.get("id"), "seccion": "opinion", "importancia": 8, "autor": autor,
            "antetitulo": r.get("antetitulo"), "titular": r.get("titular"), "entradilla": r.get("entradilla"),
            "cuerpo": cuerpo, "fuentes": r.get("fuentes") or []}]}
    else:
        d = {"fecha": fecha, "hay_pieza": False, "motivo": r.get("motivo") or "sin motivo"}
    b = RAIZ / "columnas-borrador"
    b.mkdir(exist_ok=True)
    (b / f"{nombre(fecha, reserva)}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    (b / f"{nombre(fecha, reserva)}-nota.md").write_text(r.get("nota") or "")


def comprobar(archivo):
    try:
        d = json.loads(Path(archivo).read_text())
    except Exception as ex:
        return [f"no es un JSON válido ({ex})"]
    if not d.get("hay_pieza"):
        return [f"no hay columna: {d.get('motivo', 'sin motivo')}"]
    ps = d.get("piezas") or []
    if len(ps) != 1:
        return ["tiene que haber una sola columna"]
    p, malos = ps[0], []
    for k in ("id", "titular", "entradilla", "cuerpo", "autor"):
        if not p.get(k):
            malos.append(f"le falta {k}")
    if p.get("id") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["id"]):
        malos.append("el id no es de minúsculas y guiones")
    if len(p.get("titular") or "") > MAX_TITULAR:
        malos.append(f"el titular pasa de {MAX_TITULAR} caracteres")
    n = palabras(p)
    if not PALABRAS[0] <= n <= PALABRAS[1]:
        malos.append(f"tiene {n} palabras (de {PALABRAS[0]} a {PALABRAS[1]})")
    if not isinstance(p.get("cuerpo"), list) or len(p["cuerpo"]) < 3:
        malos.append("el cuerpo no es una lista de párrafos")
    if not any(re.search(r"\]\(https?://", x) for x in p.get("cuerpo") or []):
        malos.append("no enlaza ninguna fuente en el texto")
    for f in p.get("fuentes") or []:
        if not (f.get("titulo") and str(f.get("url", "")).startswith("http")):
            malos.append("una fuente sin título o sin dirección")
            break
    publicado = (RAIZ / "publicado.txt").read_text() if (RAIZ / "publicado.txt").exists() else ""
    for clave in re.findall(r"\(pieza:(\d{4}-\d{2}-\d{2}/[\w-]+)\)", " ".join(p.get("cuerpo") or [])):
        if f"pieza:{clave}" not in publicado:
            malos.append(f"enlaza pieza:{clave}, que no está publicada")
    return malos


def la_reserva():
    fs = sorted(RESERVA.glob("*.json"))
    return fs[0] if fs else None


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "preparar":
        preparar(sys.argv[2], "--reserva" in sys.argv[3:])
    elif orden == "importar":
        importar(sys.argv[2], sys.argv[3], "--reserva" in sys.argv[4:])
    elif orden == "comprobar":
        malos = comprobar(sys.argv[2])
        if malos:
            print("columna: " + "; ".join(malos))
            sys.exit(1)
    elif orden == "reserva":
        r = la_reserva()
        if r:
            print(r.relative_to(RAIZ))
    elif orden == "guardar":
        RESERVA.mkdir(parents=True, exist_ok=True)
        origen = RAIZ / "columnas-borrador" / f"reserva-{sys.argv[2]}-verificada.json"
        malos = comprobar(origen)
        if malos:
            sys.exit("columna de reserva no guardada: " + "; ".join(malos))
        shutil.copy(origen, RESERVA / f"{sys.argv[2]}.json")
        print(f"columna de reserva guardada: reserva/columnas/{sys.argv[2]}.json")
    elif orden == "usar":
        r = la_reserva()
        if not r:
            sys.exit("columna: no hay ninguna de reserva")
        d = json.loads(r.read_text())
        d["fecha"], d["reserva"] = sys.argv[2], r.stem
        (RAIZ / "columnas").mkdir(exist_ok=True)
        (RAIZ / "columnas" / f"{sys.argv[2]}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        r.unlink()
        print(f"columna: sale la de reserva {r.stem}")
    elif orden == "descartar":
        r = la_reserva()
        if r:
            r.unlink()
            print(f"columna: descartada la de reserva {r.stem}")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
