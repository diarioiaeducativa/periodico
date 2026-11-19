# 92. La columna de opinión de los miércoles, escrita por un modelo de otra casa

Fecha: 2026-11-19 · Estado: aceptado

## Contexto

Todo lo que publica el diario es información: en «Debates» se exponen las posturas sin tomar partido. Juanjo
propuso (19-11-2026) un artículo de opinión semanal escrito por «un agente de alto nivel», GPT-6.2-Astra, sobre
un tema polémico de la semana. Se descartó una columna diaria: en los grupos no hay un debate de verdad cada día,
y un mismo columnista a diario repite sus manías de estilo. Pidió además que siempre haya una de reserva, como con el
reportaje: «al ser de opinión no es tan importante la fecha… en el momento de publicar se elige uno y el otro se
descarta». La primera salió en el número del 18-11-2026, sin anunciarla; ese mismo día pidió contarla en «La
redacción» «y donde haga falta».

El resto del diario lo escriben modelos de Claude. Que la opinión la firme un modelo de otra casa la separa a la
vista de la información y evita que todo salga de la misma voz.

## Decisión

- **Una columna los miércoles**, en la sección «Opinión» (`opinion`, en `SECCIONES_FUERA`: con su página y sin
  entrada en el menú, con enlace en el pie), sin dibujo. El día que sale, en la portada y en la página de
  su número, un anuncio en un recuadro a la derecha de la apertura, en un tercio del ancho, con el titular, la firma,
  la entradilla y «Leer la columna», y la apertura a su lado con el titular a lo ancho y, debajo, la entradilla y el
  dibujo (`apertura_portada()`); por debajo de 64 rem, el anuncio pasa debajo de la apertura. Es para llamar la
  atención ese día (Juanjo, 19-11-2026: «es para llamar la atención ese dia y romper la monotonia del diario, el resto
  de dias no cambia»). Los días siguientes sigue en la portada, como el reportaje (`opinion_reciente()`), en una franja
  a todo el ancho después de la viñeta, con el reportaje, lo más reciente primero (`tras_la_vineta()`). El titular de
  la columna va en redonda, como los demás: la cursiva, que puso el agente para distinguirla, se confundía con un
  antetítulo y no estaba en la página de la columna (Juanjo, 19-11-2026: «quitalo»). En la página de la sección, las columnas van una debajo de otra en recuadros
  de texto: en la rejilla de las secciones, sin dibujo, ocupaban la casilla de un dibujo con el icono. La columna lleva al final una nota fija:
  el diario comprueba sus datos y la opinión es del modelo.
- **La firma, como la de un columnista** (Juanjo, 19-11-2026: «la firma de opinión, ¿se podría humanizar algo?»): encima
  del titular, como en La Vanguardia y elDiario.es (que se consultaron ese día), un dibujo en un círculo, como la foto
  del columnista, y al lado «Astra» y debajo «Columnista de IA · GPT-6.2-Astra, de OpenAI», en cada lengua
  (`opinion_quien`). «Astra» sale del nombre del modelo, y la segunda línea dice que es una IA y su nombre exacto.
  El dibujo es una columna dórica con cara: la columnista hecha columna. Lo dibujó Fable, con tres propuestas; se
  descartaron una estrella (dibujada antes por Opus), por ser un lugar común de la IA («hay que huir de las frases
  hechas, en este caso de dibujos hechos»), y una columna jónica, porque sus volutas parecían cuernos. El columnista
  se busca por el campo `autor` en `COLUMNISTAS` (`generar.py`), con su nombre, su modelo, su casa y su dibujo; un
  autor que no esté allí firma «Por {autor}». Ni la firma ni la nota las escribe el columnista: las pone el
  generador, en cada lengua.
- **El columnista elige el tema**, se documenta y escribe (Juanjo, 19-11-2026, al ver que Claude buscaba el debate
  por él: «eso no debería hacerlo codex?»). Encargo: `encargos/columna.md`. Tesis clara, la postura contraria en su
  mejor versión, ideas y no personas, datos con su enlace, de 600 a 800 palabras.
- **Datos comprobados, opinión libre**: el verificador (Sonnet, `39-columna-verificacion`) contrasta cada dato y que
  no aparezca nadie de los grupos, sin tocar la tesis, los argumentos ni el tono. Un programa
  (`scripts/columna.py comprobar`) mira la medida, el titular, los enlaces y la forma.
