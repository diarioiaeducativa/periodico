# 99. La ficha del documento dice siempre dónde está

Fecha: 2026-11-22 · Estado: aceptado

## Contexto

Los artículos de la Biblioteca llevan una ficha, «El documento», con el título, la autoría, el año, el idioma y la
licencia. Solo enlazaba el documento si el redactor había encontrado su fuente oficial («Leer el documento en su
fuente oficial»), y el encargo le pedía dejar `documento.url` vacío si no la encontraba o si su web no dejaba leerla.
De las once fichas publicadas hasta el 22-11-2026, cuatro no decían dónde estaba el documento. Juanjo lo vio en la del
«Manual urgente sobre IA en el aula»: «aqui no debería constar el enlace a la biblioteca y el original? debería
aparecer siempre cómo localizar el documento».

## Decisión

- **La ficha termina siempre con una línea para localizarlo** (`articulo()` en `generar.py`): «Leer el documento:»
  y, separados por «·», el original («en su fuente oficial», con `documento.url`) o, si no lo hay, la descarga que da
  la ficha de la biblioteca («en Google Drive», con `documento.descarga`; el nombre del sitio lo pone `sitio_web()`),
  y el mensaje de la Biblioteca digital de ChatGPT-IA-edu (`mensaje`). Como sale del generador, vale también para lo
  ya publicado.
- **El DOI o la dirección oficial que trae la ficha van en `documento.url` aunque su web no deje leerla** con
  WebFetch: leerla y enlazarla son cosas distintas. La guía de la UNESCO del 13-11-2026 tenía el DOI en su ficha y el
  diario no lo enlazaba porque UNESDOC no deja leer de forma automática.
- **`documento.descarga`, nuevo**: solo cuando no hay fuente oficial y la ficha da una descarga que funciona. La
  traducción lo conserva como `documento.url`, y `revisar-enlaces.py` lo comprueba con los demás enlaces.

## Evidencia y validación

- Las cuatro fichas sin original: dos guías catalanas sin descarga en su ficha (la de orientaciones de la
  Generalitat se retiró de su web), que ahora enlazan al menos la Biblioteca digital; la guía de la UNESCO, que pasa a
  enlazar su DOI (10.58338/JXYO3928, que redirige a UNESDOC); y el manual del CESDi, del que no hay página oficial:
  la descarga de su ficha, un Google Drive («MANUAL IA_CESDi_EIDAES_VF.pdf»), funciona, y la que da una revista
  argentina ya no existe.
- La ficha se ha mirado en la vista previa en las cinco lenguas, en escritorio y en móvil.

## Riesgos

- Una descarga de Google Drive puede desaparecer: `revisar-enlaces.py` la comprueba los miércoles como el resto.
- No se ha podido confirmar quién comparte el Google Drive del manual; su nombre apunta a sus autoras.
