# Encargo: un artículo del fondo de EduMedia-IAG (pieza de reserva)

EduMedia-IAG es el grupo de Telegram sobre IA generativa de imagen, audio y vídeo para el aula. El
diario lleva cada día, como mínimo, un artículo de cada grupo; el día que EduMedia-IAG no da para
ninguno, sale uno de reserva escrito antes: este (ADR 0077). Se guarda y puede salir dentro de
semanas, así que **tiene que valer igual ese día**: nada de «esta semana», «acaba de salir» ni
«hoy». Lo leen docentes y personas interesadas que **no están** en el grupo.

## De dónde sale

La entrada (`edumedia-fondo-entrada/{FECHA}.md`) trae candidatos del historial del grupo: mensajes
de hace semanas o meses con un enlace a una herramienta, un tutorial o una técnica, que el diario no
ha contado. Con `mcp__diario__buscar_mensajes` (`--contexto edumedia:ID`) ves la conversación de
cada uno: qué se dijo, quién lo probó, qué problemas salieron.

## Qué se elige

**Uno solo**, que cumpla todo esto, comprobado hoy en su web oficial:

- **Sirve en clase** para trabajar con imagen, audio o vídeo: una herramienta, una función nueva de
  una herramienta conocida o una técnica (cómo conseguir algo con lo que ya hay).
- **Gratuita o con una versión gratuita que basta para usarla en clase.** Si solo es de pago, no.
- **Sigue existiendo y en las mismas condiciones**: la web responde, el producto no ha cambiado de
  nombre, de precio ni de licencia, y lo que se contó en el grupo sigue siendo cierto. Si algo ha
  cambiado, el artículo cuenta cómo está hoy, no cómo era.
- **No es noticia de un día** (un anuncio, un rumor, una demostración): tiene que seguir siendo útil.
- **No ha salido ya en el diario**: busca su nombre con `mcp__diario__buscar` y, con `parecidas`, el
  tema. Si salió como noticia, no vale.
- **Mejor una técnica o una herramienta consolidada** que una recién lanzada: dura más.
- **Atención a la edad**: si la herramienta exige ser mayor de edad o una edad mínima para el
  alumnado, el artículo lo dice y lo plantea para que la use el docente.

A `descartado` van **solo los que has mirado y no valen**, cada uno empezando por «mensaje <id>:» y
con el motivo comprobado («mensaje 9876: ahora solo es de pago»): ya no se vuelven a proponer nunca.
Los que no has llegado a mirar no se ponen, para que salgan otro día; tampoco el que eliges. Si
ninguno de los que miras vale, no hay artículo.

## Cómo es el artículo

- Sección **multimedia**, grupo **edumedia**, importancia **3**, antetítulo **«Del fondo de
  EduMedia»** siempre.
- 150-250 palabras. Qué es, qué se consigue con ello en clase (un ejemplo concreto de actividad),
  cómo se empieza (los pasos esenciales, sin nombres exactos de botones, que cambian), qué cuesta
  y sus límites (cuenta, edad, idioma, marca de agua, datos que pide).
- Lo que se habló en el grupo, sin nombres de quien opinaba: «en el grupo se compartió…». Al
  autor de un recurso que él mismo publicó sí se le nombra, con las reglas de `encargos/redaccion.md`.
- Las normas del libro de estilo (`encargos/estilo.md`) y de `encargos/enlaces.md` valen enteras. La fuente principal es la web oficial de la herramienta, con su nombre como texto del
  enlace en su primera mención.
- `ilustracion`: una idea para un dibujo que explique qué hace (un proceso, un antes y un después),
  nunca el logotipo ni una captura.

## El archivo

`ediciones-borrador/{FECHA}.json`, con la forma de una edición (`encargos/redaccion.md`), una sola
pieza y sin breves:

```json
{
  "fecha": "{FECHA}",
  "hay_edicion": true,
  "fondo": "edumedia",
  "motivo": "por qué se ha elegido este",
  "piezas": [{
    "id": "…", "seccion": "multimedia", "importancia": 3, "grupo": "edumedia",
    "antetitulo": "Del fondo de EduMedia", "titular": "…", "entradilla": "…", "cuerpo": "…",
    "fuentes": [{"titulo": "…", "url": "https://…"}],
    "herramienta": {"nombre": "…", "url": "la web oficial que se comprobará antes de publicarlo"},
    "mensaje": {"grupo": "edumedia", "id": 0},
    "comprobado": "qué has comprobado y dónde",
    "ilustracion": "idea para el dibujo"
  }],
  "breves": [],
  "descartado": ["mensaje <id>: motivo", "…"]
}
```

`herramienta.url` es la que se mira, sin IA, el día que se use la pieza: si deja de responder, la pieza
se retira. Tiene que ser la página principal de la herramienta, no un artículo sobre ella.
