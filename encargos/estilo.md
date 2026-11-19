# Libro de estilo del Diario de IA Educativa

Cómo escribe el diario. Vale para todo agente que escribe, revisa, traduce o resume algo que va a
leer el público (artículos, breves, reportajes, «Hace un año», comentarios de la semana, avisos,
textos para redes y vídeos) y para las personas que lo mantienen. Se lee entero antes de empezar.

Aquí está lo común. Cada tarea tiene además su guía en `encargos/` con lo propio (medidas, formato,
tono de los avisos, la viñeta…); si una norma de aquí no vale para una tarea, su guía lo dice. Las normas que no son de estilo (qué es noticia, qué lleva cada número y los artículos guardados
para los días sin noticias) están en «Cómo se hace el diario», `docs/como-se-hace.md`.

## Para quién se escribe

- Para docentes y personas interesadas en la IA en educación que **no están** en los grupos. Cada
  texto se entiende solo, sin haber leído los mensajes ni otros artículos: qué es, por qué importa a
  un docente y dónde encontrarlo.
- **Para un público muy amplio, no para expertos**: un docente de cualquier materia, una familia, una
  persona que empieza con la IA. Si algo solo lo entienden las personas que ya saben del tema, se reescribe.
- Lo que interesa al lector, no cómo funciona el diario por dentro: nada de agentes, ficheros,
  programas ni servidores en lo que se publica, salvo que el artículo trate del propio diario o de
  Anthropic (apartado «Rigor»).

## Tono

- Formal, informativo e impersonal. Nunca publicitario («increíble», «imprescindible», «revoluciona»)
  ni alarmista. Sin exclamaciones ni emojis.
- Las guías de los avisos y de la viñeta permiten un tono más cercano; nunca de anuncio.

## Lengua

- Castellano correcto y natural. Las traducciones, en su apartado.
- **Lenguaje inclusivo, pero natural**: «el profesorado», «el alumnado», «las familias»; sin
  desdoblamientos ni signos raros.
- **Sin el relativo «quien» o «quienes»** con el sentido de «la persona que»: «la persona que», un colectivo («el
  profesorado») o un giro con el asunto delante («separar la creación de la revisión», no «separar a
  quien crea de quien revisa»). El interrogativo, con tilde («¿quién?»), sí; una cita literal se
  deja como está.
- **Lo que publica el diario son «artículos»**, no «piezas» (la palabra solo es interna, en los
  campos de los archivos). Un artículo puede ser una noticia, un breve, un reportaje.
- **Lo que hace el diario con un tema: lo «publica», lo «recoge»** o el tema «sale en» el diario;
  no lo «cuenta». «El diario publicó el 3 de noviembre…», «como recogió el diario…».
- **La IA no piensa ni quiere.** Nada de verbos que dan mente o intención a un programa («piensa»,
  «entiende», «quiere», «miente»): un modelo genera, responde o da un resultado. Lo que decide es una
  empresa o una persona: «OpenAI ha limitado…», no «ChatGPT ha decidido…». Lo que un modelo inventa
  es una «respuesta inventada»; «alucinación», solo explicada.
- **Vocabulario**: «inteligencia artificial», en minúscula, y su sigla, IA, nunca AI, salvo en
  nombres propios («Google AI Studio»). «Chatbot» y «alucinar», sin comillas. Mejor «aplicación» que
  «app», «en línea» que «online», «enlace» que «link» y «aprendizaje automático» que «machine
  learning». *Prompt*, en cursiva. Un término que el lector puede no conocer se explica la primera
  vez.
- **Siglas**: una poco conocida se desarrolla la primera vez («la Agencia Española de Protección de
  Datos (AEPD)»); una técnica inglesa (LLM, API, MCP) va con lo que es («un modelo de lenguaje
  (LLM), el tipo de programa que hay detrás de ChatGPT»). Si no se vuelve a usar, no se pone.
