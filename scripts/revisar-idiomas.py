#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Busca castellano que se haya colado en las ediciones traducidas del sitio ya generado (ADR 0056).

El traductor traduce los campos que le dice su encargo; lo que queda fuera (un texto fijo del programa, la
ficha de un documento, el resumen de un vídeo, el rótulo de una viñeta para lectores de pantalla) sale en
castellano sin que nadie lo note. Este programa, sin IA, lee las páginas de `sitio/<idioma>/` y señala los
textos que parecen castellano: los que juntan varias palabras muy frecuentes en castellano que no existen
en esa lengua.

    scripts/revisar-idiomas.py                  todo el sitio
    scripts/revisar-idiomas.py --dia 2026-11-12 las páginas de ese día (su carpeta) y las fijas
    scripts/revisar-idiomas.py --idiomas ca,en  solo esos idiomas

Escribe una línea por hallazgo (idioma, página y el texto) y termina con 1 si hay alguno.

No se cuenta como castellano: lo marcado con `lang="es"`, los títulos en cursiva y entre comillas (obras y
citas, que no se traducen), las fuentes de «Comprobado en» (se citan con su título original), los nombres
propios de la lista y las páginas que guardan el texto de otros (los datos del widget). Es un detector de
errores de bulto: prefiere callar una frase dudosa a dar un aviso falso cada mañana.
"""
import argparse
import html
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"

# Palabras muy frecuentes en castellano que no son palabra en la otra lengua (o casi nunca lo son)
COMUNES = "los las una con para pero también según más muy cuando donde porque desde hasta sobre entre cada esta este estos estas sus son hay puede pueden hace hacen además mientras aunque todo todos todas años año nuevo nueva nuevos nuevas qué cómo así"
SOLO_ES = {
    # el catalán comparte «una», «sobre», «entre», «cada», «el», «del», «al», «en», «es», «se»…
    "ca": set("y los las con para pero también según más muy cuando donde porque desde hasta este estos estas sus hay puede pueden hace hacen además mientras aunque todo todos todas años año nuevo nueva nuevos nuevas qué cómo así lo su".split()),
    # el gallego comparte casi todo el vocabulario gramatical: quedan las formas que solo son castellanas
    "gl": set("y los las una uno unas unos también según más muy cuando donde hasta este estos hay puede pueden hace hacen además mientras aunque todo años año nuevo nueva nuevos nuevas qué cómo así lo su sus".split()),
    "eu": set(("y el la del al lo de en es se su " + COMUNES).split()) - set("de en".split()),
    "en": set(("y el la del al lo de en es se su " + COMUNES).split()) - set("de en son me".split()),
}
# Las que bastan solas: no se dan en esa lengua ni en un nombre propio corriente
FUERTES = {
    "ca": set("y con los las".split()),
    "gl": set("y los las una unos unas".split()),
    "eu": set("y con los las del para una".split()),
    "en": set("y con los las del para una".split()),
}
# Nombres propios y títulos que llevan palabras castellanas y no se traducen
PROPIOS = [
    "Diario de IA Educativa", "Bot de IA Educativa", "Comunidad de IA Educativa", "Vibe Coding Educativo",
    "Repositorio de recursos", "Juan José de Haro", "El profe de la bata", "La Rioja", "La Vanguardia",
    "El País", "Las Palmas", "Castilla y León", "Castilla-La Mancha", "Ceuta y Melilla", "Los Ángeles",
    "Agencia Española de Protección de Datos", "Los Angeles", "Los Ángeles", "Ministerio de Educación", "Polvo eres",
]
ETIQUETA = re.compile(r"<[^>]+>")
# Lo que no se mira: código, lo marcado como castellano, cursivas y citas (títulos y palabras citadas), las
# fuentes de cada pieza y los textos para republicar
FUERA = re.compile(
    r"<(script|style|template|svg|code|pre)\b.*?</\1>"
    r"|<(em|i|cite|q)\b[^>]*>.*?</\2>"
    r"|<section class=\"comprobado\".*?</section>"
    r"|<(\w+)\b[^>]*\blang=\"es\"[^>]*>.*?</\3>"
    r"|<(\w+)\b[^>]*\bhreflang=\"es\"[^>]*>.*?</\4>",
    re.S)
COMILLAS = re.compile(r"«[^»]{0,400}»|“[^”]{0,400}”|\"[^\"]{0,200}\"")
ENLACE = re.compile(r"<a\b[^>]*>.*?</a>", re.S)   # el texto de un enlace suele ser un título ajeno
BLOQUE = re.compile(r"<(p|li|h[1-6]|dd|dt|figcaption|caption|td|th|button|summary|label)\b[^>]*>(.*?)</\1>", re.S)
ATRIBUTO = re.compile(r"\b(?:aria-label|alt|title|placeholder)=\"([^\"]{12,})\"")
# Con el guion y el apóstrofo dentro: «ordenar-los» o «l'han» son una palabra, no un «los» suelto
PALABRA = re.compile(r"[\w'’·-]+")


def castellano(texto, idioma, sin_enlaces=None):
    """Las palabras solo castellanas del texto, si son bastantes para darlo por castellano. `sin_enlaces` es
    el mismo texto sin lo que va dentro de un enlace: ahí basta una sola palabra de las fuertes."""
    def limpia(s):
        for n in PROPIOS:
            s = s.replace(n, " ")
        crudas = [p for p in PALABRA.findall(COMILLAS.sub(" ", s)) if p.isalpha()]
        # «y» entre nombres con mayúscula («Valores y prioridades», el rótulo de una web ajena) no cuenta
        return [p.lower() for i, p in enumerate(crudas) if not (p == "y" and i and crudas[i - 1][:1].isupper())]
    if "://" in texto and " " not in texto.strip():
        return []   # una dirección
    palabras = limpia(texto)
    if len(palabras) < 3:
        return []
    # Una sola palabra fuerte basta en un texto corto (un rótulo, un dato de una ficha); en un párrafo
    # largo puede ser el nombre de algo ajeno, y ahí se pide más
    if len(palabras) <= 20:
        fuertes = {p for p in limpia(texto if sin_enlaces is None else sin_enlaces) if p in FUERTES[idioma]}
        if fuertes:
            return sorted(fuertes)
    marcas = [p for p in palabras if p in SOLO_ES[idioma]]
    distintas = set(marcas)
    # Un texto corto (un rótulo), con dos marcas distintas; uno largo, con tres y una de cada doce palabras
    if len(palabras) <= 10:
        return sorted(distintas) if len(distintas) >= 2 else []
    return sorted(distintas) if len(distintas) >= 3 and len(marcas) * 12 >= len(palabras) else []


def textos(pagina):
    t = FUERA.sub(" ", pagina)
    plano = lambda s: re.sub(r"\s+", " ", html.unescape(ETIQUETA.sub(" ", s))).strip()
    for m in ATRIBUTO.finditer(t):
        yield html.unescape(m.group(1)), None
    for m in BLOQUE.finditer(t):
        yield plano(m.group(2)), plano(ENLACE.sub(" ", m.group(2)))


def paginas(idioma, dia):
    base = SITIO / idioma
    for f in sorted(base.rglob("*.html")):
        rel = f.relative_to(base)
        if rel.parts[0] in ("pagefind", "n") or rel.name in ("insertar.html",):
            continue
        # Con --dia: la carpeta de ese día y las páginas que no son de ningún día
        if dia and re.fullmatch(r"\d{4}-\d\d-\d\d", rel.parts[0]) and rel.parts[0] != dia:
            continue
        if dia and rel.parts[0] in ("semana", "mes", "breves", "vineta") and len(rel.parts) > 2:
            continue
        yield f, rel


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dia", help="solo las páginas de ese día (AAAA-MM-DD) y las fijas")
    ap.add_argument("--idiomas", default="ca,gl,eu,en")
    ap.add_argument("--sitio", help="otra carpeta con el sitio generado (por defecto, sitio/)")
    a = ap.parse_args()
    global SITIO
    if a.sitio:
        SITIO = pathlib.Path(a.sitio)
    vistos, n = set(), 0
    for idioma in a.idiomas.split(","):
        if not (SITIO / idioma).is_dir():
            continue
        for f, rel in paginas(idioma, a.dia):
            for t, sin_enlaces in textos(f.read_text(encoding="utf-8", errors="replace")):
                marcas = castellano(t, idioma, sin_enlaces)
                # Lo que se repite en todas las páginas (cabecera, pie), una sola vez por idioma
                if marcas and (idioma, t) not in vistos:
                    vistos.add((idioma, t))
                    n += 1
                    print(f"{idioma}\t{rel}\t{t[:160]}{'…' if len(t) > 160 else ''}\t[{', '.join(marcas)}]")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
