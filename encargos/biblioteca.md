# Encargo: los artículos de la Biblioteca digital

La Biblioteca digital es el tema de ChatGPT-IA-edu donde los miembros dejan documentos sobre
IA y educación: guías de las administraciones, informes de organismos, estudios, libros. Cada
documento llega con una ficha (referencia, resumen, palabras clave, licencia). El diario dedica
a cada documento nuevo un artículo en su sección «Biblioteca», para profesorado y personas
interesadas que **no están** en el grupo. Se publica sin que nadie lo revise antes: el repaso es
la única revisión.

## Qué es el artículo (y qué no)

- **No repite la ficha**, que ya es un resumen. Explica el documento a quien no lo ha leído:
  quién lo publica y con qué autoridad (una consejería, un organismo internacional, un grupo de
  investigación, un docente), a quién va dirigido, qué propone o qué encuentra, qué tiene de
  nuevo o de útil para un docente y qué límites tiene.
- **Dice lo que dice el documento**, con alguna cita breve y exacta entre comillas (como mucho
  dos, de menos de 25 palabras cada una) y los datos concretos que aporte (cifras, criterios,
  ejemplos), con la precisión de la fuente.
- **Lo sitúa**: si en la biblioteca hay documentos que tratan lo mismo (están en la lista de
  la entrada), cómo se relaciona con ellos, con su enlace al mensaje y, como texto del enlace, el título o una descripción del documento (nunca «mensaje 123»). Si es una versión nueva
  de otro, qué cambia. Sin inventar relaciones.
- Termina con lo que puede sacar de él un docente: para qué le sirve, por dónde empezar a leer.

## Un documento que el diario ya ha contado

La entrada trae las piezas publicadas en el diario en los últimos días, con sus fuentes. Si una
de ellas ya trataba **este mismo documento** (el propio documento, su presentación, la nota de
prensa que lo anunciaba o una noticia sobre él), no se escribe otro artículo: el diario no repite
un tema en días seguidos. Ese documento va a `ya_contado`, con la fecha y el id de la pieza que lo
contó, y esa pieza pasa a la sección Biblioteca con el enlace al documento. Que traten el mismo
tema no basta: tiene que ser el mismo documento (otro informe del mismo organismo, o una versión
nueva, sí lleva artículo, que explica qué cambia).

Y la pieza tiene que haber leído **el documento en sí**: lo dice su «leído» en la lista de piezas
de la entrada. Si se escribió con la nota de prensa, una página de presentación o una noticia
sobre él, el documento no está contado: lleva su artículo, centrado en lo que la pieza no dijo,
enlaza a ella en una frase y no repite lo que ella ya contó. Si el documento contiene más de lo
que la pieza trató (otro informe dentro del mismo PDF, apartados que no tocó), tampoco está
contado.

Si dos documentos del día son el mismo (el enlace a la ficha y el PDF, por ejemplo), un solo
artículo, con el `mensaje` del que trae el texto completo; el otro va a `descartado`, empezando
por «mensaje <id>:» y diciendo con qué mensaje se contó.

## Del fondo de la biblioteca (pieza de reserva)

Cuando la entrada lo dice, no trae documentos de hoy sino candidatos del fondo: documentos que
entraron hace tiempo y el diario no ha contado. El artículo se guarda en la reserva y sale el día
que la redacción no pueda preparar el número (ADR 0021), así que tiene que valer igual dentro de
semanas.

- **Elige uno solo, y que siga vigente.** Antes de escribir, comprueba en internet que es la
  última versión (si el organismo ha publicado una edición nueva, una actualización o un documento
  que lo sustituye, no vale), que no se ha retirado y que lo que propone no ha quedado superado
  (una guía sobre una herramienta que ya no existe, un informe cuyas cifras ya se han renovado).
  Si ninguno vale, no hay artículo: los tres a `descartado`.
- **Los demás candidatos, a `descartado`**, cada uno empezando por «mensaje <id>:» y con el motivo
  («mensaje 21890: hay una versión de 2026 que lo sustituye»). Así no se vuelven a proponer. Los
  candidatos traen el texto completo del PDF o son enlaces con su ficha: léelos enteros.
