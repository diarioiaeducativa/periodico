# 93. Las instrucciones de los agentes, como páginas del diario

Fecha: 2026-11-20 · Estado: aceptado

## Contexto

El libro de estilo (`encargos/estilo.md`, ADR 0078) dice que cada tarea tiene además su guía en `encargos/`, pero
la página `estilo.html` solo enlazaba la carpeta en GitHub: el lector no veía qué guías hay ni de qué agente es cada
una. La lista ya existía en «El diario por dentro» (ADR 0082), con cada agente enlazado a su guía en GitHub, rodeada
de los menús de GitHub, que no son del diario.

Juanjo pidió que las guías estén en la misma página que el libro de estilo, «para que todo lo que sea igual esté en
el mismo sitio», sin tocar lo que leen los agentes («no quiero interferir con el trabajo de los agentes»), y que cada
guía se lea como una página del diario, solo en castellano «de momento, cuando esté más estable lo traduciremos».

## Decisión

- **La lista de guías se añade al generar la página del libro de estilo**, tras el párrafo que las nombra, y no se
  escribe en `encargos/estilo.md`: los agentes leen ese archivo entero en cada tarea y no ganan nada con ella. Es la
  misma lista de «El diario por dentro» (`guias_html()`, con `GUIAS_AGENTES` y los nombres de `equipo`), así que
  está en las cinco lenguas sin traducir nada nuevo y no hay dos listas que mantener.
- **Cada guía es una página** (`guia-<nombre>.html`, `GUIAS_PAGINAS` en `generar.py`), con la maqueta de las normas
  (ADR 0081): todas las guías de `encargos/` salvo el libro de estilo y el del traductor, que ya lo eran, y los
  encargos de paso de los agentes sin guía propia (revisor, revisor de dibujos, juez de humor, cronista, verificador,
  juez de la columna, jefe de reportajes, juez de reportajes y comentarista), con el título «Instrucciones del…».
  Se leen del `.md` cada vez que se genera la web, así que siguen solas a cada cambio de una guía.
- Cada página dice qué es («Las instrucciones con las que trabaja este agente, tal como las lee»), que lo que va
  entre llaves lo pone el programa, si lo hay, y enlaza al original en el repositorio, con su historial.
- **Solo en castellano**: unas 15.000 palabras que cambian casi a diario (la guía de redacción, 15 veces en un mes);
  traducirlas a cuatro lenguas en cada cambio gastaría mucho. Las otras lenguas enlazan a la página castellana, como
  ya decía su lista («en castellano»). Cuando cambien menos, se traducirán como las normas (ADR 0085).
- El convertidor de las normas aprende lo que usan las guías: los ejemplos de formato (los modelos de JSON), a lo
  ancho y pasando de línea en el móvil, y las listas dentro de listas. Un nombre entre acentos graves solo se enlaza
  al repositorio si es una ruta (lleva barra o punto): `multimedia` o `columnas` son palabras que coincidían con una
  carpeta, y se enlazaban por error.
- De paso, la frase de la lista en catalán y en gallego decía «a el repositori» y «en o repositorio»: ahora «al
  repositori» y «no repositorio».

## Consecuencias

- Todo lo que dice cómo escriben los agentes está en un mismo sitio: el libro de estilo y, desde él, cada guía.
- Los agentes leen lo mismo que antes.
- Una guía que use algo que el convertidor no conoce (un tercer nivel de lista, una tabla con barras dentro de una
  celda) se vería mal: al cambiar la forma de una guía, hay que mirarla en la web.
- Las páginas de las guías no entran en el buscador del diario ni en el mapa del sitio, como las normas.

## Validación

Las 21 páginas, el libro de estilo en castellano, catalán, gallego, euskera e inglés y «El diario por dentro»
generados y pasados por `scripts/revisar-maqueta.js` en Chromium, Firefox y WebKit, en escritorio, tableta y móvil,
sin avisos (20-11-2026). Cada página tiene todas las palabras de su original. En el móvil, dos guías desbordaban por
nombres largos entre acentos graves: ahora se parten.
