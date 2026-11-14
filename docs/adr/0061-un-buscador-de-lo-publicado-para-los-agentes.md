# 61. Un buscador de lo publicado para los agentes

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
  (`difflib`, 0,8) y lo dice. Ordena por BM25. Tiene un modo `parecidas`: con un texto (el titular y la
  entradilla que se piensan escribir), toma sus 30 palabras más distintivas y devuelve las piezas que más
  las comparten. Cada resultado trae la clave para enlazar, la fecha de publicación y los trozos con las
  palabras marcadas.
- **Los agentes lo usan como herramienta propia, no como orden**: `scripts/buscar-mcp.py` es un servidor
  MCP mínimo (sin dependencias) que ofrece `buscar`, y cada agente que escribe o revisa (redacción,
  Biblioteca, Repositorio, reportaje, «Hace un año» y comentario de la semana) lo carga con
  `--mcp-config scripts/buscar-mcp.json` y el permiso `mcp__diario__buscar`. `Bash` sigue prohibido.
- **`encargos/enlaces.md`** pide usarlo antes de presentar a una persona, herramienta, proyecto o sitio (con
  su nombre), y antes de escribir sobre un tema (con `parecidas`); el repaso de la redacción lo comprueba.

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
- Solo busca en castellano: las otras ediciones son traducciones de las mismas piezas.

## Evidencia

- `python3 scripts/buscar.py vilela` encuentra el breve de Liga de Valores, los dictados de EDUmind, MiClase y
  Atlas en xogo; `edumind`, también el Reloj EDUmind; `vilella` avisa y busca «vilela».
- `--parecidas` con «El INTEF presenta la actualización de su guía sobre inteligencia artificial en
  educación» pone primero `pieza:2026-11-13/intef-guias-ia-simo`.

## Validación

- En el contenedor del NAS, con los datos publicados, un agente (`claude -p`, Haiku 5.5, `acceptEdits`, la
  herramienta y `Bash` prohibido) usó `buscar` con una errata y en modo `parecidas` con los resultados de
  arriba, y no pudo ejecutar `touch` (no tiene `Bash`). El protocolo MCP del servidor se probó además a mano
  (`initialize`, `tools/list`, `tools/call`).
- Falta verlo en la redacción real de esta noche: que los agentes lo usen y que los números dejen de omitir
  piezas relacionadas. Hipótesis pendiente de validación.