- **Sin condicional de rumor**: no «OpenAI habría lanzado…», sino «según [fuente], OpenAI ha
  lanzado…» o «es posible que…».
- **Frases claras**: una idea por frase, la palabra corriente antes que la técnica y fuera las
  metáforas gastadas («cambio de paradigma», «en la era de la IA»).
- **Antes claro que breve.** Nada de expresiones comprimidas que obligan a releer: sustantivos
  encadenados («flujo de generación multimodal con verificación cruzada»), jerga de los grupos,
  palabras que se dan por sabidas o frases a las que les falta el verbo. Si una frase corta se entiende
  peor que una algo más larga, va la larga: «un sistema que crea imágenes y vídeo y comprueba el
  resultado con otro modelo».
- Los nombres de productos, aplicaciones, grupos y documentos, tal como los escribe la empresa o la persona que los hace
  («ChatGPT», «Vibe Coding Educativo»). Un recurso en catalán u otra lengua se describe en castellano
  y conserva su nombre; el título de una obra queda en su idioma.

## Titulares, antetítulos y entradillas

- **Titular**: claro, con verbo, sin preguntas ni ganchos («no creerás…»). Dice qué aporta lo que
  recoge, no solo el nombre de la herramienta o del documento. **Como mucho 90 caracteres**, contando
  los espacios: lo que no quepa va al antetítulo o a la entradilla.
- **Antetítulo**: de dos a cinco palabras, sin verbo: el tipo de cosa o el ámbito («Guía oficial»,
  «Nuevo en el repositorio», «Del fondo de EduMedia»).
- **Entradilla**: una o dos frases que resumen el artículo (dos o tres en el reportaje). No repite el
  titular: aporta lo siguiente.
- **El titular y la entradilla no dicen más que el cuerpo ni que la fuente.** Lo que el cuerpo
  matiza («según la empresa», «en los planes de pago», «es una hipótesis del autor») no desaparece
  arriba. Una prueba sin nada con que comparar no «demuestra» ni «sugiere» una causa.
- **Lo que no es de estos días lleva su fecha en el titular**: un informe de agosto no «se publica»
  hoy, es «Un informe de agosto…».

## Personas

- **Temas, no personas.** No se nombra a las personas que opinan o preguntan en los grupos, tampoco con «un
  miembro dijo…»: se recogen las posturas.
- **Se nombra al autor de un recurso que él mismo ha publicado** (una aplicación, una guía, un
  documento), como crédito («creada por…»), con el nombre que consta en el propio recurso o el
  nombre completo de la persona que lo publica. Un nombre de pila no identifica a nadie: si el recurso no
  dice quién lo hace, «su autor», y que la web no lo indica. Nunca se completa un apellido.
- **Quién es quién lo dice la marca del material, no el nombre** (ADR 0066): los autores del diario
  son solo los mensajes marcados `[autor del diario: …]`; otra persona con el mismo nombre de pila es
  otra persona. Las marcas no se publican.
- **Los autores del diario, como cualquiera**: se nombran como crédito de sus recursos igual que los
  demás, con el nombre completo con que firman el diario, aunque en los grupos usen otro.
- **Los cargos, solo si tienen que ver con la noticia** (administrar un grupo, ser coautor del
  diario): si no, la persona es un docente más.
- **Si el artículo trata del propio diario, lo dice** con esas palabras («este diario»).
- **El alumnado**: no se publica nada que lo identifique (nombre, imagen, ni centro y curso juntos),
  aunque aparezca en el material compartido. De una herramienta para el aula se dice, según sus
  condiciones, si pide datos del alumnado y si los usa para entrenar sus modelos; si no consta, se dice.

## Rigor

- **Cada afirmación se comprueba en la fuente original**: el anuncio oficial, la página del producto,
  el documento de la administración. Un mensaje del grupo, un enlace a X o un vídeo no bastan.
- **Lo que no se puede comprobar, se quita o se dice como no confirmado.** Nada de inventar
  fechas, cifras, autores ni funciones.
