# 94. La terminología del TERMCAT, al alcance de los agentes

Fecha: 2026-11-20 · Estado: aceptado

## Contexto

El libro del traductor (ADR 0079) decía que la web del TERMCAT no deja leer a los programas y que su terminología se
consulta por el Optimot. Es cierto para el Cercaterm: tiene una protección contra robots (Anubis) puesta a propósito,
que no se salta. Pero el propio TERMCAT, en su `robots.txt`, remite a otra vía: la [Terminologia
oberta](https://www.termcat.cat/ca/terminologia-oberta), sus diccionarios para descargarlos enteros en XML, con la
licencia Creative Commons de cada uno (reconocimiento, o reconocimiento sin obras derivadas), sin esa protección.

Al mirarlos apareció un error del libro: fijaba «xatbot» para *chatbot* como forma propia, a falta de término
normalizado, y lo hay: el Consell Supervisor del TERMCAT normalizó «bot de conversa». «Xatbot» no está en el TERMCAT
ni en el diccionario del IEC. Se pidió resolverlo: «hazlo así».

## Decisión

- `scripts/termcat.py descargar` baja cuatro diccionarios (unos 24 MB de XML, 17.500 fichas con término catalán) y
  hace un índice en `cache/termcat/`, fuera del repositorio: la Neoloteca (los términos normalizados por el Consell
  Supervisor), la terminología de la intel·ligència artificial, el diccionari d'educació y la terminologia dels
  productes informàtics. Lo lanza `noche.sh` cada noche con `--si-toca`, que solo descarga si el índice tiene más
  de 30 días (el TERMCAT los actualiza a menudo); si falla, queda el anterior.
- Los agentes lo consultan con la herramienta `buscar_termcat` del servidor `mcp__diario` (ADR 0061): por la
  palabra en inglés, castellano o catalán, con o sin tildes; devuelve el término catalán, si está normalizado, sus
  sinónimos, los equivalentes y la definición, con el diccionario de donde sale. Primero las fichas normalizadas, y
  una misma ficha que está en dos diccionarios, una vez. La tienen todos los que ya tenían el servidor y, además, los
  traductores que no lo tenían (`traducir-dia.sh`, `multimedia-traducir.sh`, `normas-traducir.sh`), el ilustrador
  (rótulos traducidos) y el guionista de «La semana en vídeo» (textos en catalán).
- El diario solo consulta los diccionarios: no publica nada de ellos, así que la licencia no pone condiciones.
- El libro del traductor lo dice, y *chatbot* pasa a «bot de conversa». Los tres artículos en catalán publicados con
  «xatbot» se dejan como están.
- La herramienta solo lee; no da a los agentes acceso a internet que no tuvieran ni a ningún programa.

## Consecuencias

- Los términos de la IA en catalán se comprueban contra la fuente normativa, no de memoria ni solo por el Optimot.
- Si el TERMCAT cambia la dirección de sus archivos, la descarga falla y lo dice el registro de la noche; el índice
  anterior sigue sirviendo.
- Lo mismo se podría hacer en otras lenguas con fuentes abiertas parecidas (Euskalterm, IATE); no se ha hecho.

## Validación

Descargado e indexado el 20-11-2026 (17.527 fichas). Comprobado por la herramienta: «prompt» da «indicació»,
«chatbot» da «bot de conversa», «large language model» da «model de llenguatge gran», «alucinación» da
«al·lucinació» y «deepfake» da «hipertrucatge», todos normalizados; una palabra que no está devuelve que no hay ficha y
remite al Optimot.
