# La imagen del boletín semanal (Claude Code, Python, git) más lo que el diario necesita para
# publicar: el cliente SSH, para subir con sus claves de despliegue, y rsync. Y, para revisar
# los dibujos en su página (ADR 0005), Playwright con el Chromium sin pantalla, la versión
# más ligera (solo el «headless shell», unos 250 MB). Y Pagefind, para el índice del buscador (ADR 0007), y numpy, para la música de los vídeos (ADR 0016), e internetarchive, para subirlos a Internet Archive (ADR 0037), y segno, para los QR de la edición en papel (ADR 0054), y Pillow, para aligerar la imagen de cada pieza al compartir (ADR 0010).
# Se reconstruye después del boletín en el actualizador semanal del vigía, así que coge la
# misma versión de Claude Code.
FROM boletin-semanal:local
USER root
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN apt-get update && apt-get install -y --no-install-recommends openssh-client rsync python3-pip \
    && pip3 install --no-cache-dir --break-system-packages playwright==1.61.0 'pagefind[bin]==1.6.0' numpy==2.2.6 internetarchive==5.11.1 segno==1.6.6 pillow==12.3.0 snowballstemmer==3.0.1 \
    && python3 -m playwright install --with-deps --only-shell chromium \
    && chmod -R a+rX /ms-playwright \
    && rm -rf /var/lib/apt/lists/* /root/.cache
USER 1000:10
