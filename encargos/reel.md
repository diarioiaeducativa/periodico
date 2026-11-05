# Encargo: el guion de «La semana en vídeo»

Cada domingo el diario publica un vídeo vertical, sin voz y con música, que resume la semana: lo
más destacado de cada número, día a día (ADR 0016). Dura entre 50 segundos y un minuto y
medio, según cuántas piezas lleve. Sale en la web, en el número del domingo, y en Instagram
(@comunidad.iaeducativa), donde lo verán docentes que no conocen los grupos. Un programa monta el
vídeo con los dibujos y los colores del diario; tú eliges las piezas y escribes los textos que
salen en pantalla. Nadie los revisa antes de que se publiquen.

## Qué piezas

- Es un resumen de verdad, no trozos sueltos: **como mínimo una pieza de cada número de la
  semana**, la más interesante de ese día. Los números son las ediciones de `ediciones/` (y de
  `biblioteca/` y `repositorio/`) con fecha desde el domingo anterior hasta el sábado de este
  encargo, ambos incluidos: cada `fecha` con alguna pieza es un número.
- Si algún día tuvo más de una pieza que valga la pena, puedes añadir hasta tres más en total:
  **como mucho 10 piezas**. Ningún día puede quedarse sin la suya para dejar sitio a otro.
- Pon las noticias en orden de fecha. El programa escribe en cada una el día en que salió.
- Entre las de un mismo día, la que más interesa a un docente cualquiera y se entiende en tres
  segundos. En el conjunto, no dos piezas del mismo tema.
- Solo piezas que existen en esas ediciones, con su `fecha` y su `id` exactos.

## Qué textos, por pieza, en castellano y en catalán

- **golpe**: de una a tres palabras, como un rótulo (sale en mayúsculas y enorme): el tema. No
  pongas el día: lo pone el programa.
  Como mucho 22 caracteres. «Detectores de IA», «Google», «Ciencia en 3D».
- **titular**: una frase corta que diga qué ha pasado, sin punto final. Como mucho 60 caracteres.
- **dato**: el detalle que lo hace interesante, concreto y comprobable en la pieza. Como mucho
  90 caracteres.
- Todo sale de la pieza: nada que no diga ella. Habla de temas, no de personas (se nombra solo
  al autor de un recurso que él mismo ha publicado, también si es Juanjo de Haro).
- El catalán, natural y correcto, no calcado. Los nombres propios de productos y grupos no se traducen.

## Además

- **descripcion** (es y ca): una o dos frases que resuman el vídeo para la web, entre 80 y 240
  caracteres.
- **instagram**: el texto que acompaña al vídeo en Instagram, en castellano: de dos a cuatro
  frases que cuenten lo de la semana para quien no conoce los grupos. Entre 150 y 600 caracteres.
  Impersonal, sin saludo, sin enlaces, sin etiquetas (#), sin emojis ni exclamaciones: el
  programa añade el aviso de IA, la remisión al perfil y las etiquetas.
- Tono informativo, nunca publicitario. Lenguaje inclusivo natural.

## Salida

`reels/<fecha del sábado>.json`, JSON válido en UTF-8:

```json
{"fecha": "2026-11-07",
 "noticias": [
  {"fecha": "2026-11-03", "id": "google-ia-cuentas-escolares",
   "golpe": {"es": "Google", "ca": "Google"},
   "titular": {"es": "IA apagada por defecto en las cuentas escolares", "ca": "IA apagada per defecte als comptes escolars"},
   "dato": {"es": "Cada centro decide qué activa, producto a producto", "ca": "Cada centre decideix què activa, producte a producte"}}],
 "descripcion": {"es": "…", "ca": "…"},
 "instagram": "…"}
```
