# Encargo: los recursos del Repositorio de Vibe Coding Educativo

El [Repositorio de recursos](https://vibe-coding-educativo.github.io/app_edu/) de Vibe Coding
Educativo reúne las aplicaciones y recursos educativos digitales que el profesorado de esa
comunidad crea, casi siempre con ayuda de la inteligencia artificial, y comparte con licencia
abierta. El diario los cuenta en su sección «Vibe coding», para profesorado y personas
interesadas que **no están** en el grupo. El repaso es la única comprobación de cada dato contra su fuente:
escribe como si nadie más fuera a revisarlo.

La entrada (`repositorio-entrada/<FECHA>.md`) dice el **modo**:

- **dia**: un artículo por cada recurso de la entrada. Antetítulo «Nuevo en el repositorio».
- **semana**: el número del sábado resume la semana del repositorio. **Una sola pieza** con
  todos los recursos que aún no ha contado el diario. Antetítulo «La semana del repositorio».
  Lo que entró en la semana y ya tuvo su artículo viene en la entrada, en «Ya contados esta
  semana»: no lo describas otra vez, porque el programa añade al final de la pieza su lista con
  el enlace a cada artículo. La entradilla da el total de la semana y cuántos se presentan aquí
  («El Repositorio de recursos de Vibe Coding Educativo suma esta semana nueve recursos: cuatro
  se presentan aquí y cinco ya tuvieron su artículo»). Si no queda ninguno por contar, la pieza
  va sin `recursos`: titular, entradilla y un párrafo breve que resume la semana a partir de esa
  lista.
- **fondo**: un día con poco que contar y sin recursos nuevos. La entrada trae varios recursos
  antiguos del repositorio: **elige uno**, el que más pueda servir hoy a un docente y funcione
  bien, y escribe su artículo. Antetítulo «Del fondo del repositorio». Los demás no se
  descartan: no los pongas en `descartado`.

## Qué cuenta el artículo

- Qué es el recurso y qué hace, para qué nivel y materia, y qué puede hacer con él un docente
  en clase. Lo que tiene de propio frente a lo habitual (funciona sin conexión, guarda los
  datos en el dispositivo, está en catalán, se puede adaptar…), si lo tiene.
- Cómo se usa, en pocas palabras: si se abre en el navegador sin cuenta, si se descarga, si
  tiene versión para imprimir.
- **Lo que se ve, no lo que promete.** Escribe a partir de la captura (ábrela con Read), del
  texto que se ve en la página y de la propia página (WebFetch). La captura y el texto visible
  salen de un navegador de verdad, que ejecuta el programa; **WebFetch no ejecuta JavaScript**,
  así que con una aplicación suele devolver poco, un error o solo el título. Eso no quiere decir
  que no funcione: mandan la captura y el texto visible. La descripción de la ficha
  orienta, pero la ha escrito el autor o el bot: lo que diga y no se vea en el recurso, o no
  se dice, o se dice como suyo («según su autor…»).
- **El mensaje que lo compartió.** Si la entrada trae el mensaje con que se compartió el recurso
  en un grupo (casi siempre, la presentación de su autor), léelo: dice lo que la página no
  enseña al abrirla (otro idioma, otra versión, para qué lo hizo). Lo que diga y no se vea en el
  recurso va como suyo («según su autor…»). El mensaje va en `fuentes`, con el título
  «Presentación en <grupo>».
- **Idiomas y versiones.** Antes de decir que un recurso está en una lengua, o que es solo para
  algo, mira si tiene más: el selector de idioma, una versión en `/es/` o `/ca/`, el campo
  «Idiomas» de la entrada y el mensaje del autor. Que la página se abra en catalán no quiere
  decir que solo esté en catalán.
- Con la autoría y la licencia, tal como constan en la ficha.
- Solo lo que sirve al docente: nada de detalles técnicos que no le cambian nada (que un enlace
  redirige a otro, dónde está alojada la web), y nada sobre cómo trabaja el diario («se
  describen según lo visto al abrirlos»): eso ya lo explica «La redacción».
- Recursos en catalán u otra lengua: se describen en castellano y se respeta su nombre.

## Cuándo no hay artículo

Pasa el recurso a `descartado` (con su `url` y el motivo) si la captura muestra que no abre o
da error, si no se puede usar sin cuenta o sin pagar, si no es un recurso educativo, si la página no deja ver qué hace (una
página en blanco, un aviso de error) o si no hay nada fiable que contar. Mejor sin artículo
que con uno dudoso. En modo **semana**, los descartados se quedan fuera de la pieza.

## Lo ya publicado

Enlaza en el texto lo que el diario ya ha publicado y está claramente relacionado (la misma
herramienta, el mismo documento, el mismo debate), como dice `encargos/enlaces.md`, con las claves
de `publicado.txt`.

## Personas

- Se nombra a la autora o el autor del recurso, como crédito («creada por …»), con el nombre
  tal como figura en la ficha. **Juan José de Haro, como cualquiera**: si el recurso es suyo, se le
  nombra y `autoria` lleva su nombre igual que la de los demás. En el diario es «Juan José de
  Haro», también en `autoria`, aunque la ficha diga «Juanjo». Los cargos (administrar un grupo,
  ser coautor del diario), solo si tienen que ver con la noticia.
- En modo **semana**, los recursos de una misma persona van juntos y seguidos, y la pieza
  puede decirlo («Felip Sarroca suma esta semana tres aplicaciones de química…»).

## Rigor

- Abre cada recurso (WebFetch) y mira su captura. Nada de inventar funciones, niveles ni
  cifras.
- El enlace es siempre el de la web que usará el lector. Si la ficha lleva a un repositorio
  de código (GitHub), busca si tiene web pública; si no la tiene, se dice que se descarga
  desde su repositorio, y `captura` queda vacío.
- Si el recurso se apoya en un servicio ajeno (un modelo de IA, una API), dilo, con lo que
  exige (cuenta, clave, pago).
- En `comprobado`, qué abriste y qué viste.

## Estilo

- Castellano. Tono formal, informativo e impersonal, nunca publicitario: nada de «increíble»,
  «imprescindible» ni exclamaciones. Sin emojis. Lenguaje inclusivo pero natural.
- Titular claro, con verbo, que diga qué permite hacer el recurso (no solo su nombre). En modo
  semana, el titular resume lo de la semana («Formulación química, dictados en catalán y un
  mapa del potencial gravitatorio, nuevos en el repositorio»).
  El titular no pasa de 90 caracteres, contando los espacios: lo que no quepa va al antetítulo o a la entradilla.
- **dia** y **fondo**: entre 250 y 350 palabras de cuerpo, en párrafos de 3 a 5 frases.
- **semana**: `cuerpo` con un solo párrafo breve de presentación (2 o 3 frases: cuántos
  recursos, de qué tratan); cada recurso, en su `texto`, con 80 a 120 palabras. No expliques qué
  es el repositorio ni que la pieza sale cada sábado: lo dice una línea fija que pone el programa
  bajo la entradilla.

## Salida

`repositorio-borrador/<FECHA>.json` (JSON válido, UTF-8):

```json
{
  "fecha": "AAAA-MM-DD",
  "piezas": [
    {
      "id": "el id del recurso (dia, fondo) o «semana-del-repositorio» (semana)",
      "seccion": "vibecoding",
      "repositorio": "dia | semana | fondo",
      "importancia": 2,
      "grupo": "vce",
      "antetitulo": "el que dice la entrada",
      "titular": "…",
      "entradilla": "una o dos frases",
      "cuerpo": ["párrafo", "párrafo; se admiten enlaces [texto](url) y **negritas**"],
      "recursos": [
        {"id": "el id de la entrada", "titulo": "nombre del recurso", "autoria": "como en la ficha, o vacío",
         "url": "https://… (la web del recurso)", "ficha": "la ficha en el repositorio, tal como la da la entrada",
         "licencia": "la de la ficha", "captura": "solo el nombre del archivo, como lo da la entrada (AAAA-MM-DD-id.jpg), o vacío",
         "captura_alt": "qué se ve en la captura, en una frase, para quien no la ve",
         "texto": ["solo en modo semana: el párrafo de este recurso"]}
      ],
      "fuentes": [{"titulo": "…", "url": "https://…"}],
      "comprobado": "qué se abrió y qué se vio"
    }
  ],
  "descartado": [{"url": "https://…", "motivo": "…"}]
}
```

- **dia**: una pieza por recurso, en el orden de la entrada, con un solo elemento en `recursos`
  y su `texto` vacío; el artículo va en `cuerpo`.
- **semana**: una sola pieza con todos los recursos en `recursos`, agrupados por autoría.
- **fondo**: una sola pieza, con el recurso elegido.
- `fuentes`: la web de cada recurso primero y todo lo demás que cites. La ficha del
  repositorio ya la enlaza el diario: no hace falta repetirla. Lo que el texto nombra, enlazado también
  en su primera mención (`encargos/enlaces.md`).
