Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) el documento {ORIGEN}, una de las normas públicas del diario, que se publica como página para los lectores de esa lengua. Sigue el libro del traductor, `encargos/traduccion.md` (el apartado general y el de tu lengua), y el libro de estilo, `encargos/estilo.md`.

Escribe {DESTINO}, en Markdown:

1. La primera línea, tal cual: `<!-- origen: {HASH} -->`
2. Después, la traducción completa, con la misma estructura que el original: los mismos títulos (`#`, `##`) en el mismo orden, las mismas listas con los mismos puntos, las mismas tablas con las mismas filas y columnas, y las mismas negritas y cursivas.

No se traduce:

- lo que va entre acentos graves, exactamente igual, letra por letra, aunque parezca una palabra corriente: son nombres de archivos, de campos o de valores que usa el programa del diario (`` `encargos/` ``, `` `pieza:AAAA-MM-DD/id` ``, `` `fuentes` ``, `` `grafico` ``, `` `barras` ``, `` `columnas` ``, `` `lineas` ``, `` `[autor del diario: …]` ``, `` `[texto](url)` ``). No añadas ni quites ninguno: el original tiene los mismos que tiene que tener la traducción;
- la dirección de cada enlace (lo que va entre paréntesis tras `[texto]`); el texto del enlace sí, salvo que sea el título de una obra o de un documento;
- las menciones a los registros de decisiones, que se dejan con la forma «ADR 0026», con las mismas cifras;
- los nombres de productos, de empresas y de los grupos;
- los ejemplos que el original da en castellano para explicar una norma del castellano (el «quien» relativo, «pieza», «el diario cuenta»…): se dejan en castellano, entre comillas, porque la norma trata de cómo se escribe en castellano; lo que los explica sí se traduce.

El diario se llama en {LENGUA} «{TITULO}»: úsalo siempre así, en los títulos y en el texto, con la declinación que pida la frase. Los nombres del Bot de IA Educativa y de los grupos no se traducen.

Que la traducción se lea natural en {LENGUA}, como un texto escrito en esa lengua, y que lo entienda cualquier lector. Comprueba al acabar que no falta ningún apartado ni ningún punto. No toques nada fuera de {DESTINO}. Responde en una línea: el documento traducido y si algo te ha planteado dudas.
