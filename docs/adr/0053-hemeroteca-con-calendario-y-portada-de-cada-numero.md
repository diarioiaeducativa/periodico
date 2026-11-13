# 53. La hemeroteca, un calendario con la portada y los titulares de cada número

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

La hemeroteca era una lista por meses y semanas plegadas (ADR 0034), con la pieza que abrió cada número. Para
encontrar un día había que adivinar su semana y desplegarla, y la página crecía sin fin: en un año serían 365
números. Juanjo pidió (13-11-2026) que fuera más fácil de consultar y propuso un calendario; al ver las
hemerotecas de los diarios de referencia (La Vanguardia, ABC, The Guardian, The New York Times, la BBC), pidió
además la portada de cada número y que se viera, en un portátil, el calendario y el número sin bajar.

## Decisión

- **Un calendario por meses**, por la fecha de cabecera de cada número (la que recuerda quien lo leyó, un día
  después de la conversación que cuenta), con flechas y un desplegable de meses; el mes elegido queda en la
  dirección (`?mes=AAAA-MM`). Hoy, rodeado con el bolígrafo rojo de la cabecera. Los días sin número, en gris.
- **Elegir un día con un clic o un toque** (o la barra espaciadora): no lo abre ni cambia al pasar el ratón
  por encima (Juanjo: «si muevo el ratón el día cambia»). Sin JavaScript, cada día abre su número.
- **El número elegido, en su marco a la derecha** (en el móvil, debajo): su fecha y número, que enlazan al
  número, y todos sus titulares por secciones, sacados de `datos/AAAA-MM.json` (los de «Para tu web», ADR 0032),
  sin breves ni «Hace un año». A la izquierda, **la portada del número en miniatura**: la página del día de la
  cabecera a la viñeta, tal como se ve en un ordenador. Pulsada, se amplía en el visor del resto de imágenes
  del diario, a lo ancho (900 px) y bajando dentro de él, porque ajustada a la pantalla quedaba tan pequeña
  como la miniatura.
- **Sin huecos** (ADR 0041): si los titulares son pocos, la portada se recorta por abajo para acabar con ellos;
  si son muchos, siguen por debajo de ella. En pantalla ancha, el calendario acompaña al bajar (`sticky`), y
  `scripts/revisar-maqueta.js` no cuenta como hueco una columna fija así.
- **Una columna con el resumen de cada semana**: el número de la semana, enlazado a su página (ADR 0034). Es la
  semana que cuentan los números de esa fila (los de martes a domingo cuentan los días de lunes a sábado de esa
  semana; el del lunes es el último de la anterior), no la semana en que se publican.
- **Todo lo posible a la vista sin bajar**: en pantalla ancha, el título, el buscador y el calendario a la
  izquierda, y el número elegido a la derecha desde arriba. En un portátil de 1366 × 768 (unos 650 px útiles)
  se ve el calendario casi entero y un día normal completo.
- **Fuera de la hemeroteca**: la lista de semanas y la de los boletines anteriores, que ya dan el calendario y
  las páginas de cada semana (que enlazan su mes y los boletines), y la frase de presentación.
- **Las abreviaturas de los días, las normativas**: L M X J V S D (RAE), dl. dt. dc. dj. dv. ds. dg. (IEC),
  l. m. mc. x. v. s. d. (RAG), al. as. az. og. or. lr. ig. (Gobierno Vasco), Mon… Sun en inglés.
- **Icono propio**: `library-big`, de Lucide.
- **La portada en miniatura** (`scripts/portadas.py`, sin IA): `publicar-nas.sh` la captura con el Chromium de
  Playwright del sitio ya montado, a 900 px de ancho y en tema claro, en los cinco idiomas, y vuelve a montar el
  sitio para ponerla en el calendario. Se guarda en `portadas/<fecha>-<idioma>.jpg` con sus medidas en
  `portadas/medidas.json`, que viajan con el repositorio. La vista previa de las 5:00 no la tiene hasta la
  publicación.
- **En las páginas de un número anterior** (su portada y sus piezas), el menú empieza por «‹ Núm. 9 ›», que
  lleva a la portada de ese número, y «Hoy», a la de hoy, en lugar de «Portada», que no decía de qué día era
  (Juanjo: «quiero ir a la portada del día que estoy mirando… pero que también se pueda ir a la portada de
  hoy»).

## Alternativas descartadas

- **Una captura de la portada web entera**: ilegible en pequeño y con piezas de otros días. La captura llega
  hasta la viñeta, que es lo del número.
- **La imagen de vista previa del número (ADR 0010)** como portada: solo enseña la pieza que lo abre.
- **Los titulares bajo el calendario y la portada grande a la derecha** (sin huecos): obligaba a bajar para
  leer los titulares. Juanjo eligió verlo todo a la vez.
- **Un resumen de la semana en el recuadro del día**: mezclaba dos cosas; la semana ya tiene su página.

## Consecuencias

- Cada portada pesa unos 135 KB de media: unos 245 MB al año en los cinco idiomas, solo se descarga la del día
  que se mira.
- Un día con muchos titulares sigue pidiendo bajar un poco en un portátil.

## Validación

Chromium, Firefox y WebKit, en ordenador, tableta y móvil, en los cinco idiomas y en tema claro y oscuro;
`revisar-maqueta.js` y `revisar-anchos.js` sin avisos; los 16 días comprobados uno a uno, sin huecos en el
recuadro del número; el visor y el menú de los días anteriores, probados con clic, toque y teclado.
