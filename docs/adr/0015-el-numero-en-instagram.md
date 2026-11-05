# 15. El número de cada día en Instagram, como carrusel

Fecha: 2026-11-05 · Estado: aceptado

## Contexto

El 05-11-2026 se creó la cuenta de Instagram @comunidad.iaeducativa («Comunidad de IA Educativa»)
para dar a conocer los tres grupos, sus boletines y el diario. Juanjo, ese mismo día: «ahora cada
dia quiero publicar el diario también por instagram, se puede automatizar?».

## Decisión

Recomendado y aceptado por Juanjo el 05-11-2026 («sí, hazlo así»):

- **Un carrusel diario de imágenes, no un reel.** Un vídeo cada día con la misma plantilla cansa
  y pide música distinta cada vez; los reels quedan para piezas especiales, hechos aparte.
- **Las imágenes las hace un programa, sin IA** (`scripts/instagram.py imagenes`, Chromium de
  Playwright, como `og-numero.py`): 1080 × 1350 (4:5), con la tipografía y los colores del
  diario. La portada con los titulares, una imagen por pieza (sección, antetítulo, titular,
  dibujo o captura y entradilla; como mucho cinco), las tres viñetas de Tiza y Algoritmo, una
  por imagen para que el remate llegue al deslizar, y un cierre que remite al enlace del perfil.
  Cada texto se reduce hasta un mínimo legible si no cabe; si aun así no cabe, no hay carrusel
  ese día y se avisa.
- **La descripción la escribe el agente de los avisos** en el mismo paso (campo `instagram` de
  `avisos/<fecha>.json`, `encargos/avisos.md`); el programa le añade la cabecera con el número,
  la remisión al enlace del perfil, el aviso de que está redactado y dibujado con IA y las
  etiquetas. Si el texto falta o no cumple (longitud, enlaces, etiquetas), van los titulares.
- **Publica la API oficial de Instagram** con una app de Meta propia («Diario de IA Educativa»,
  id 1816197736382213), sin publicar (modo de desarrollo), con la configuración de «inicio de
  sesión unificado», la única disponible para apps nuevas (la de «inicio de sesión de Instagram»
  ya no se ofrece). Esa configuración exige un portfolio comercial: se creó «Comunidad de IA
  Educativa» (sin verificar; la verificación solo hace falta para enviar la app a revisión o leer
  datos de terceros). La cuenta @comunidad.iaeducativa es evaluadora de Instagram de la app y
  pasó a ser profesional de tipo creador, que la API exige. Las llamadas van a
  `graph.facebook.com` con el id de la cuenta (17841419195377541).
- **Las imágenes se sirven desde la rama `instagram` del repositorio del sitio**, que se rehace
  cada día con un solo commit y push forzado: la API descarga cada imagen de una dirección
  pública, y así no se acumulan unos 1,2 MB diarios en la historia del sitio ni ocupan el NAS ni
  IONOS. En el repositorio de la redacción no se guardan (`.gitignore`): se pueden rehacer.
- **Cuándo**: `publicar-nas.sh` hace las imágenes antes de generar el sitio; `reloj.sh` publica a
  partir de las 7:05, después del número, y solo si la página del día ya está en línea. Un solo
  intento automático, sin reintentar después de `media_publish`, para no publicar dos veces;
  `estado/<fecha>.instagram` guarda el enlace.
- **El permiso** es un token de usuario del sistema, que no caduca, generado en el panel de la
  app; vive en `~/.config/diario-instagram.json` (en el NAS, `home/.config`), con permisos 600 y
  una copia en el portátil. Cada día a las 12:00 `reloj.sh` comprueba que sigue valiendo y es de
  la cuenta correcta; si falla, avisa a Juanjo. `renovar` queda para el caso de cambiar a un token
  de Instagram de 60 días. Si se pierde o se revoca, se genera otro en Casos de uso → API de
  Instagram → Generar tokens de acceso.

## Alternativas descartadas

- **Reel diario**: ver arriba.
- **Publicar a mano o con un servicio de terceros** (Buffer, Later): trabajo diario o un coste y
  un intermediario más; la API oficial es gratuita para la propia cuenta.
- **Imágenes en el sitio** (`sitio/instagram/`): engordarían la historia del repositorio del sitio
  cada día.
- **Inicio de sesión con Facebook**: Meta lo da por antiguo y exige una página de Facebook
  conectada a la cuenta.
- **Inicio de sesión de Instagram** (`graph.instagram.com`, sin portfolio): era lo previsto,
  pero Meta ya no lo ofrece en las apps nuevas («no está disponible en las apps más recientes»).

## Consecuencias

- Unos segundos más al publicar y una llamada a la API por imagen.
- Lo que sale en Instagram no se puede retocar después salvo la descripción, a mano desde la app.
- Si Meta cambia la API o caduca el permiso, el carrusel deja de salir y Juanjo recibe un aviso;
  el diario y los avisos de los grupos no dependen de ello.

## Evidencia

- Publicación de contenidos, documentación de Meta (tipos, carruseles de hasta 20 elementos,
  imágenes en JPEG desde una dirección pública, 100 publicaciones por API cada 24 horas):
  https://developers.facebook.com/docs/instagram-platform/content-publishing
- Renovación del token de larga duración (`refresh_access_token`, `ig_refresh_token`):
  https://developers.facebook.com/docs/instagram-platform/reference/refresh_access_token
- `raw.githubusercontent.com` sirve los JPEG de la rama con `Content-Type: image/jpeg`
  (comprobado el 05-11-2026 con la rama `instagram`).

## Riesgos y limitaciones

- Meta puede exigir la revisión de la app o la verificación del portfolio para mantener el
  acceso; está en modo de desarrollo, que basta para una cuenta con rol en la app.
- `alt_text` en los elementos del carrusel: si la API dejara de aceptarlo, se publica sin él.

## Validación

- Imágenes de los números 3 y 4 generadas en local el 05-11-2026 y revisadas a la vista.
- Rama `instagram` subida y servida como `image/jpeg` el 05-11-2026.
- Permiso comprobado el 05-11-2026: responde la cuenta @comunidad.iaeducativa y `content_publishing_limit` da 0 de 100.
- Primera publicación real el 05-11-2026, a mano desde el contenedor del NAS: número 4, 9 imágenes, https://www.instagram.com/p/DfWkHexltyc/ (revisada a la vista).
