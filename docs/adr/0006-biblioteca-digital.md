# 6. La sección Biblioteca: un artículo por documento de la Biblioteca digital

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

La Biblioteca digital es el tema de ChatGPT-IA-edu donde los miembros dejan guías, informes y
estudios sobre IA y educación, cada uno con su ficha (desde el 24-10-2026 los publica el bot de
los grupos, ADR 0002 del bot). Tiene 177 entradas desde febrero de 2025, unas 6 al mes en
septiembre y octubre de 2026 (archivos PDF y enlaces con ficha). Juanjo pidió una sección del
diario que dedique un artículo a cada documento nuevo.

## Decisión

- **Un artículo por documento**, de 400 a 700 palabras, en la sección «Biblioteca» (icono
  `library` de Lucide, color petróleo). No repite la ficha: explica quién lo publica y con qué
  autoridad, qué propone o encuentra, con citas breves y exactas, cómo encaja con otros
  documentos de la biblioteca y qué puede sacar de él un docente. Criterios en
  `encargos/biblioteca.md`.
- **Se lee el documento entero.** Desde el 03-11-2026 el bot guarda el texto completo de los PDF
  de la Biblioteca que entran desde octubre de 2026 (ADR 0026 del bot), y el documentalista lo
  lee entero; además busca la fuente oficial para enlazarla. Sin PDF en el grupo, lo lee en su
  fuente oficial. El artículo lleva una ficha del documento (título original, autoría, año,
  idioma, licencia y enlace oficial, si lo hay). El diario no copia el archivo: enlaza a la
  fuente oficial y al mensaje de la biblioteca, así que da igual su licencia.
- Un enlace a otro documento de la biblioteca lleva a su artículo del diario si lo tiene
  (`enlaces_biblioteca` en `generar.py`), con su título o una descripción como texto.
- **Se nombra a los autores del documento, no a quien lo comparte** (regla del diario: solo se
  nombra al autor de un recurso propio). Recomendado y aceptado por Juanjo.
- **Proceso** (`scripts/biblioteca.sh`): un programa (`scripts/biblioteca.py`) toma del bot los
  documentos que entraron ese día (mensaje raíz del tema con archivo, o con al menos 300
  caracteres de ficha propia); el documentalista (Sonnet 5.5) escribe; el revisor (Sonnet 5.5)
  lo contrasta con el documento; el ilustrador dibuja lo esencial (nunca la portada), con la
  revisión de dibujos (ADR 0005), y el traductor hace la versión catalana. `noche.sh` lo lanza
  tras la viñeta y nunca impide el número; un día sin más que un documento también es número.
- **El redactor diario deja esos documentos** para no duplicarlos.
- **Un documento que el diario ya ha contado no lleva artículo propio** (04-11-2026). El informe
  del comité del MIT salió como noticia en el número 2 (a partir de la nota del MIT compartida en
  el grupo) y, al entrar en la biblioteca, con artículo propio en el número 3: dos días seguidos con
  el mismo tema. El redactor ya consultaba lo publicado; el documentalista no. Ahora
  `biblioteca.py` le da las piezas de los últimos 30 días con sus fuentes (también las del mismo
  número), y si una trataba ese mismo documento (el documento, su nota de prensa o una noticia
  sobre él), lo apunta en `ya_contado` con la fecha y el id de esa pieza, sin escribir artículo.
  La comparación la hace el agente porque las direcciones no coinciden (la nota y el informe
  estaban en webs distintas); el revisor la comprueba abriendo las fuentes, y si no es el mismo
  documento lo pasa a `descartado`. `generar.py` pone esa pieza también en la sección Biblioteca,
  con el enlace al documento junto al de la conversación, y los enlaces de otros artículos a ese
  documento llevan a ella. Un número con solo documentos ya contados no anuncia nada de la
  Biblioteca. Recomendado y aceptado por Juanjo, que aceptó también dejar publicado el artículo del
  número 3, más completo que la noticia, en lugar de retirarlo.
- **En la portada, aparte**: los 3 artículos más recientes de la Biblioteca, en su bloque, sin restar
  sitio a las piezas del día, como cada sección desde el ADR 0041 (antes, de los últimos siete días con su
  propio tope, `BIBLIOTECA_PORTADA`). La página de la sección
  presenta la biblioteca y enlaza al tema del grupo.
- **Lo anterior**: no se recuperan las 177 entradas. Se intentaron las 6 de octubre de 2026
  (se le propusieron «unas 5, de septiembre y octubre»; contadas bien, eran 12 en dos meses, y
  se dejó en octubre), con el número del 3 de noviembre. Salieron 4: los informes para la UNESCO
  y del Foro Económico Mundial y las dos guías de la Generalitat de Catalunya. Las guías, en la
  primera prueba, se descartaron porque no aparecían en ninguna web oficial; con el texto
  completo del PDF salieron bien. Quedaron sin artículo un artículo de revista del que la web
  del editor solo da el título y un manual enlazado en Google Drive, sin fuente oficial.
- **La UNESCO** bloquea a propósito la lectura automática de su repositorio, y eso no se salta:
  el artículo de su informe se apoya en el resumen de la autora principal y lo dice en el texto.
- «La redacción» presenta al documentalista y la sección, y el organigrama lo añade.

## Consecuencias

- Unos 5-10 minutos más las noches con documento, sin coste nuevo.
- Un documento que no se encuentre en su fuente oficial puede quedarse sin artículo (pasa a
  `descartado`); con `scripts/biblioteca.sh FECHA id` se puede rehacer a mano.
