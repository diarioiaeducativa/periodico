# Encargo común: enlaces en el texto

Vale para todo el que escribe en el diario (redacción, Biblioteca, Repositorio y reportaje) y
para quien lo revisa. Quien lee un nombre tiene que poder ir a él ahí mismo, sin bajar hasta las
fuentes del pie.

## Las fuentes, donde se nombran

- **Lo que se nombra se enlaza donde se nombra**: la primera vez que el texto menciona un
  documento, artículo, herramienta, web o anuncio que está en `fuentes`, va enlazado ahí, con su
  nombre como texto del enlace: `lo explica en el artículo «[Agentes de IA que aprenden mientras
  duermen](https://educacion.bilateria.org/agentes-de-ia-que-aprenden-mientras-duermen)»`.
- Solo la primera mención, y una vez cada fuente. Lo que el texto no nombra no se enlaza.
- `fuentes` sigue al pie con todas, también las enlazadas en el texto.

## Los documentos que se nombran

Un anuncio, una noticia o un mensaje que habla de un documento publicado (una guía, un informe,
una norma) no basta: el lector quiere el documento.

- **Se busca el documento y se enlaza su página oficial** en la primera mención, con su título
  como texto del enlace, y va también a `fuentes`. Si no se ha podido leer, se dice, pero el
  enlace va igual: el lector sí puede leerlo.
- **Si está en la Biblioteca digital de ChatGPT-IA-edu**, se dice y se enlaza también su
  mensaje: la redacción tiene la lista al final de su entrada, con la fecha y el enlace de cada uno.
  Atención a las versiones: una guía actualizada es otro documento, con otra fecha.
- Si el documento todavía no está publicado (se presenta ese día, se anuncia para más adelante),
  se dice así, sin enlace inventado.

## Lo que el diario ya ha publicado

A medida que el diario crece, cada vez más temas continúan algo ya publicado: el lector tiene
que poder ir a ello.

- **Lo ya publicado está en `publicado.txt`**, cada pieza con su clave: `pieza:AAAA-MM-DD/id`.
- **`publicado.txt` solo tiene titulares: para saber qué se ha publicado, el buscador del diario.** Tienes
  la herramienta `mcp__diario__buscar`, que busca en el texto entero de todo lo publicado (piezas, breves,
  Biblioteca, Repositorio, reportajes y «Hace un año»), sin distinguir tildes ni mayúsculas y con las
  variantes de cada palabra; si un nombre no sale, prueba con los parecidos. Úsala siempre:
  - **antes de presentar a una persona, una herramienta, un proyecto o un sitio web**, con su nombre (y con
    el apellido solo, o el nombre del sitio). Lo que digas de lo que ya contó el diario tiene que ser
    completo: si ha salido varias veces, se dice y se enlazan las piezas, como mucho tres; las demás se
    resumen («además de…»). Nunca «lo contó en un breve» si también salió en otras piezas;
  - **antes de escribir sobre un tema**, con `parecidas` y el titular y la entradilla que piensas escribir:
    si sale una pieza que ya cuenta lo mismo, la tuya no se escribe o se queda en lo nuevo y la enlaza.
- **Enlaza lo que está claramente relacionado**: la pieza que contó el mismo producto, documento,
  recurso, anuncio o debate, o de la que lo tuyo es continuación. Compartir un tema general
  («la IA en la evaluación») no basta.
- **El enlace va en el texto, donde se menciona**, con esta forma:
  `[el informe del MIT que el diario contó el 2 de noviembre](pieza:2026-11-01/informe-mit-ia)`.
  El texto del enlace dice de qué trata, nunca «aquí» ni «este artículo».
- **La fecha de la clave no es la de publicación**: es la de las conversaciones, y el número
  sale al día siguiente. Si dices cuándo lo contó el diario, usa la fecha de publicación que
  `publicado.txt` pone en el encabezado de cada día (en el ejemplo, la clave es del 1 y la pieza
  salió el 2 de noviembre).
- Como mucho tres enlaces de este tipo por pieza y uno por breve. Solo claves que estén en
  `publicado.txt`, copiadas tal cual; el programa quita el enlace si la pieza no existe.
- **Lo nuevo de un tema ya publicado** (una respuesta, cómo se hace, un dato posterior) no es
  una pieza nueva: es un breve que cuenta solo lo nuevo y enlaza la pieza anterior.
