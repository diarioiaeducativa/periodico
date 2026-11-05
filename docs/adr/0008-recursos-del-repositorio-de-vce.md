# 8. Los recursos del Repositorio de VCE, en Vibe coding: una cola para los días flojos y el sábado

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

El [Repositorio de recursos](https://vibe-coding-educativo.github.io/app_edu/) de Vibe Coding
Educativo (VCE) reúne las aplicaciones y recursos educativos que comparten los miembros de esa
comunidad. Juanjo preguntó si se podía hacer con ellos algo parecido a la Biblioteca (ADR 0006).

Hasta ahora el diario solo contaba un recurso si se hablaba de él en el grupo ese día. De los 16
que entraron del 27-10 al 03-11, 4 tuvieron pieza en la sección Vibe coding. Otros se
descartaron con motivos que el repositorio habría resuelto: que se habían publicado el día
anterior, que no se encontraban en fuentes públicas o que la página no dejaba ver su contenido.

**Ritmo de altas**, contado con las 476 respuestas del formulario (que guardan cada envío, también
lo borrado después de la hoja), porque la «Marca temporal» de la hoja no sirve para lo anterior
al bot: con el formulario, cambiar un recurso era reenviarlo y la limpieza nocturna dejaba solo
el envío más reciente.

| Periodo | Altas | Por semana |
|---|---|---|
| Arranque (junio y julio de 2025) | 171 | carga inicial |
| Curso 2025-26 (septiembre a junio) | 161 en 43 semanas | media de 3,7; lo normal, entre 2 y 5; 6 semanas sin ninguna y una con 14 |
| Verano de 2026 (julio a septiembre) | 12 | 1 |
| Del 1 al 24 de octubre de 2026 | 9 | 2-3 |
| Con el bot (27-10 al 03-11) | 16 en 8 días | pico de estreno, 3 de Juanjo |

En el curso hubo 31 autores; el que más, el 16 % (25 recursos). Juanjo señaló que algunas
personas dan de alta varios recursos de golpe y luego pasan semanas sin nada, y que hay días con
muy pocos mensajes en los grupos (el 03-11-2026, por ejemplo).

## Decisión

Juanjo aprobó la cola y su funcionamiento el 03-11-2026. Se pensó en una sección propia
(«Taller»), pero él propuso usar la sección Vibe coding, que ya presentaba aplicaciones, y se
hizo así: las secciones del diario van por temas.

- **Una cola.** Todo recurso que entra en el repositorio desde el 27-10-2026 (el día en que el
  bot empezó a dar las altas) entra en la cola. Sale de ella cuando el diario lo cuenta, en una
  pieza del redactor o en un artículo del repositorio, o cuando se descarta. Es una cola sin
  estado guardado: `scripts/repositorio.py` la calcula cada noche comparando la hoja con las
  direcciones que aparecen en `ediciones/` y `repositorio/`.
- **Días flojos.** Si el número tiene menos de 4 piezas (3 hasta el 04-11-2026), contando las de la Biblioteca, el
  documentalista escribe sobre las que falten, como mucho 2: de la más antigua a la más nueva y
  nunca dos de la misma persona el mismo día, por turnos de autor: va antes quien lleva más tiempo
  sin un recurso con artículo y, dentro, el más antiguo, para que nadie acapare el espacio. Es un artículo de 250 a 350 palabras con la
  captura del recurso, con el antetítulo «Nuevo en el repositorio».
- **El sábado.** El número del sábado (las conversaciones del viernes) recoge en una sola pieza
  todo lo que queda en la cola, agrupado por autor, con 80 a 120 palabras y una captura por
  recurso: «La semana del repositorio». Una tanda de varios recursos de una persona se queda en
  un bloque, y nada espera más de una semana.
- **El fondo.** Un día flojo con la cola vacía, el programa elige al azar (con la fecha como
  semilla) tres recursos anteriores al 27-10 que no tengan un aviso pendiente de la revisión del
  repositorio (ADR 0013 del bot), con licencia declarada, también por turnos de autor, y que no sean un GPT, un Gem o un
  proyecto de Claude. El documentalista elige uno: «Del fondo del repositorio». Así un día sin
  apenas mensajes también tiene número.
- **Captura en lugar de dibujo.** El programa abre cada recurso en el Chromium sin pantalla de la
  revisión de dibujos (ADR 0005), a 1280×800 y en tema claro, y guarda la captura (JPEG al 72 %,
  entre 40 y 80 KB) y el texto que se ve. Lo que no abre no pasa al agente; el sábado, lo que
  sigue sin abrir sale de la cola como descartado. El documentalista mira la captura y abre la
  web; el revisor vuelve a abrirla y quita lo que no se ve en el recurso. En el artículo, la
  captura se amplía al pulsarla, sobre la propia página y con la X arriba a la derecha. Las
  capturas que el revisor no usa se borran.
- **Agentes**: documentalista, revisor y traductor (Sonnet 5.5, pasos 16 a 18), sin ilustrador.
  Criterios en `encargos/repositorio.md`. Se nombra a la autora o el autor como crédito, también
  a Juanjo de Haro, igual que en el resto del diario (ADR 0018).
- **Datos**: la hoja publicada en CSV, la misma que lee la web del repositorio. El bot no guarda
  copia: la consulta por su API cada 15 minutos y la tiene en memoria. Los avisos de la revisión
  salen de `/bot-datos/avisos.json`.
- **En `noche.sh`**, después de la Biblioteca; nunca impide el número. Un día sin mensajes en
  ningún grupo, o en que la redacción decide no sacar número, también se intenta con la
  Biblioteca y el repositorio (`solo_anexos`).
- **El portavoz** menciona en el aviso de VCE los recursos del número.
- La descripción de Vibe coding enlaza el repositorio, y «La redacción» y su organigrama lo
  cuentan.

## Alternativas descartadas

- **Un artículo de 400-700 palabras por recurso, como en la Biblioteca**: una app pequeña no da
  para tanto sin rellenar, y unos 4 a la semana desplazarían a las noticias.
- **Una sección propia («Taller»)**: separaba lo hecho del cómo se hace, pero repartía las
  presentaciones de aplicaciones entre dos secciones. Juanjo prefirió Vibe coding.
- **Recuperar los documentos antiguos de la Biblioteca en el fondo**: solo los que entraron desde
  octubre de 2026 tienen el texto completo guardado, y sin él la Biblioteca tuvo que descartar dos
  de los 6 que intentó recuperar. De momento, solo el repositorio.
- **Leer la hoja por la API del bot**: exige su clave, y lo publicado en CSV basta.

## Consecuencias

- Unos 5 minutos por artículo y unos 10 el viernes por la noche, sin coste
  nuevo.
- Las capturas se guardan en `repositorio/capturas/` y se publican en `capturas/` del sitio:
  unos 5 a la semana, unos 15 MB al año.
- El primer sábado, el 07-11-2026, la cola trae lo que entró desde el 27-10 y no se ha contado:
  una pieza más larga que las siguientes.
- El umbral empezó en 3 piezas, sacado de los 6 números publicados (5 con 3 o más, uno con 1).
  El 04-11-2026 Juanjo lo subió a 4, tras un número 3 con solo tres artículos: le parecían pocos.
  Se avisó de que la cola se gastará antes y el sábado puede quedar poco para «La semana del
  repositorio». Hay que revisarlo con un mes de datos.

## Evidencia

- Ritmo de altas: respuestas del formulario «Añade tu aplicación al repositorio educativo»
  (Google Forms, descargadas el 03-11-2026) y CSV publicado de la hoja. Recuento por semana ISO;
  un envío cuenta como alta si su enlace (normalizado) o su título no habían salido antes; los de baja se cuentan aparte.
- `vce-app_edu/limpieza.gs`: ante un enlace o título repetido, conserva la fila más reciente.
- `bot-chatgpt-ia-edu/scripts/catalogo.py`, `enlace_catalogo`: la ficha de un recurso es
  `https://vibe-coding-educativo.github.io/app_edu/?ids=<enlace>`.
- Piezas por número: `ediciones/2026-10-28.json` a `2026-11-02.json`.

## Validación

Probado el 03-11-2026 en copias de la redacción, con la hoja real y la configuración de Claude sin
el perfil de Juanjo, en los tres modos: un día sin piezas (2 artículos de la cola: Rompecabezas
Jigsaw y Laboratori de formulació), la semana forzada con `REPOSITORIO_MODO=semana` (10 recursos
en una pieza y 2 descartados) y el fondo forzado. Cada paso de agente tarda alrededor de un minuto.
Sitio generado y revisado en Chromium, Firefox y WebKit, a 1280 y 360 píxeles, en tema claro y
oscuro y con pantalla táctil: sin errores de JavaScript, sin recursos que falten, sin
desbordamiento horizontal, y el visor se abre y se cierra en todos.

Lo que salió en las pruebas y se corrigió:

- La cola contaba «La teva veu», que el diario ya había contado el 01-11: la ficha usa el
  acortador ja.cat y la pieza enlazaba la dirección final. Ahora se compara también la dirección
  a la que lleva el enlace.
- El fondo eligió un recurso con aviso pendiente (ficha con ja.cat y aviso guardado con la
  dirección antigua). Ahora los avisos se comparan por enlace, por dirección final y por título.
- El fondo eligió un recurso de Juanjo y se le excluyó del fondo; el 04-11-2026 también de los
  días flojos. Juanjo lo corrigió ese día: «no quiero que me ignores, quiero ser tratado como
  cualquiera, evitando monopolizar los recursos un solo usuario». Desde entonces sus recursos
  entran como los de cualquiera, y la cola y el fondo van por turnos de autor.
- FoQo y FoQa no se podían capturar: una tipografía que no termina de cargar dejaba la captura
  esperando. Se espera a que la página esté construida, se dan 12 segundos a la carga completa y
  la captura no espera a las tipografías (`PW_TEST_SCREENSHOT_NO_FONTS_READY`).
- El documentalista descartó una aplicación porque WebFetch devolvía un error: WebFetch no ejecuta
  JavaScript. Los encargos dicen ahora que mandan la captura y el texto visible, que salen de un
  navegador de verdad.
- El agente guardaba la captura con su carpeta y la limpieza la tomaba por no usada: ahora se
  compara solo el nombre del archivo, aquí y en el generador.
- En la pieza de la semana, las capturas a todo el ancho hacían una página de casi 10.000 píxeles:
  ahora van al lado de su texto en pantallas anchas.
- El traductor tradujo «Vibe Coding Educativo», que es un nombre propio.
