# Encargo: el reportaje del domingo

Los domingos, además del número del día, el diario publica un reportaje: un solo tema de
la semana, tratado a fondo. Es para profesorado y personas interesadas que **no están**
en los tres grupos (ChatGPT-IA-edu, Vibe Coding Educativo y EduMedia-IAG).

**No es un resumen de la semana**: eso ya lo hace cada lunes el boletín semanal de los
grupos. Las piezas diarias cuentan lo que se dijo; el reportaje explica el asunto entero:
qué es, por qué importa en un centro educativo, qué dicen quienes tienen algo que decir y
qué puede hacer un docente. Se publica sin que nadie lo revise antes: la comprobación del
revisor es la única revisión. **El reportaje sale siempre** (Juanjo, 06-11-2026: «el reportaje no puede
faltar, siempre estará»): si la semana va floja, el tema puede venir de las semanas anteriores, si
sigue vivo, o de un documento de la Biblioteca digital (`biblioteca/*.json`) que merezca explicarse a
fondo y no haya tenido reportaje.

## Entrada

- `semanas/<FECHA>.md`: los mensajes de los tres grupos de los siete días que acaban en
  FECHA (el sábado).
- `ediciones/*.json` de esos siete días: las piezas diarias ya publicadas sobre la semana.
- `reportajes/*.json`: los reportajes anteriores, para no repetir tema.

## Cómo se elige el tema

- Ha salido en más de un grupo o en varios días, o ha generado un debate con argumentos.
- Da para algo más que una pieza diaria: tiene contexto, actores, normativa o práctica de aula
  que contar. Una novedad de un día, sin más recorrido, no basta.
- Interesa a un docente corriente, no solo a quien programa o a quien ya lo domina.
- No lo ha tratado un reportaje anterior (salvo un cambio de fondo).
- Ante la duda, el que más ayude al profesorado a decidir o a actuar.

## Qué lleva

- **Lo que se habló en los grupos**, sin nombrar a quien opina: las posturas, las dudas, las
  experiencias. Cada vez que se recoja algo de los grupos, enlazado a su mensaje exacto con
  Markdown: `[texto](https://t.me/<alias>/<id>)` (alias: ChatGPTedu, vceduca, EduMediaIAG).
  Solo se nombra a quien ha publicado un recurso propio, como crédito, también si es Juan José de Haro (así, no «Juanjo»),
  y sin su cargo (administrar un grupo, ser coautor del diario) salvo que tenga que ver con la noticia.
- **Lo que dicen los actores implicados, uno por uno y con sus documentos**: las empresas
  (OpenAI, Google, Anthropic, Microsoft…), las administraciones educativas, la AEPD, la Unión
  Europea, organismos internacionales (UNESCO, OCDE), según el tema. Cada uno, con su
  documento oficial enlazado, en castellano o catalán si existe esa versión.
- **El marco en España**: la normativa y las guías del Ministerio y de las comunidades
  autónomas, si las hay. Si solo unas pocas tienen guía, se dice cuáles y que el resto no.
- **Estudios o informes** que aporten datos, con su autor nombrado en el texto. Una cifra, con
  la precisión de la fuente y su cantidad absoluta.
- **Qué puede hacer un docente**: recomendaciones prácticas, al alcance de cualquiera, sin pagar
  nada ni saber más de lo habitual.
- Si hay posturas serias en los dos sentidos, las dos.

## Rigor (lo más importante)

- Cada afirmación sobre un producto, una cifra, una norma o un documento se comprueba en la
  fuente original con WebSearch/WebFetch. A la fuente original, no a un artículo que la recoge.
- Lo que no puedas comprobar: o lo quitas, o lo dices como no confirmado.
- Fechas y datos cambiantes, fechados («a 1 de noviembre de 2026…»).
- En `comprobado`, qué comprobaste y dónde, por apartados.

## Estilo

- Castellano. Tono formal, informativo e impersonal, de reportaje de suplemento; nunca
  publicitario ni alarmista. Sin emojis. Lenguaje inclusivo pero natural.
- Titular claro, con verbo, sin preguntas. Antetítulo de 2-5 palabras. Entradilla de dos o
  tres frases que diga de qué va y qué se lleva el lector.
- Entre 1.200 y 1.800 palabras de cuerpo, en 4 a 6 apartados con ladillo (un sustantivo o
  una frase corta, sin imitar preguntas frecuentes). Párrafos de 3 a 6 frases.
- Negritas con mesura: dos o tres ideas en todo el reportaje.
- Se entiende solo, sin haber estado en los grupos ni haber leído las piezas diarias.

## Lo ya publicado

Enlaza en el texto lo que el diario ya ha publicado y está claramente relacionado (la misma
herramienta, el mismo documento, el mismo debate), como dice `encargos/enlaces.md`, con las claves
de `publicado.txt`.

## Salida

`reportajes/<FECHA>.json` (JSON válido, UTF-8):

```json
{
  "fecha": "AAAA-MM-DD (el sábado)",
  "hay_reportaje": true,
  "motivo": "por qué este tema (o por qué no hay reportaje)",
  "id": "reportaje-corto-sin-espacios",
  "antetitulo": "…",
  "titular": "…",
  "entradilla": "…",
  "apartados": [{"ladillo": "…", "parrafos": ["…", "se admiten enlaces [texto](url) y **negritas**"]}],
  "claves": ["tres a cinco ideas para llevarse, una frase cada una"],
  "relacionadas": [{"fecha": "AAAA-MM-DD", "id": "id de una pieza diaria de la semana sobre el tema"}],
  "fuentes": [{"titulo": "… (autor u organismo)", "url": "https://…"}],
  "mensaje": {"grupo": "chatgpt | vce | edumedia", "id": 0},
  "comprobado": "qué se comprobó y dónde",
  "ilustracion": "idea para una infografía SVG que explique lo esencial del reportaje"
}
```

- `mensaje`: el mensaje donde arrancó la conversación principal sobre el tema.
- `relacionadas`: solo piezas que existan en `ediciones/` (comprueba `fecha` e `id`).
- `fuentes`: todas las fuentes externas del cuerpo, también las citadas de pasada. Lo que el texto nombra, enlazado también
  en su primera mención (`encargos/enlaces.md`).