- **Siempre una de reserva** (`reserva/columnas/`): si hay una cuando sale la nueva, el juez (Opus,
  `40-columna-eleccion`) elige la mejor y la otra se descarta; si la nueva no vale, sale la de reserva. La mañana
  siguiente, `reserva.sh` escribe otra si no queda ninguna (con los mensajes de la última semana y las piezas de
  las cuatro últimas, sobre un debate que no dependa de unos días). Así, cada semana Astra escribe dos columnas.
- **Dónde corre el columnista** (`nas/columnista.sh`, cada minuto en el crontab del NAS): `scripts/columna.sh`, en el
  contenedor del diario, deja en `columnas-trabajo/<clave>/` el encargo con todo el material dentro (`prompt.md`), la
  forma de la respuesta (`esquema.json`) y un `pedido`; el NAS lanza Codex en la caja del agente de noticias
  (`noticias-chatgpt-ia-edu`: sistema de archivos de solo lectura, sin privilegios, con su cuenta de ChatGPT), sin
  terminal (`--disable shell_tool`), con la búsqueda en la web y la respuesta comprobada contra el esquema. Deja
  `columna.json` y `hecho`, que es lo que espera `columna.sh` (50 minutos como mucho).
- **Horario**: la noche del martes al miércoles, en `noche.sh` (o con `COLUMNA=1`), y la de reserva a las 8:00 en
  `reserva.sh`. Ninguna coincide con el agente de noticias (de 4:39 a 5:10), que usa la misma cuenta de ChatGPT.
- **Traducción**: la de siempre (`traducir 38-columna-traduccion columna`, tipo `columna` en `idiomas.py`), que
  conserva el tono y la fuerza de cada argumento. Las comprobaciones nocturnas de estilo, autoría y erratas incluyen
  `columnas/`.
- Sin columna, el número sale igual; si no hay ni nueva ni de reserva, `incidencia`.

## Evidencia y validación

- La prueba del 19-11-2026 en el portátil: GPT-6.2-Astra con razonamiento alto eligió el tema (qué se califica
  cuando se permite la IA, de tres conversaciones de ChatGPT-IA-edu), con 687 palabras y dos fuentes, que se
  comprobaron (el informe de la Office for Students y Advance HE del 11-11-2026 y el modelo de declaración del
  INTEF). Gastó unos 111.000 tokens: 13 puntos de la sesión de 5 horas de Codex y 2 del límite semanal.
- Codex no puede ejecutar órdenes dentro de Docker con su caja (`workspace-write` pide bubblewrap y falla); con la
  caja desactivada, una instrucción colada en un mensaje de los grupos podría usar la terminal con la cuenta de
  ChatGPT a mano. Por eso va sin terminal y con el material en el encargo, como el agente de noticias (unos 380 kB
  con siete días de mensajes, sin los «Contexto: día anterior», que se repiten).
- El anuncio, el artículo y la sección se probaron en Chromium y Firefox, en escritorio, tableta y móvil, con tema claro y
  oscuro.

## Riesgos

- La consulta de Codex depende del acceso de la cuenta de ChatGPT del agente de noticias, que este renueva cada
  día al ejecutarse; si un día caduca, falla la columna nueva y sale la de reserva.
- «La redacción» la cuenta en los cinco idiomas: 18 agentes, el columnista y el juez de la columna en el equipo
  («Los miércoles»), su fila en el organigrama, el apartado de «El diario por dentro» y la excepción a «Son agentes
  de Claude». Las normas (`docs/como-se-hace.md`) la recogen en el número, en la tabla de normas, en «Quién hace cada
  cosa», en el horario, en la reserva y en las revisiones. Si cambia el modelo que la escribe, hay que cambiarlo en
  todos esos sitios.

## Alternativas descartadas

- **Una columna diaria**: no hay un debate de verdad cada día y la voz de un solo columnista cansa.
- **Que Claude elija el tema y prepare el debate para Astra**: lo que firma un agente lo hace entero ese agente.
- **Codex dentro del contenedor del diario, con terminal**: tendría a mano las claves de publicación del diario.
