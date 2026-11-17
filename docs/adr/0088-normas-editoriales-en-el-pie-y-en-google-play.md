# 88. «Normas editoriales» en el pie y en la declaración de Google Play

Fecha: 2026-11-17 · Estado: aceptado

## Contexto

La declaración de apps de noticias de Google Play (Contenido de la aplicación → Aplicaciones de noticias y
revistas → Credenciales) pregunta si el medio tiene directrices editoriales publicadas y pide su dirección. Llevaba
`redaccion.html`. El 17-11-2026 Google aprobó la versión 1.0.2 «con problemas» por «Violation of Incorrect News and
Magazines Declaration: Does not link to editorial guidelines», con una captura de «La redacción»: desde el ADR 0082
es la versión breve para lectores (organigrama, cómo se hace cada número) y no se reconoce como unas normas.

Las normas ya existen como página propia desde el ADR 0081: `normas.html` («Cómo se hace el Diario de IA
Educativa»), que reúne las normas del diario, quién las aplica y cómo se comprueban, y enlaza el libro de estilo y
el del traductor; traducida a las otras lenguas por el ADR 0085.

## Decisión

- La declaración de Google Play lleva `https://diarioiaeducativa.github.io/normas.html` como directrices editoriales.
- El pie de todas las páginas, en la columna «El diario», enlaza a esa página tras «La redacción» con el nombre que
  usa la política: «Normas editoriales» (ca «Normes editorials», gl «Normas editoriais», eu «Arau editorialak», en
  «Editorial guidelines»). La dirección es la de su lengua si está traducida (`doc_href`) y, si no, la castellana.
- `normas.html` no se renombra ni se quita del pie: es la dirección de la declaración, como `contacto.html`.

## Alternativas descartadas

- Apelar: la declaración era mejorable y el revisor solo mira lo que enlaza.
- Enlazar el libro de estilo (`estilo.html`): trata de cómo se escribe, no de la exactitud, las fuentes, las
  correcciones y quién responde, que es lo que piden unas normas editoriales.
- Cambiar el título del documento: es el que leen los agentes y rehacer sus traducciones no hace falta; el nombre
  de la política va en el enlace del pie.

## Consecuencias

- El revisor, desde la app, encuentra las normas a un toque desde cualquier pantalla y con el nombre de la política.
- Un enlace más en el pie de todas las páginas.

## Evidencia

Correo de Google Play del 17-11-2026 (02:56 UTC), «Action Required: Your app is not compliant with Google Play
Policies (Diario de IA Educativa)», con la captura `POLICY_DECLARATION_NEWS_MAGS-9235.png`.

## Riesgos y limitaciones

Que el revisor siga sin reconocer «Cómo se hace…» como normas. Si vuelve a rechazarse, se le puede dar un título
con «normas editoriales» al documento.

## Validación

Web generada en una copia el 17-11-2026: el enlace sale en el pie de la portada, de un artículo en inglés
(`../../normas.html`) y de las páginas de cada lengua; mirado en Firefox y Chromium, escritorio y móvil, sin errores.
