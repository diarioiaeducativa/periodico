#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Los resúmenes del vídeo y del pódcast semanales de cada grupo en las otras lenguas (ADR 0057 y 0101). Sin IA: solo dice qué falta por
traducir y comprueba lo traducido.

    scripts/multimedia.py pendientes                 una línea por semana con algo por traducir: «AAAA-WW ca gl…»
    scripts/multimedia.py traduccion SEMANA IDIOMA   comprueba la traducción; si no vale, la quita

El boletín semanal deja en multimedia/AAAA-WW.json, en castellano, unas 70 palabras sobre lo que cuenta el
vídeo de cada grupo, y puede cambiarlas después (añade un grupo, corrige una cifra). La traducción vive en
multimedia-XX/AAAA-WW.json, solo con el resumen de cada grupo y, en `origen`, el texto en castellano del que
salió: lo apunta este programa al darla por buena. Si el resumen en castellano cambia, `origen` deja de
coincidir, generar.py vuelve a enseñar el castellano y la semana vuelve a estar pendiente.

«traduccion» sale con 1 si ha quitado el archivo, y lo dice en una línea."""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import idiomas  # noqa: E402


def leer(f):
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return None


# Cada resumen y la clave en que la traducción guarda el texto en castellano del que salió
CAMPOS = {"resumen": "origen", "resumen_podcast": "origen_podcast"}


def resumenes(sem):
    """{grupo: {campo: resumen en castellano}} de los grupos que tienen alguno."""
    d = leer(RAIZ / "multimedia" / f"{sem}.json") or {}
    g = d.get("grupos")
    r = {}
    for k, v in (g if isinstance(g, dict) else {}).items():
        x = {c: v[c].strip() for c in CAMPOS if isinstance(v, dict) and isinstance(v.get(c), str) and v[c].strip()}
        if x:
            r[k] = x
    return r


def al_dia(sem, c):
    """Si la traducción a ese idioma tiene todos los resúmenes y salió del texto de ahora."""
    t = (leer(RAIZ / f"multimedia-{c}" / f"{sem}.json") or {}).get("grupos")
    t = t if isinstance(t, dict) else {}
    return all(isinstance(t.get(g), dict) and t[g].get(CAMPOS[k]) == r and (t[g].get(k) or "").strip()
               for g, x in resumenes(sem).items() for k, r in x.items())


def pendientes():
    for f in sorted((RAIZ / "multimedia").glob("20??-??.json")):
        if not resumenes(f.stem):
            continue
        faltan = [c for c in idiomas.IDIOMAS if not al_dia(f.stem, c)]
        if faltan:
            yield f.stem, faltan


def traduccion(sem, c):
    """Comprueba lo que ha dejado el traductor y, si vale, apunta de qué texto salió cada resumen."""
    f = RAIZ / f"multimedia-{c}" / f"{sem}.json"
    orig = resumenes(sem)
    if not f.exists() or not orig:
        return []
    t = leer(f)
    grupos = (t or {}).get("grupos") if isinstance(t, dict) else None
    malos = []
    if not isinstance(grupos, dict):
        malos.append("no es un JSON válido con sus grupos")
    else:
        for g, campos in orig.items():
            x = grupos.get(g)
            for k, r in campos.items():
                tr = (x.get(k) or "").strip() if isinstance(x, dict) and isinstance(x.get(k), str) else ""
                if not tr:
                    malos.append(f"{g}: falta {k}")
                elif tr == r:
                    malos.append(f"{g}: {k} está sin traducir")
                elif not 0.5 <= len(tr) / len(r) <= 2.0:
                    malos.append(f"{g}: el largo de {k} no cuadra ({len(tr)} frente a {len(r)} caracteres)")
    if malos:
        f.unlink()
        return [f"multimedia-{c}/{sem}.json quitado: " + "; ".join(malos)]
    limpio = {"semana": sem, "grupos": {g: {kk: v for k, r in campos.items() for kk, v in ((k, grupos[g][k].strip()), (CAMPOS[k], r))}
                                        for g, campos in orig.items()}}
    f.write_text(json.dumps(limpio, ensure_ascii=False, indent=2) + "\n")
    return []


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "pendientes":
        for sem, faltan in pendientes():
            print(sem, " ".join(faltan))
    elif orden == "traduccion" and len(sys.argv) == 4:
        quitado = traduccion(sys.argv[2], sys.argv[3])
        for linea in quitado:
            print(f"traducción: {linea}")
        sys.exit(1 if quitado else 0)
    else:
        print(__doc__)
        sys.exit(2)
