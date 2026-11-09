# 40. «Hace un año»: lo que se hablaba el mismo día del año anterior, contado desde hoy

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

En un año la inteligencia artificial generativa cambia tanto que lo que se discutía en los grupos hace
doce meses dice mucho de dónde estamos: modelos que eran novedad y ya se han retirado, límites que se daban
por fijos, problemas que se han resuelto solos. Juanjo pidió (09-11-2026) una pieza diaria, «un espacio para
la nostalgia», con algo que se estuviera hablando exactamente un año antes en alguno de los grupos y la
diferencia con hoy.

El archivo del Bot de IA Educativa tiene los mensajes de ChatGPT-IA-edu desde abril de 2023, de Vibe Coding
Educativo desde mayo de 2025 y de EduMedia-IAG desde julio de 2025. Entre el 09-11-2025 y el 08-11-2026, la
mediana fue de 38 mensajes diarios entre los tres grupos; solo 2 días no tuvieron ninguno y 26, menos de 10.

## Decisión

- **Una pieza cada día**, en la sección «Hace un año» (`hace-un-ano`), al final del número. «Hace un año» se
  cuenta desde el día en que sale el número, el que ve el lector: el número del 10 de noviembre de 2026 mira
  los mensajes del 10 de noviembre de 2025 (el 29 de febrero, el 28).
- **Un solo tema, el que mejor muestre el contraste**: un modelo o una herramienta que ha cambiado o ya no
  existe, un problema resuelto, un límite superado, una predicción confirmada o desmentida, un debate zanjado.
  **Sin repetir** tema ni producto de los últimos 30 días: la entrada lleva lo ya contado, porque en días
  seguidos se suele hablar de lo mismo (en la prueba, dos piezas seguidas salieron sobre Veo y Gemini Omni).
  Si el día justo no da para nada, el anterior o el siguiente, diciendo la fecha real; si tampoco, el número
  sale sin la pieza: mejor nada que una nostalgia forzada.
- **Lo de hoy, comprobado**: el redactor (Opus) comprueba en internet cómo está hoy cada cosa que afirma, y
  el verificador (Sonnet, que no ha escrito nada) lo contrasta con los mensajes de entonces y con las fuentes;
  lo que no confirma se quita. Después, la traducción a los otros cuatro idiomas.
- **Medida**: de 150 a 250 palabras con la entradilla. Un programa (`scripts/hace_un_ano.py comprobar`)
  revisa la medida, los campos y que la fecha original sea de hace un año (±1 día).
- **Sin entrada en el menú**: la sección tiene su página (`hace-un-ano.html`), pero el menú lleva las
  secciones de noticias y en los portátiles solo le quedaban unos 170 px libres. Se llega desde la pieza de
  cada número y desde el pie, junto a la hemeroteca y la semana, con lo que mira atrás. Si se lee mucho, se
  sube al menú cambiando una línea (`SECCIONES_FUERA` en `generar.py`).
- **Un dibujo, siempre un díptico «Entonces / Ahora»**: la fecha de entonces a la izquierda y «Hoy» a la
  derecha, con lo concreto de la pieza en cada mitad. Lo hace el ilustrador con la revisión de dibujos de
  siempre (ADR 0005); si no pasa, la pieza sale sin dibujo.
- **En la portada, con lo de hoy, junto a los breves**: una fila de dos recuadros del mismo alto, los breves en
  dos tercios y «Hace un año» en el otro, en sepia, con el díptico en miniatura junto al titular. Sola a todo el
  ancho se veía demasiado grande para una pieza de memoria, y en la fila de «Más del día» quedaba casi siempre
  sola, con dos tercios vacíos. Sin breves, sale en una franja ancha, con el díptico a un lado y el texto al
  otro; en la página de un número, al final, con los breves del número. Los de días anteriores no salen en la
  portada. Color sepia, de foto
  antigua, e icono de reloj con la flecha hacia atrás (Lucide `rotate-ccw-clock`).
- No va en la página de la semana (ADR 0034), que es de lo que se habló esa semana, ni en el comentario de la
  semana (ADR 0038).

## Alternativas descartadas

- **En el menú superior**: cabía justo en pantallas de 1280 px o más, pero agotaba el último hueco para una
  sección de noticias.
- **Varios temas por día**: dos piezas de memoria cada día pesarían más que la actualidad.
- **Al final de la portada**: quedaba a más de tres pantallas, detrás de las secciones con lo de días
  anteriores. **En la fila de «Más del día»**: dejaba un hueco casi a diario.
- **Dos columnas, con una cita del mensaje de entonces al lado**: obligaría a citar palabras de personas
  concretas, cuando el diario cuenta temas y no personas.
- **Sin comprobar lo de hoy**: es justo lo que más se presta al error («ya no existe», «ya se resolvió»).

## Consecuencias

- Tres agentes más cada noche (redactor, verificador e ilustrador, unos 15 minutos en la prueba), sin coste
  nuevo, más la revisión del dibujo y la traducción.
- El organigrama de «La redacción» (un dibujo) aún no lleva ni al cronista ni al comentarista de la semana;
  el texto del equipo, sí.

## Validación

Tres piezas de prueba, de los números del 7, el 8 y el 9 de noviembre de 2026 (mensajes del 7, el 8 y el 9 de
noviembre de 2025), generadas en una copia aparte y publicadas en sus números: el verificador corrigió entre
dos y seis detalles en cada una, y en la del 9 quitó un contraste falso (una separación de datos que ya
existía hace un año). Los tres dípticos pasaron la revisión de dibujos a la primera. Portada, número, pieza y
página de la sección probados con `probar-web` en Chromium y Firefox, escritorio y móvil, claro y oscuro.
Contraste del sepia: 6,8:1 sobre el papel claro y 10:1 en oscuro.
