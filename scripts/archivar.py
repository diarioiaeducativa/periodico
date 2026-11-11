#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pide a Internet Archive que guarde el número del día en la Wayback Machine (ADR 0046).

    scripts/archivar.py [AAAA-MM-DD]   (fecha de las conversaciones; sin fecha, la de ayer)

Guarda la portada de cada idioma, la página del día y cada pieza y breve del número, en los cinco
idiomas. La lista sale del mapa del sitio publicado: mientras no lleve el día (GitHub Pages aún no ha
desplegado), espera, como mucho ESPERA_MAX segundos. Usa «Save Page Now» sin cuenta: una captura cada
vez y PAUSA segundos entre una y otra, para no pasar del ritmo que Internet Archive admite. Si contesta
que va demasiado deprisa (429), espera unos minutos y vuelve a probar; a la segunda seguida, lo deja
para no acabar bloqueado. Sin IA y sin datos de nadie: solo las direcciones públicas del diario.
Lo lanza publicar-nas.sh en segundo plano, con el sitio ya subido; el registro va a registro/archivo.log.
"""
import datetime
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://diarioiaeducativa.github.io/"
IDIOMAS = ["", "ca/", "gl/", "eu/", "en/"]
PAUSA = 20            # segundos entre capturas
ESPERA_MAX = 1800     # cuánto se espera a que el sitio publicado lleve el día
REINTENTO = 300       # espera tras un 429 o un fallo del servidor
AGENTE = "DiarioIAEducativa-archivo/1.0 (+https://diarioiaeducativa.github.io/)"


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    """La respuesta buena de Save Page Now es una redirección a la captura: basta con verla, sin seguirla."""
    def redirect_request(self, *a, **k):
        return None


ABRIR = urllib.request.build_opener(SinRedireccion)


def log(texto):
    print(f"{datetime.datetime.now():%F %T}  {texto}", flush=True)


def leer(url):
    pet = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pet, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def paginas(fecha):
    """Las direcciones del número en el mapa del sitio publicado, o None si aún no lo lleva."""
    try:
        mapa = leer(BASE + "sitemap.xml")
    except (urllib.error.URLError, OSError) as e:
        log(f"no se pudo leer el mapa del sitio: {e}")
        return None
    del_dia = sorted(set(u for u in re.findall(r"<loc>([^<]+)</loc>", mapa) if f"/{fecha}/" in u))
    if not del_dia:
        return None
    return [BASE + i for i in IDIOMAS] + del_dia


def guardar(url):
    """Devuelve 'ok' con la captura, 'lento' si Internet Archive pide frenar o 'fallo'."""
    pet = urllib.request.Request("https://web.archive.org/save/" + url, headers={"User-Agent": AGENTE})
    try:
        r = ABRIR.open(pet, timeout=180)
        codigo, destino = r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        codigo, destino = e.code, e.headers.get("Location", "")
    except (urllib.error.URLError, OSError) as e:
        log(f"fallo de red con {url}: {e}")
        return "fallo"
    if codigo in (301, 302) and "/web/" in destino:
        # La redirección lleva la última página que vio el navegador de Internet Archive: en la portada
        # de la raíz, la del idioma al que salta (el suyo es el inglés), aunque lo guardado es la raíz.
        captura = re.search(r"/web/(\d{14})", destino)
        log(f"guardada {url} (captura {captura.group(1) if captura else destino})")
        return "ok"
    if codigo == 429:
        return "lento"
    log(f"no guardada {url} (HTTP {codigo})")
    return "lento" if codigo >= 500 else "fallo"


def main():
    fecha = sys.argv[1] if len(sys.argv) > 1 else f"{datetime.date.today() - datetime.timedelta(days=1)}"
    inicio = time.monotonic()
    while (lista := paginas(fecha)) is None:
        if time.monotonic() - inicio > ESPERA_MAX:
            log(f"el sitio publicado no lleva el día {fecha}: no se archiva")
            return 1
        time.sleep(60)
    log(f"{len(lista)} páginas del {fecha} para Internet Archive")
    hechas = 0
    for url in lista:
        resultado = guardar(url)
        if resultado == "lento":
            log(f"Internet Archive pide frenar con {url}: nuevo intento en {REINTENTO // 60} minutos")
            time.sleep(REINTENTO)
            resultado = guardar(url)
            if resultado == "lento":
                log("sigue pidiendo frenar: se deja para no acabar bloqueado")
                break
        hechas += resultado == "ok"
        time.sleep(PAUSA)
    log(f"archivadas {hechas} de {len(lista)} páginas del {fecha}")
    return 0 if hechas == len(lista) else 1


if __name__ == "__main__":
    sys.exit(main())
