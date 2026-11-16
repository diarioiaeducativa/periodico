# 84. Gráficos con datos, dibujados por el programa

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Algunos artículos y reportajes manejan varias cifras comparables de un mismo estudio o encuesta, que se entienden
mejor en un gráfico. Hasta ahora la guía de las ilustraciones permitía que el ilustrador dibujara «un pequeño
gráfico con lo esencial» a mano, en el SVG, sin ninguna comprobación de que las barras o los puntos respetaran los
valores. En las primeras semanas, 4 de unos 100 artículos tenían tres o más porcentajes comparables (los dos
reportajes, la noticia de Scribe v3 y la de Fable 5.2).

## Decisión

- Un artículo (`grafico`) o un apartado del reportaje (`apartados[].grafico`) puede llevar los datos de un gráfico:
  tipo (`barras`, horizontales; `columnas`; `lineas`), título, unidad, etiquetas, una o varias series con sus
  valores, la fuente y una nota.
- `generar.py` (`grafico()`) lo dibuja en SVG con los colores del diario, que cambian solos en el tema oscuro, y un
  ancho que mantiene las letras legibles en el móvil: las barras empiezan en cero y llevan una guía de fondo hasta el
  máximo (el 100 % en los porcentajes), cada valor escrito, la leyenda si hay varias series y, al pie, la fuente
  enlazada y la nota. Para quien no ve el gráfico, su descripción lleva todos los datos. Las cifras siguen la forma de
  cada lengua (coma decimal; «25%» en inglés, «% 25» en euskera).
- Las normas, en el libro de estilo («Gráficos»): solo con tres o más cifras comparables de una misma fuente, el
  título dice qué se mide, la fuente siempre, y la nota con la muestra y si los datos son de la propia empresa. El
  redactor y el reportero proponen el gráfico; el revisor y el verificador comprueban cada valor y, si uno no se
  confirma, lo quitan entero. El ilustrador ya no dibuja gráficos con datos.
- Las traducciones traducen el título, las etiquetas, las series y la nota; `scripts/idiomas.py` comprueba que el
  tipo, la unidad y los valores son los mismos que en castellano. El corrector de estilo no puede tocarlo (ADR 0083).

## Consecuencias

- Los datos de un gráfico se comprueban como cualquier cifra y se dibujan siempre igual y a escala.
- Gráficos de vez en cuando, no en cada número.

## Validación

Dibujados en local, en Chromium y Firefox, en escritorio y móvil, en tema claro y oscuro (16-11-2026): barras con los
tres porcentajes del estudio de Stanford del reportaje del 14-11-2026, y columnas con dos series y líneas con datos de
prueba.
