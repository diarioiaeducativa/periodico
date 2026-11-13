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
  `discussion_comment`, y el programa en `.github/avisar-comentario.py`). El Markdown llega con formato:
  el programa pide a GitHub el comentario ya convertido a HTML (`bodyHTML`) y se queda con lo que Telegram
  muestra (negrita, cursiva, tachado, enlaces, código y citas; listas con viñeta, imágenes como enlace);
  sin ese HTML, o si Telegram lo rechaza, va el texto tal cual. Usa los secretos `BOT_IAEDUCATIVA_TOKEN`, `JUANJO_CHAT` y `RAUL_CHAT` de ese
  repositorio. La publicación diaria sincroniza el sitio sin tocar `.github/` (`--exclude .github` en
  `publicar-nas.sh`, `publicar.sh` y `vigilante.sh`), o la borraría.
- **Configuración**: `GISCUS` y `comentarios()` en `generar.py`; textos en `comentarios`,
  `comentarios_aviso` y `comentarios_cuenta` de cada idioma; estilo en `diario.css`.
- **Lo ya comentado se lee sin pulsar nada, de una copia en el propio sitio; giscus, solo para escribir**
  (13-11-2026). El primer arreglo de la privacidad (aprobado por Juanjo entre las medidas del examen del diario,
  ADR 0055) cargaba giscus solo al pulsar «Ver los comentarios»: así ningún lector se conectaba a un tercero
  (antes, cada pieza pedía `giscus.app/client.js` al abrirse y la página de privacidad decía «Quien no comenta
  no envía nada», que no era cierto), pero había que pulsar sin saber si había algo. Juanjo: «Eso no es
  práctico». Ahora:
  - Una acción del repositorio del sitio (`.github/workflows/copiar-comentarios.yml`, programa en
    `.github/copiar-comentarios.py`) lee de GitHub todos los hilos de la categoría y deja uno por pieza en
    `comentarios/AAAA-MM-DD/id.json`, con autor, enlace a su perfil, fecha (UTC), enlace al comentario y
    texto. Se lanza con cada comentario creado, editado o borrado, con cada hilo borrado o movido, a mano y
    cada hora (lo que se oculta al moderar no avisa: tarda como mucho una hora en desaparecer de la copia).
    Siempre lo rehace todo; si entretanto ha subido el número, vuelve a empezar sobre lo nuevo (cinco intentos).
    Las claves de despliegue del NAS no pueden subir flujos de GitHub Actions («refusing to allow an OAuth App to
    create or update workflow»): el `.yml` se guarda aquí, en `flujos-sitio/`, y se copia al sitio desde el portátil,
    con la cuenta de Juanjo. Cambiarlo es cambiarlo en los dos sitios.
  - El texto es el HTML que da GitHub, pasado por una lista cerrada de etiquetas de texto: sin atributos salvo
    el destino de los enlaces (solo `http`, `https` y `mailto`), sin scripts, estilos ni SVG, y sin imágenes,
    que quedan como enlace, para que leer no cargue nada de fuera. Sin avatares. Un comentario ocultado no
    sale; uno borrado, solo si tiene respuestas («Comentario borrado»), para no dejarlas sueltas.
  - La pieza pide su archivo al propio diario y, si lo hay, enseña los comentarios con sus respuestas encima
    del aviso y del botón, que ahora dice «Comentar» (en los cinco idiomas). Si aún no hay comentarios, la
    petición da 404 y solo queda el botón. Al pulsarlo se carga giscus como antes y la copia se oculta, porque
    giscus enseña el hilo entero. La fecha, con las mismas reglas que el resto del diario (`fecha_corta` y
    `fecha_con_anyo`, el año solo si no es el actual) y la hora local: el euskera no está en todos los navegadores.
  - La publicación no toca `comentarios/` (`--exclude /comentarios/` en `publicar-nas.sh`, `publicar-web.sh`,
    `publicar.sh` y `vigilante.sh`). Como la acción puede subir al sitio mientras sale el número, esos scripts
    actualizan con `pull --rebase` (la nota del modelo sigue a su commit con `notes.rewriteRef`) y, si la
    subida falla, se ponen encima y lo intentan otra vez.
  - La frase de privacidad lo dice en los cinco idiomas: los comentarios se leen de una copia del diario y
    giscus se carga solo al pulsar «Comentar».
  Validación: el programa, con una respuesta de GitHub guardada que incluía enlaces `javascript:`, atributos
  `onclick`, `<script>`, SVG, una imagen de `camo`, casillas, emoji, un comentario ocultado y otro borrado con y
  sin respuestas. La página, con dos comentarios y una respuesta simulados, en Chromium, Firefox y WebKit, en el
  ordenador (1280 px) y en el móvil (360 px), tema claro y oscuro, en castellano, catalán y euskera: sin errores
  de JavaScript ni desbordamiento y ninguna petición fuera del diario antes de pulsar; después, `giscus.app` y
  `github.githubassets.com`, y la copia oculta.

## Alternativas descartadas

- **Widget de discusión de Telegram**: necesita un canal público por el que pasen los artículos, y el
  canal ya se descartó.
- **Respuestas de Bluesky**: la web solo las muestra; para comentar hay que ir a Bluesky.
- **Sistema propio en el hosting de bilateria.org**: otro servidor público que mantener y vigilar contra
  el spam.

## Consecuencias

- Moderación desde GitHub: ocultar, borrar o bloquear en la Discussion de cada pieza.
- Leer los comentarios no conecta con nadie de fuera; `giscus.app` se pide solo al pulsar «Comentar», y es la
  única petición a un tercero del diario.
- Lo que se comenta tarda en salir en la copia lo que tardan la acción y GitHub Pages (un par de minutos); en
  giscus sale al momento.
- giscus da como mucho 100 comentarios por hilo y 100 respuestas por comentario en una consulta: la copia, igual.
- Si se renombra la categoría, hay que cambiar `GISCUS["category"]` (giscus la busca por nombre).

## Riesgos y limitaciones

- La cuenta de GitHub deja fuera a buena parte del profesorado: aceptado por Juanjo.
- giscus es un servicio de un tercero alojado en Vercel; si cae, el recuadro no carga y el resto de la
  página sigue igual.
- Sin gallego en giscus.

## Validación

Aviso: hilo de prueba con un comentario; la acción tardó unos 10 s desde el comentario hasta el
mensaje. El mensaje para Raül, probado desviado a Juanjo; el hilo de prueba, borrado. Formato: un comentario real
con títulos, negrita, cursiva, tachado, enlaces, cita, listas numeradas y anidadas, tareas, código,
tabla, imagen, mención y emoji, convertido y aceptado por Telegram; un comentario de 16.000 caracteres,
partido en cinco mensajes sin romper el formato; prueba completa desde GitHub en 10 s.

Chromium, Firefox y WebKit, en el ordenador y en el móvil (Pixel 7 e iPhone 15), tema claro y oscuro:
sin errores de JavaScript ni desbordamiento; el único 404 es el de giscus preguntando por un hilo que aún
no existe. Cambio de tema en directo comprobado en Chrome. Revisado en pantalla por Juanjo antes de
publicar.
