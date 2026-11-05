# Encargo común: enlazar lo que el diario ya ha publicado

Vale para todo el que escribe en el diario (redacción, Biblioteca, Repositorio y reportaje) y
para quien lo revisa. A medida que el diario crece, cada vez más temas continúan algo ya
publicado: el lector tiene que poder ir a ello.

- **Lo ya publicado está en `publicado.txt`**, cada pieza con su clave: `pieza:AAAA-MM-DD/id`.
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
