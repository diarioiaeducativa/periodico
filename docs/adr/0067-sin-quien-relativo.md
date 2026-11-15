# 67. Sin el relativo «quien» con el sentido de «la persona que»

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

El reportaje del 14-11-2026 llevaba siete «quien» o «quienes» relativos («Quien hizo la prueba afirmó…», «separar a
quien crea de quien revisa»), y «Hace un año», uno más. Juanjo lo señaló antes de que saliera: «no quiero que se use
quien o quienes en este sentido». Es una norma de su estilo desde el 09-11-2026, pero no estaba en los encargos del
diario, así que los agentes no la conocían.

## Decisión

- **En los encargos** (redacción, y con ella «Hace un año» y el comentario de la semana; reportaje, biblioteca,
  repositorio, avisos y vídeo): sin el relativo «quien» o «quienes»; en su lugar, «la persona que», un colectivo o
  un giro con el asunto delante. El interrogativo («¿quién?») sí, y las citas literales no se tocan.
- **Una comprobación sin IA** (`scripts/revisar-quien.py`), en `noche.sh` tras la de autoría (ADR 0066) y antes de
  traducir la edición. En castellano el relativo no lleva tilde y el interrogativo sí, así que basta con buscar la
  palabra sin tilde, fuera de las citas. Si encuentra algo, un corrector (`encargos/pasos/29-quien.md`, Sonnet) la
  reescribe en castellano y en las traducciones que calquen el giro («qui», «quen»). Lo que quede, se anota en el
  registro.
- Las traducciones parten del castellano: sin «quien» en el original, no aparecen «qui» ni «quen» con ese sentido.

## Alternativas descartadas

- **Sustituirlo de forma automática**: cada frase pide su giro («las personas que», un colectivo, otra
  construcción), y la concordancia cambia.
- **Corregir lo ya publicado**: en lo publicado hasta el 15-11-2026 hay 62 frases así. Es una cuestión de estilo, no
  un error, y corregirlas exigiría una nota de corrección en cada pieza (ADR 0055); se aplica desde ahora.

## Validación

- En el número del 14-11-2026 encontró el «quien» de la entradilla de «Hace un año», que se había escapado a la
  revisión a mano; ya corregidos los del reportaje, no encontró ninguno más.
- `--todo` sobre lo publicado: 62 frases, ninguna con el interrogativo ni dentro de una cita.
