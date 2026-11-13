# 56. Dos comprobaciones sin IA de lo publicado: castellano colado y enlaces caídos

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

El examen del diario del 13-11-2026 (ADR 0055) encontró dos clases de fallo que ningún agente mira, porque
no están en lo que cada uno escribe o traduce:

- **Castellano en las ediciones traducidas, fuera de lo que traduce el traductor**: el rótulo de la viñeta
  para lectores de pantalla («Viñeta 1… Tiza…»), la ficha de un documento de la Biblioteca («(guía) y…»),
  los resúmenes de los vídeos de la semana y un vídeo entero. Estaban en los cuatro idiomas y nadie lo había
  visto.
- **Enlaces que dejan de existir**: los dos de una pieza del 5-11 (un repositorio y su web) habían
  desaparecido una semana después, sin aviso en la pieza.

Juanjo aprobó el 13-11-2026 las dos comprobaciones entre las medidas del examen; la de enlaces, semanal.

## Decisión

Dos programas corrientes, sin IA, que no impiden nunca que el número salga:

- **`scripts/revisar-idiomas.py`**, cada noche, sobre el sitio recién generado (`noche.sh`, tras el último
  `generar.py`): lee las páginas del día y las fijas de `sitio/ca`, `gl`, `eu` y `en` y señala los textos que
  parecen castellano. Un texto corto (hasta 20 palabras: un rótulo, un dato de una ficha) basta que lleve
  una palabra que no existe en esa lengua («y», «con», «los», «las» en catalán); uno largo necesita tres
  distintas y una de cada doce. No cuenta lo marcado con `lang="es"`, los títulos en cursiva o entre
  comillas, las fuentes de «Comprobado en», el texto de los enlaces en la regla de una sola palabra, ni
  una lista de nombres propios. Lo que encuentra va a `registro/FECHA-idiomas.txt` y a un aviso a quien
  revisa el número, antes de que salga.
- **`scripts/revisar-enlaces.py --avisar`**, la noche del miércoles, en segundo plano y con el número ya
  listo: abre los enlaces externos de todo lo publicado (155 direcciones de 102 servidores el 13-11) y da
  por caído el que responde 404 o 410 o cuyo dominio ya no existe. Avisa cuando un enlace lleva dos pasadas
  seguidas caído, con la copia de la Wayback Machine si la hay. No toca las piezas: la nota de actualización
  (ADR 0055) va en los cinco idiomas. Guarda su estado en `estado/enlaces.json`. De una pieza que ya lleva
  la nota con la copia archivada no vuelve a avisar.
- **Los resúmenes de los vídeos de la semana se marcan como castellano** en las ediciones traducidas
  (`lang="es"` y una línea que lo dice), en vez de pasar por traducidos: los escribe el boletín en
  castellano, como el vídeo y el pódcast. Desde el ADR 0057 se traducen, y la marca queda solo para
  mientras falta la traducción.

## Alternativas descartadas

- **Que lo revise un agente**: es un trabajo de reglas fijas, y un agente más cada noche gasta y puede
  fallar; el programa tarda un segundo.
- **Un detector de idioma estadístico** (una biblioteca): habría que instalarla en el contenedor, y en
  textos de tres o cuatro palabras, que es donde están estos fallos, acierta poco.
- **Dar por caído un 403 o un error del servidor**: muchas webs oficiales rechazan la lectura automática
  (UNESCO, OpenAI); eso no se salta ni se cuenta como caída.
- **Comprobar los enlaces cada día**: en dos semanas cayeron 2 de 155. Una vez por semana basta y molesta
  menos a los servidores.
- **Traducir cada lunes los resúmenes de los vídeos**: llegan con el boletín, fuera de la redacción
  nocturna; hacerlo pide un paso nuevo con un agente los lunes por la mañana. Quedó como posibilidad y se
  hizo el mismo día (ADR 0057).

## Consecuencias

- Una palabra castellana legítima fuera de comillas y de cursiva (el nombre de una sección de una web
  ajena) puede dar un aviso falso. El programa prefiere callar: en una frase larga no avisa por una sola.
- La comprobación de idiomas no ve los errores de traducción, solo el castellano sin traducir.
- La de enlaces hace una petición cada 3 segundos a un mismo servidor y se identifica como revisor de
  enlaces del diario, con la dirección de «La redacción».

## Evidencia

- Sobre la copia del sitio del 12-11-2026, con los fallos sin arreglar, `revisar-idiomas.py` señala los
  tres resúmenes de los vídeos y el título y la descripción del vídeo «Así encaja todo» en gallego, euskera
  e inglés (22 líneas). Sobre el sitio del 13-11, antes de corregir la ficha del documento del regulador
  inglés, la señalaba en los cuatro idiomas; después, ninguna línea.
- Los dos enlaces de Tongjiang Lab respondían el 13-11-2026 con 404 y sin respuesta del dominio, y los dos
  tenían copia en la Wayback Machine.

## Riesgos y limitaciones

- Las listas de palabras de `revisar-idiomas.py` están hechas a mano y afinadas contra 16 números: un
  falso aviso repetido se corrige añadiendo el nombre a `PROPIOS` o quitando la palabra de la lista.
- No se ha visto todavía una pasada nocturna en el NAS de ninguno de los dos; la primera será la del
  14-11-2026 (idiomas) y la del miércoles 18-11-2026 (enlaces).

## Validación

- `revisar-idiomas.py` sin argumentos y con `--dia 2026-11-12` sobre el sitio generado el 13-11: sin
  hallazgos y salida 0. `bash -n scripts/noche.sh`, correcto.
- `revisar-enlaces.py` ejecutado entero en local el 13-11-2026.
