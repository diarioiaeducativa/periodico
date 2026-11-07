# 30. Comentarios con giscus, en las Discussions de GitHub

Fecha: 2026-11-07 · Estado: aceptado

## Contexto

Raül Torres propuso comentarios en cada artículo «para que la gente pudiera opinar» (07-11-2026). El
diario es un sitio estático en GitHub Pages: no hay servidor que reciba y guarde comentarios, y el NAS
no se abre al público (trabaja solo, sin que nadie se conecte a él).

## Decisión

- **giscus** (<https://giscus.app>), de código abierto, gratuito, sin anuncios ni rastreo. Los
  comentarios se guardan en las Discussions del repositorio del sitio
  (`diarioiaeducativa/diarioiaeducativa.github.io`), categoría «Comentarios», de tipo anuncio: solo
  giscus y los administradores abren hilos, y cualquiera responde. La app de giscus está instalada solo
  en ese repositorio, con permiso de leer metadatos y escribir en Discussions.
- **Solo GitHub**: para comentar hace falta una cuenta de GitHub. Juanjo descartó añadir un enlace a la
  conversación de Telegram para quien no la tenga. Un aviso encima del recuadro lo dice y enlaza el
  alta: «Para comentar hace falta una cuenta gratuita de GitHub. Los comentarios son públicos y se
  guardan en GitHub.»
- **Un hilo por pieza, el mismo en los cinco idiomas**: `mapping=specific` con la ruta de la pieza sin
  idioma (`AAAA-MM-DD/id`, `AAAA-MM-DD/breve-N`) y `strict=1` (giscus busca por el hash del término, sin
  coincidencias aproximadas). El hilo se crea con el primer comentario.
- **Dónde**: al pie de artículos, editoriales, reportajes y breves, tras «Más en…» y antes de «Volver a
  la portada», fuera del `<article>` y con `data-pagefind-ignore`. Carga diferida (`loading=lazy`), caja
  de escribir arriba, sin reacciones.
- **Idioma y tema**: giscus en el idioma de la edición; el gallego, en castellano, porque giscus no lo
  tiene. Tema `light` o `transparent_dark` según el del diario, y cambia al momento con el botón de tema
  (un `MutationObserver` sobre `data-theme` manda `setConfig` al iframe).
- **Aviso de cada comentario**, a Juanjo y a Raül Torres (lo pidió Juanjo, 07-11-2026), el mismo mensaje
  por el Bot de IA Educativa: pieza, autor, el texto entero (en varios mensajes si pasa de 3.000
  caracteres) y enlaces a la pieza y al comentario en
  GitHub. A nadie se le avisa de lo que escribe él (`jjdeharo`, `raultorres-ia`). Lo manda una acción de
  GitHub del repositorio del sitio (`.github/workflows/avisar-comentario.yml`, evento
  `discussion_comment`), con los secretos `BOT_IAEDUCATIVA_TOKEN`, `JUANJO_CHAT` y `RAUL_CHAT` de ese
  repositorio. La publicación diaria sincroniza el sitio sin tocar `.github/` (`--exclude .github` en
  `publicar-nas.sh`, `publicar.sh` y `vigilante.sh`), o la borraría.
- **Configuración**: `GISCUS` y `comentarios()` en `generar.py`; textos en `comentarios`,
  `comentarios_aviso` y `comentarios_cuenta` de cada idioma; estilo en `diario.css`.

## Alternativas descartadas

- **Widget de discusión de Telegram**: necesita un canal público por el que pasen los artículos, y el
  canal ya se descartó.
- **Respuestas de Bluesky**: la web solo las muestra; para comentar hay que ir a Bluesky.
- **Sistema propio en el hosting de bilateria.org**: otro servidor público que mantener y vigilar contra
  el spam.

## Consecuencias

- Moderación desde GitHub: ocultar, borrar o bloquear en la Discussion de cada pieza.
- Cada página pide `giscus.app` al llegar al recuadro: es la única petición a un tercero del diario.
- Si se renombra la categoría, hay que cambiar `GISCUS["category"]` (giscus la busca por nombre).

## Riesgos y limitaciones

- La cuenta de GitHub deja fuera a buena parte del profesorado: aceptado por Juanjo.
- giscus es un servicio de un tercero alojado en Vercel; si cae, el recuadro no carga y el resto de la
  página sigue igual.
- Sin gallego en giscus.

## Validación

Aviso: hilo de prueba con un comentario; la acción tardó unos 10 s desde el comentario hasta el
mensaje. El mensaje para Raül, probado desviado a Juanjo; el hilo de prueba, borrado.

Chromium, Firefox y WebKit, en el ordenador y en el móvil (Pixel 7 e iPhone 15), tema claro y oscuro:
sin errores de JavaScript ni desbordamiento; el único 404 es el de giscus preguntando por un hilo que aún
no existe. Cambio de tema en directo comprobado en Chrome. Revisado en pantalla por Juanjo antes de
publicar.
