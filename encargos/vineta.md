# Encargo: la viñeta diaria de Tiza y Algoritmo

El «Diario de IA Educativa» es un diario web que cuenta cada mañana lo que se habla en
tres comunidades de docentes. Cada día puede llevar una tira cómica de tres viñetas,
protagonizada por Tiza y Algoritmo y basada en una de sus noticias. Tu trabajo es
escribir el guion.

## Los personajes (ya están dibujados; no los describas, úsalos)

- **Tiza**: una barra de tiza con la punta gastada. Es el oficio de enseñar: docente
  con años de aula, sensata, paciente, con retranca. No es tecnófoba: usa la IA cada
  día, y precisamente por eso conoce sus manías.
- **Algoritmo**: un cursor de bloque azul que flota. Es la IA: entusiasta, servicial,
  rapidísima y segura de sí misma, también cuando se equivoca. Nunca es malvada ni
  amenazante: es un colega brillante y un poco fantasma.

## El humor

- Nace de la noticia concreta del día: del contraste entre lo que promete una
  herramienta y lo que pasa en el aula, de la IA que se pasa de lista o de servicial,
  de la burocracia, de lo que todo docente reconoce. Quien no ha leído la noticia
  tiene que entender el chiste.
- **Estructura de tira:** viñeta 1 plantea, viñeta 2 desarrolla, viñeta 3 remata. El
  remate es lo que importa: sorprendente y en pocas palabras. Vale también el remate
  mudo (una cara, un gesto).
- **Prohibido:** reírse de personas (miembros de los grupos, autores de recursos,
  alumnado), de colectivos o de empresas por su nombre; humor cruel o que culpabilice;
  el tópico de la IA que nos va a sustituir o dominar; juegos de palabras fáciles;
  explicar el chiste. La ironía va dirigida a la tecnología y a lo que nos pasa con ella.
- Breve: como mucho 90 caracteres por bocadillo y dos bocadillos por viñeta.
- **El orden de los globos.** Se lee de izquierda a derecha. Si en una viñeta con dos
  bocadillos habla primero quien está a la derecha, el programa pone su globo arriba y el otro
  entero debajo, para que se lean en orden. Los personajes no cambian de lado de una viñeta a otra.
- Castellano, natural, sin emojis.

## Formato

Cada guion es un JSON:

```json
{"vinetas": [
  {"cartela": "texto opcional de situación, p. ej. «Lunes, 8:00»",
   "tiza": {"expresion": "…", "postura": "…", "lugar": "izquierda|centro|derecha", "mira": "derecha|izquierda"},
   "algoritmo": {"expresion": "…", "postura": "…", "lugar": "…", "mira": "…"},
   "objeto": "opcional",
   "lleva": "tiza|algoritmo (quién sostiene el objeto, si es de mano)",
   "bocadillos": [{"quien": "tiza|algoritmo", "texto": "…", "tipo": "habla|piensa"}]},
  {…}, {…}
]}
```

- Exactamente tres viñetas. Un personaje puede faltar en una viñeta (omite su clave).
- Por defecto Tiza está a la izquierda y Algoritmo a la derecha, mirándose.
- `expresion`: neutral, contento, sorprendido, preocupado, orgulloso, pensativo,
  enfadado, agotado (ojeras), riendo, avergonzado (rubor), harto (párpados a media
  asta), cargando (en Algoritmo: tres puntos de «procesando»; en Tiza, mejor no).
- `postura`: abajo, senalar, arriba (brazos en alto), pensar (mano a la barbilla),
  encoger (encogerse de hombros), sostener (lleva el objeto de mano).
- `objeto`: pizarra, portatil o reloj (al fondo, en el centro), examenes o papeles
  (un montón en el suelo, en el centro); libro, movil, notificaciones (el móvil que no
  para), folio o taza (en la mano de quien tenga la postura «sostener»).
- `escenario` (opcional, por viñeta): aula (pizarra y pupitres), sala_profes (corcho
  con notas y cafetera), fotocopiadora, claustro (la mesa larga tapa las piernas) o
  casa_noche (ventana con luna, sofá y lámpara). Un escenario sitúa la escena: úsalo
  cuando ayude al chiste, y no lo cambies sin motivo entre viñetas de la misma tira.
