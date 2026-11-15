# 67. Normas de estilo comprobadas cada noche: sin «quien» relativo y sin citas solo en inglés

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
- **Una comprobación sin IA** (`scripts/revisar-estilo.py`), en `noche.sh` tras la de autoría (ADR 0066) y antes de
  traducir la edición. En castellano el relativo no lleva tilde y el interrogativo sí, así que basta con buscar la
  palabra sin tilde, fuera de las citas. Si encuentra algo, un corrector (`encargos/pasos/29-estilo.md`, Sonnet) la
  reescribe en castellano y en las traducciones que calquen el giro («qui», «quen»). Lo que quede, se anota en el
  registro.
- Las traducciones parten del castellano: sin «quien» en el original, no aparecen «qui» ni «quen» con ese sentido.

- **Ninguna cita solo en inglés en una edición que no es inglesa** (añadido el 15-11-2026). El reportaje de ese día
  citaba en inglés a Turnitin y GPTZero en las cinco ediciones, sin traducir: «will need to apply your professional
  judgment». Juanjo: «en las versiones que no están en inglés o bien se da traducido o bien se pone la traducción al
  lado. No debe haber fragmentos solo en inglés en idioma no inglés». La cita original se queda y su traducción va al
  lado, entre paréntesis. La misma comprobación la busca en castellano, catalán, gallego y euskera: una cita entre
  comillas con al menos dos palabras de las más corrientes del inglés (y una de cada cinco) y sin traducción detrás.
  El título enlazado de una obra se deja en su idioma, como pide el perfil de Juanjo para lo oficial ajeno. El
  corrector añade la traducción en todas las versiones.

## Alternativas descartadas

- **Sustituirlo de forma automática**: cada frase pide su giro («las personas que», un colectivo, otra
  construcción), y la concordancia cambia.
- **Corregir lo ya publicado**: en lo publicado hasta el 15-11-2026 hay 62 frases así. Es una cuestión de estilo, no
  un error, y corregirlas exigiría una nota de corrección en cada pieza (ADR 0055); se aplica desde ahora.

## Validación

- Citas en inglés, `--todo` sobre lo publicado: las tres del reportaje del 15-11 y una de la Biblioteca del 03-11
  («This is not a moment for patches and duct tape»), en cuatro idiomas; las cinco se tradujeron ese día. Las
  primeras versiones de la regla daban por inglesas «On puc opinar?» (catalán), un nombre propio («Ask the Three
  Questions») y el título enlazado de un artículo; se quitaron pidiendo dos palabras corrientes y saltando los enlaces.

- En el número del 14-11-2026 encontró el «quien» de la entradilla de «Hace un año», que se había escapado a la
  revisión a mano; ya corregidos los del reportaje, no encontró ninguno más.
- `--todo` sobre lo publicado: 62 frases, ninguna con el interrogativo ni dentro de una cita.