- **Lo que anuncia una empresa, con sus condiciones**: en qué plan, a qué precio, hasta cuándo, en qué
  países. «Gratis» o «para todos» se contrasta con sus condiciones.
- **El lenguaje de las empresas, atribuido o fuera**: «revolucionario», «potente» o «sin
  precedentes», solo dentro de una cita atribuida; el texto dice qué hace el producto. Un estudio o una
  encuesta se presenta con quién lo hace y quién lo paga, y si es de la propia empresa, se dice
  («según un estudio de la propia OpenAI»). Una nota de prensa no se reproduce: se identifica y se
  reescribe.
- **Cuando un artículo trata de Anthropic o de Claude**, una frase recuerda que el diario lo escriben
  agentes de Claude, para que el lector lo tenga en cuenta. Nombrarlos de pasada, en una lista, no lo pide.
- **Las cifras, con la precisión de la fuente** (sin decimales que la fuente no da) y una proporción
  con su cantidad absoluta («el doble, de 10 a 20 centros»). Si la fuente da cifras distintas según
  la versión o el plan, se dice a cuál corresponde cada una. Del 20 % al 30 % son 10 puntos más, no
  un 10 % más. Mejor «uno de cada ocho docentes» que «el 12,5 %».
- **Una norma, aplicada al caso**: si el artículo cuenta lo que exige una ley o una autoridad, dice también
  qué supone para lo que trata (si hace falta permiso, un aviso o nada), y no deja que el lector saque la
  conclusión (Juanjo, 19-11-2026, ante las condiciones de la AEPD en la pieza de Umami: «debes hacerlo tú»).
- **Los datos que cambian se fechan** («a 1 de noviembre de 2026»); lo demás no lleva fecha.
- **Toda hora, con su huso**, porque el diario se lee en todo el mundo (ADR 0091). La de España:
  «a las 10:30 (hora peninsular española, UTC+1)», UTC+2 en verano; «peninsular», porque Canarias va
  una hora por detrás. La de fuera, con la de origen y la equivalente en España: «a las 10:00 de
  California (19:00 en la España peninsular, UTC+1)». Si un texto da varias horas del mismo sitio, el
  huso va la primera vez.
- **Una página oficial puede estar desactualizada**: si contradice lo que el diario ya publicó con el
  documento delante, manda lo publicado, y se dice.
- **Antes de juzgar un enlace, se abre**: la dirección no dice lo que hay en la página ni su fecha.
- **Lo que el diario ya publicó, igual**: un artículo sobre un asunto ya tratado da las mismas
  cifras y fechas que el anterior, lo enlaza y, si algo ha cambiado, lo dice.

## Citas y otros idiomas

- Citas breves y exactas, entre comillas, y pocas: el artículo explica, no copia.
- **Lo que va entre comillas se busca tal cual en la fuente**; si no aparece, se quita o se
  parafrasea. Una frase tomada de una fuente va entre comillas o se reescribe.
- **Ninguna cita solo en inglés**: o traducida, o con la traducción al lado entre paréntesis.
- Lo oficial ajeno (el título de una norma, de un informe) queda en su idioma original.

## Fuentes y enlaces

Lo detallado está en `encargos/enlaces.md`; lo esencial:

- **Lo que se nombra se enlaza donde se nombra**, en su primera mención y con su nombre como texto del
  enlace; al pie, en `fuentes`, todas.
- **A la fuente original y oficial**, en castellano (o en catalán) si existe esa versión; una
  herramienta, a la web que usará el lector, no a su repositorio de código.
- **Lo ya publicado que está claramente relacionado, enlazado** con su clave (`pieza:AAAA-MM-DD/id`),
  con un texto que diga de qué trata, nunca «aquí».
- El texto de un enlace nunca es «mensaje 123» ni una dirección desnuda.
- Un enlace que descarga un archivo lo dice: «la guía (PDF)».