- **Antetítulo «Del fondo de la biblioteca»**, siempre. El artículo no lo presenta como novedad ni
  dice «hoy» o «esta semana»: dice cuándo se publicó el documento y por qué sigue siendo útil.
- Lo demás, como cualquier artículo de la biblioteca.

## Lo ya publicado

Enlaza en el texto lo que el diario ya ha publicado y está claramente relacionado (la misma
herramienta, el mismo documento, el mismo debate), como dice `encargos/enlaces.md`, con las claves
de `publicado.txt`.

## Personas

- Se nombra a los autores del documento o al organismo que lo publica.
- **No se nombra a quien lo ha subido a la biblioteca**, salvo que sea también su autor. Juan José de
  Haro (así, no «Juanjo», aunque en los grupos firme así), como cualquiera: se le nombra si es
  autor del documento. Los cargos (administrar un grupo,
  ser coautor del diario), solo si tienen que ver con la noticia.

## Rigor (lo más importante)

- **Lee el documento entero.** Si la entrada trae el «Texto completo del PDF», ese texto es el
  documento tal como está en la biblioteca: léelo entero y escribe con él. Busca además su fuente
  oficial con WebSearch y WebFetch (el DOI, la página del organismo o el PDF en su sitio) para
  enlazarla; si no la encuentras o no deja leer, `documento.url` queda vacío y el artículo enlaza
  al documento en la biblioteca, que ya lo hace el diario con `mensaje`.
- Si la entrada solo trae la ficha o el comienzo del PDF, lee el documento en su fuente oficial.
  Si no la hay o no deja leer, apóyate solo en una fuente fiable que lo resuma (mejor de sus
  propios autores), dilo en el texto, y si eso no basta para un artículo digno, no lo hay.
- El enlace del documento es siempre el oficial, nunca una copia de terceros.
- Nada de inventar fechas, cifras, autores ni capítulos.
- En `comprobado`, qué leíste y dónde.

## Estilo

- Castellano. Tono formal, informativo e impersonal, nunca publicitario. Sin emojis. Lenguaje
  inclusivo pero natural.
- Titular claro, con verbo, que diga qué aporta el documento (no solo su título). Antetítulo de
  2-5 palabras con el tipo de documento («Guía oficial», «Informe de la UNESCO»).
- Entre 400 y 700 palabras de cuerpo, en párrafos de 3 a 6 frases.
- Documentos en catalán u otra lengua: se describen en castellano y se respeta su título.

## Salida

`biblioteca-borrador/<FECHA>.json` (JSON válido, UTF-8):

```json
{
  "fecha": "AAAA-MM-DD",
  "piezas": [
    {
      "id": "corto-sin-espacios",
      "seccion": "biblioteca",
      "importancia": 2,
      "grupo": "chatgpt",
      "antetitulo": "…",
      "titular": "…",
      "entradilla": "una o dos frases",
      "cuerpo": ["párrafo", "párrafo; se admiten enlaces [texto](url) y **negritas**"],
      "documento": {"titulo": "título original", "autoria": "autores u organismo", "anyo": "2026",
                    "idioma": "castellano | catalán | inglés…", "licencia": "la que conste, o «no consta»",
                    "url": "https://… (oficial)"},
      "fuentes": [{"titulo": "…", "url": "https://…"}],
      "mensaje": {"grupo": "chatgpt", "id": 0},
      "comprobado": "qué se leyó y dónde",
      "ilustracion": "idea para un dibujo SVG que explique lo esencial del documento (un esquema de lo que propone, no su portada)"
    }
  ],
  "ya_contado": [
    {"mensaje": {"grupo": "chatgpt", "id": 0}, "fecha": "AAAA-MM-DD de la pieza que lo contó",
     "id": "id de esa pieza", "titular": "su titular", "motivo": "por qué es el mismo documento"}
  ],
  "descartado": ["documento sin artículo y por qué"]
}
```

- Una pieza por documento de la entrada, en el mismo orden, salvo los que van a `ya_contado`.
- `mensaje`: el id del mensaje del documento en la biblioteca, tal como lo da la entrada.
- `fuentes`: el documento oficial primero y todo lo demás que cites. Lo que el texto nombra, enlazado también
  en su primera mención (`encargos/enlaces.md`).
