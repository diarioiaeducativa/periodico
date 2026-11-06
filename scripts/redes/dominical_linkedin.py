#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El dominical en LinkedIn (ADR 0027): el vídeo con su texto, publicado al momento. Corre en el
contenedor del boletín con su .venv, y reutiliza su navegador y su publicador de vídeos
(scripts/7-linkedin.py, que ya lo hace cada lunes): no duplica, porque antes busca el texto en lo
publicado.

    dominical_linkedin.py TEXTO.txt VIDEO.mp4 [--comprobar]
"""
import importlib.util
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path("/proyecto")   # el repositorio del boletín
spec = importlib.util.spec_from_file_location("li", BASE / "scripts" / "7-linkedin.py")
li = importlib.util.module_from_spec(spec)
spec.loader.exec_module(li)
from playwright.sync_api import sync_playwright  # noqa: E402

texto = Path(sys.argv[1]).read_text().strip()
video = sys.argv[2]
comprobar = "--comprobar" in sys.argv

entorno = subprocess.run([str(BASE / "scripts" / "navegador-linkedin.sh"), "preparar"],
                         capture_output=True, text=True, env={**os.environ, "FORZAR_VIRTUAL": "1"})
if entorno.returncode != 0:
    sys.exit(f"no hay navegador para LinkedIn:\n{entorno.stderr[-500:]}")
datos = dict(linea.split("=", 1) for linea in entorno.stdout.splitlines() if "=" in linea and not linea[0].isdigit())
li.log(f"navegador listo ({datos.get('MODO', '?')})")
with sync_playwright() as p:
    nav = p.chromium.connect_over_cdp(f"http://127.0.0.1:{os.environ.get('PUERTO_CDP', '9222')}")
    ctx, quien = nav.contexts[0], datos.get("MODO") == "cookies"
    page = li.pestana(ctx, quien)
    try:
        r = li.publicar(page, {"linkedin_text": texto, "files": {"video": video}}, "publicar",
                        datetime.now(li.MADRID), comprobar, lambda: li.pestana(ctx, quien))
    except Exception as error:  # noqa: BLE001
        li.volcar(page, Path(os.environ.get("HOME", "/tmp")) / ".local/state/diario-dominical/linkedin-error")
        sys.exit(f"ERROR: {type(error).__name__}: {str(error)[:300]}")
    li.log(r)
    sys.exit(1 if "NO aparece" in r else 0)
