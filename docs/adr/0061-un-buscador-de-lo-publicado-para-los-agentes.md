# 61. Buscadores de lo publicado y de los mensajes para los agentes

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

Los agentes que escriben y revisan el diario sabían qué se había publicado por `publicado.txt`, que solo
lleva la clave y el titular de cada pieza. El 14-11-2026, la pieza «Atlas en xogo» del número del 13 decía que
el diario había contado a su autor, Luis Vilela Acuña, «en un breve», el único sitio donde su nombre estaba
en un titular; ya había contado otras tres aplicaciones suyas, con el nombre solo en el cuerpo. Juanjo lo vio
con el buscador de la web y pidió «un buscador de calidad que los agentes puedan consultar incluso con
variantes de palabras si esto es posible, es la unica forma de que el diario no empiece a repetir articulos
o dejarse referencias como lo de hoy».

El buscador de la web (Pagefind, ADR 0007) funciona en el navegador y los agentes no pueden usarlo. Buscar
texto en los archivos (Grep) distingue tildes y mayúsculas, no encuentra variantes y obliga a repasar cinco
carpetas. Los agentes no tienen consola: `Bash` está prohibido porque leen mensajes de Telegram que escribe
cualquiera.

## Decisión

- **`scripts/buscar.py`**: busca en el texto entero de todo lo publicado en castellano (piezas y breves de
  cada número, Biblioteca, Repositorio, reportajes y «Hace un año»). Construye en cada consulta un índice en
  memoria con SQLite FTS5, sin tildes ni mayúsculas, sobre las raíces de las palabras (algoritmo de Snowball
  para el castellano, `snowballstemmer` 3.0.1, licencia BSD, en el `Dockerfile`; sin él, una aproximación
  que quita las terminaciones comunes). Si una palabra no sale, prueba con las parecidas del vocabulario
  (`difflib`, 0,85) y lo dice. Ordena por BM25. Tiene un modo `parecidas`: con un texto (el titular y la
  entradilla que se piensan escribir), toma sus 30 palabras más distintivas y devuelve las piezas que más
  las comparten. Cada resultado trae la clave para enlazar, la fecha de publicación y los trozos con las
  palabras marcadas.
- **`scripts/buscar_mensajes.py`**, el mismo motor sobre todo el historial de los tres grupos (unos 50.000
  mensajes), con lo que el bot describe de cada imagen y la vista previa de cada enlace. Filtra por grupo y
  fechas, ordena por pertinencia o por fecha y enseña el contexto de un mensaje (los que lo rodean en su
  tema, el que responde y sus respuestas). Como son muchos, el índice se guarda en `cache/mensajes.sqlite`
  (32 MB, fuera de git): `noche.sh` lo rehace entero cada noche antes de la redacción (unos dos minutos) y
  cada consulta añade antes los mensajes nuevos. Juanjo lo pidió el mismo día («si, hazlo»), tras saber que
  los agentes solo veían los mensajes del día, o de la semana en el reportaje.
- **Los agentes lo usan como herramienta propia, no como orden**: `scripts/buscar-mcp.py` es un servidor
  MCP mínimo (sin dependencias) que ofrece `buscar`, `buscar_mensajes` y `contexto_mensaje`, y cada agente que escribe o revisa (redacción,
  Biblioteca, Repositorio, reportaje, «Hace un año» y comentario de la semana) lo carga con
  `--mcp-config scripts/buscar-mcp.json` y el permiso `mcp__diario` (las tres). `Bash` sigue prohibido.
- **`encargos/enlaces.md`** pide usarlo antes de presentar a una persona, herramienta, proyecto o sitio (con
  su nombre), antes de escribir sobre un tema (con `parecidas`) y, con los mensajes, para saber si algo ya se
  habló y citar el mensaje original; el reportaje reúne con él lo dicho a lo largo de los meses. El repaso de
  la redacción lo comprueba.

## Alternativas descartadas

- **Permitir a los agentes solo la orden `python3 scripts/buscar.py`** (`Bash(python3 scripts/buscar.py:*)`
  sin prohibir `Bash`): probado en el contenedor, una orden encadenada (`… ; touch /tmp/pr/intruso`) se
  ejecutó, porque el modo `acceptEdits` deja pasar sin preguntar las órdenes de archivos. Con mensajes de
  Telegram como entrada, no.
- **Un archivo con todo el texto para buscar con Grep**: sin variantes ni parecidos, y distingue tildes.
- **Búsqueda por significado (embeddings)**: necesita un modelo y su mantenimiento; las raíces, los
  parecidos y BM25 cubren nombres y temas sin coste.

## Consecuencias

- Cada consulta tarda menos de un segundo con las piezas de hoy; el índice se rehace cada vez, así que
  siempre está al día y no hay nada que mantener. Si un día pasa de unos segundos, se guarda el índice.
- Solo busca en castellano: las otras ediciones son traducciones de las mismas piezas. Los mensajes, en el
  idioma en que se escribieron; las raíces son las del castellano, así que en catalán y gallego encuentra
  la palabra exacta y algunas variantes.
- Si el índice de los mensajes no se puede rehacer, queda el de la noche anterior más lo nuevo.

## Evidencia

- `python3 scripts/buscar.py vilela` encuentra el breve de Liga de Valores, los dictados de EDUmind, MiClase y
  Atlas en xogo; `edumind`, también el Reloj EDUmind; `vilella` avisa y busca «vilela».
- Mensajes: 49.722 indexados en 121 s; una consulta, unos 0,6 s. `vilela` encuentra la presentación de
  Atlas en xogo y la de Liga de Valores; `--contexto vce:14877` da el hilo de la conversación sobre la
  consola y la aplicación, con el mensaje al que responde.
- `--parecidas` con «El INTEF presenta la actualización de su guía sobre inteligencia artificial en
  educación» pone primero `pieza:2026-11-13/intef-guias-ia-simo`.

## Validación

- En el contenedor del NAS, con los datos publicados, un agente (`claude -p`, Haiku 5.5, `acceptEdits`, la
  herramienta y `Bash` prohibido) usó `buscar` con una errata y en modo `parecidas` con los resultados de
  arriba, y no pudo ejecutar `touch` (no tiene `Bash`). El protocolo MCP del servidor se probó además a mano
  (`initialize`, `tools/list`, `tools/call`).
- Falta verlo en la redacción real de esta noche: que los agentes lo usen y que los números dejen de omitir
  piezas relacionadas. Hipótesis pendiente de validación.