## Forma

- **Comillas españolas** («»); dentro de ellas, las inglesas (“”).
- **El porcentaje, con espacio** (25 %); los millares, con punto (1.200); las monedas, con su nombre
  («10 dólares», «4 euros»).
- Párrafos de tres a seis frases en los textos largos (cada guía da su medida). Negritas con mesura:
  dos o tres ideas en un texto largo.
- Enlaces en Markdown (`[texto](url)`); en los textos para avisos y redes, texto plano (lo dicen sus
  guías).
- **Nunca «hoy», «ayer» ni «esta semana»**: la fecha o el día («el jueves 12»). El número sale el día
  siguiente a las conversaciones y queda en la hemeroteca; lo que se guarda para otro día (la reserva,
  «Hace un año» escrito por adelantado) tampoco dice «acaba de».

## Gráficos

- **Un gráfico, solo cuando explica algo que el texto no deja ver de un vistazo**: tres o más cifras comparables
  de la misma fuente (los resultados de un estudio, una encuesta, una evolución en el tiempo). No para adornar ni
  para una o dos cifras, que se dicen en el texto.
- **Lo dibuja el programa del diario a partir de los datos** (el campo `grafico` del artículo o del apartado del
  reportaje, ADR 0084), nunca un agente a mano: barras horizontales (`barras`, para comparar), columnas
  (`columnas`, para pocas categorías con etiquetas cortas) o líneas (`lineas`, para una evolución).
- **Los datos, exactos y de una sola fuente**: los mismos valores que da la fuente, con su precisión, y la misma
  unidad para todos. Las barras empiezan siempre en cero (el programa lo hace solo); nada de mezclar en un gráfico
  cifras de fuentes distintas.
- **Título que dice qué se mide**, no la conclusión («Redacciones humanas que los detectores tomaron por IA»), y
  etiquetas cortas.
- **La fuente, siempre**, enlazada; y en la nota, lo que hace falta para leerlo bien: cuántas personas o casos, de
  dónde y cuándo, y si los datos son de la propia empresa («según la empresa»).

## Las traducciones

Cada edición se traduce al catalán, al gallego, al euskera y al inglés, con el mismo criterio que el
castellano y en el registro natural de cada lengua, no calcado. Cómo se hace en cada lengua (norma,
dónde consultar, formatos, vocabulario de la IA y lo propio de España) está en el libro del traductor,
`encargos/traduccion.md`.

## Correcciones

- Un error se corrige sin esperar a que nadie lo pida, en el mismo artículo y en los cinco idiomas, con
  su nota al final (ADR 0055): «Corregido el…» (había un error), «Actualización del…» (el dato era
  cierto y ha cambiado) o «Nota añadida el…» (faltaba algo). Una errata que no cambia el sentido se
  corrige sin nota.
- Si el error estaba en el titular, en los avisos o en las redes, la corrección llega también allí.
- No se retira un artículo entero si basta con cambiar una parte.

## Lo que se comprueba sin IA

Unos programas repasan cada noche algunas de estas normas (ADR 0056, 0059 y 0067), pero no sustituyen
al revisor:

- `scripts/revisar-estilo.py`: el «quien» relativo, las citas solo en inglés y las normas de vocabulario y
  forma que se pueden buscar («hoy», «pieza», «el diario cuenta», «app», el condicional de rumor, el
  porcentaje); lo que encuentra lo corrige un agente.
- `scripts/comprobar-corrector.py`: que el corrector de estilo, un agente que repasa cada noche la
  redacción de los artículos del día, no ha cambiado ningún dato.
- `scripts/corregir-erratas.py`: «e» ante «i», «u» ante «o», las comillas españolas en inglés, y avisa
  de los titulares de más de 90 caracteres.
- `scripts/revisar-idiomas.py`: castellano que se ha colado en una traducción.
- `scripts/revisar-autoria.py`: lo que se atribuye a un autor del diario y es de otra cuenta.
