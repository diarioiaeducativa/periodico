# 59. Arreglos tras la revisión a ciegas: erratas de regla fija, fuentes en rejilla, tabla impresa y salto al contenido

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

La revisión a ciegas del 13-11-2026 (ADR 0058) dejó, además de la frase del pie, 21 hallazgos. Cruzados con
las decisiones ya tomadas, siete chocaban con alguna (la portada con tres piezas por sección, ADR 0041; el
menú del móvil que se desliza, ADR 0003; las columnas justificadas, ADR 0044; los dos recursos diarios del
repositorio, ADR 0008; el correo de contacto, ADR 0051; los comentarios con giscus, ADR 0030; el hueco de
`videos.html`, aceptado ese día) y uno esperaba a Google Play. De los demás, Juanjo encargó los once que se
le propusieron («hazlos»).

## Decisión

- **Erratas de regla fija, corregidas por un programa** (`scripts/corregir-erratas.py`, cada noche antes de
  generar y sin IA): en castellano, «y» ante una palabra que empieza por el sonido «i» y «o» ante una que
  empieza por «o»; en inglés, las comillas españolas, que pasan a “ ”. Cambia solo esos caracteres, sin
  reescribir el archivo. Había cinco «y» por «e» y 466 comillas en 35 archivos de la edición inglesa. Al
  traductor de inglés se le añade la norma (`scripts/idiomas.py`), y los textos fijos de la edición inglesa
  y la descripción de las viñetas para lectores de pantalla llevan también sus comillas.
- **Titulares de 90 caracteres como máximo**, contando los espacios, en los encargos del redactor, el
  documentalista, el reportero y el cronista, y en el repaso de las noticias. El programa solo avisa en el
  registro de los que se pasan: acortarlos es escribir. No se aplica a lo ya publicado.
- **Las fuentes de «Comprobado en», en rejilla** y no con columnas de CSS: con una o dos fuentes, Firefox
  dejaba vacía la primera columna y Safari partía el enlace entre dos. Se leen por filas.
- **La tabla de un reportaje, al imprimir, corta las columnas y ocupa todo el ancho**, con la cabecera
  repetida en cada página y sin partir filas. Dentro de una columna se montaba sobre el texto (en la pieza)
  o partía las palabras por sílabas (en la edición en papel). Sus estilos pasan de `.reportaje .tabla` a
  `.articulo .tabla`, para que valgan también en `papel.html`.
- **«Saltar al contenido»**, lo primero que encuentra el teclado en todas las páginas con cabecera: solo se
  ve al recibir el foco y lleva al `<main>`, al que `escribir()` pone `id="contenido"`. Lo copiado («Enlace
  copiado», el código de la tarjeta) se dice además en una región viva para lectores de pantalla.
- **La fecha de cada pieza queda fuera del buscador** (`data-pagefind-ignore`): el extracto de cada
  resultado empezaba por un resto de ella.
- **La imagen de cada pieza para los buscadores es su PNG de vista previa** (ADR 0010) cuando la pieza tiene
  dibujo: Google no admite un dibujo vectorial como imagen de una noticia. Las piezas con captura siguen con
  ella, y las que no tienen dibujo, sin imagen (ADR 0039).
- **Tres aclaraciones al lector**: «Cómo se hace cada número» dice por qué la dirección lleva la fecha del
  día anterior a la cabecera; la hemeroteca rotula como «Número de prueba» los días anteriores al
  lanzamiento, y la presentación del número 1 lleva una nota que remite a «La redacción».
- **La noticia del regulador inglés** (`2026-11-12/ofs-evaluacion-sin-ia`) cita el informe y no la cobertura
  de otro medio, con su nota (ADR 0055), en los cinco idiomas.

## Alternativas descartadas

- **Que la ficha del día de la hemeroteca no deje seguir los titulares por debajo de la portada**, como
  pedía la revisión: es lo que decidió el ADR 0053 para no dejar huecos. Se propuso por error y no se toca.
- **Corregir a mano las erratas y nada más**: volverían. La regla es fija y un programa la aplica sin riesgo.
- **Que el programa acorte los titulares**: cortar un titular es cambiar lo que dice.
- **`columns` solo con tres fuentes o más** (`:has()`): arreglaba el caso visto, pero no garantizaba otros
  repartos; la rejilla no parte nunca un elemento.
- **Quitar del buscador el titular y el antetítulo** para que el extracto no los repita: dejarían de
  encontrarse por sus palabras.

## Consecuencias

- El corrector toca también lo ya publicado cuando se lanza sin `--dia`; cada noche solo mira los archivos
  del día. Una regla nueva se añade allí y se prueba antes con `--mirar`.
- No corrige «y» ante diptongo («y hierro») ni ante palabras que se escriben con «i» pero no suenan así
  («y iPhone»): la segunda letra en mayúscula las delata. Tampoco «y IA».
- Las fuentes se leen ahora por filas, no por columnas.
- Una página nueva que use `cabecera()` lleva el salto al contenido sin hacer nada más.

## Evidencia

- Informe [Making AI work for students: reflections on institutional practice](https://www.officeforstudents.org.uk/publications/making-ai-work-for-students-reflections-on-institutional-practice/)
  (Office for Students y Advance HE, 11-11-2026, 48 páginas), leído el 13-11-2026: tareas sin supervisión
  que se completan con IA «to a high standard […] with limited engagement from students» (apartado 49);
  formatos seguros (57 y 69); recursos y alumnado con discapacidad (59); pruebas con la IA permitida o
  exigida (57 c); que es difícil establecer de forma concluyente si se usó IA (74), y que el resultado de
  un detector debe ser «at most, one piece of evidence» y la sospecha sin pruebas no debe bajar una nota
  (75). Dos frases de la pieza no estaban así en el informe y se ajustaron: «la revisión humana no
  distingue bien el texto de IA» y «no propone sacar la IA de la educación».
- La lista de fuentes, antes del cambio, en la página publicada: con una fuente, en Firefox empezaba en la
  segunda columna y en WebKit el enlace ocupaba dos; con dos, en Firefox la primera columna quedaba vacía.

## Riesgos y limitaciones

- La impresión se ha comprobado pasándola a PDF con Chromium; en Firefox y Safari, solo que la página carga
  sin errores, no el papel.
- Safari se ha probado con su motor (WebKit) en Linux, no en un Mac ni en un iPhone.
- Las notas y las frases nuevas en catalán, gallego, euskera e inglés son traducción de IA, sin revisión de
  un hablante.
- El tope de los titulares es una instrucción a agentes: reduce los largos, no los impide. Se verá en el
  registro de cada noche.

## Validación

- `generar.py` sin errores en los cinco idiomas, en una copia aparte, y Pagefind rehecho.
- `scripts/revisar-maqueta.js` sin avisos en 20 páginas (portada, número, piezas con una, dos, tres y 36
  fuentes, reportaje, «La redacción» y la hemeroteca en varios idiomas, buscador, contacto), en Chromium y
  Firefox, ordenador, tableta y móvil; `scripts/revisar-anchos.js` sin avisos en seis de ellas.
- En Chromium, Firefox y WebKit: las fuentes empiezan en la primera columna y ningún enlace se parte; el
  salto al contenido se ve al tabular y lleva el foco al `<main>`; el día 30 de octubre sale como «Número de
  prueba»; el extracto del buscador empieza por el antetítulo.
- El reportaje y la edición en papel del 7 de noviembre, en PDF: la tabla a todo el ancho, en dos páginas,
  con su cabecera en cada una.
- `scripts/corregir-erratas.py` lanzado dos veces seguidas: la segunda no cambia nada.
