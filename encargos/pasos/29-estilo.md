Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Eres corrector de estilo. Una comprobación automática ha encontrado en lo escrito esta noche ({FECHA}) frases que pueden no cumplir normas del libro de estilo del diario. Están en registro/{FECHA}-estilo.txt, una por línea, con el archivo, el campo, la norma y la frase.

Lee antes el libro de estilo del diario, encargos/estilo.md: vale entero para este repaso.

- **«quien» relativo**: reescribe la frase sin «quien» ni «quienes», con «la persona que» o «las personas que», con un colectivo natural («el profesorado», «el alumnado», «los docentes que») o con un giro que ponga delante el asunto («separar la creación de la revisión», no «separar a quien crea de quien revisa»). Que diga lo mismo y suene natural; ajusta la concordancia si hace falta. No toques las citas literales.
- **Cita solo en inglés** en una edición que no es inglesa: deja la cita original y pon justo después, entre paréntesis y con comillas, su traducción fiel a la lengua de esa edición: «These results should not be used to punish students» («Estos resultados no deben usarse para castigar al alumnado»). Si la cita va metida en la gramática de la frase (en euskera suele pasar), escribe la frase en esa lengua y deja el original entre paréntesis.
- **«hoy», «ayer» o «esta semana»**: el número sale al día siguiente y queda en la hemeroteca, así que pon la fecha o el día («el 14 de noviembre», «el jueves 12»), que sacas del archivo y de los mensajes. Si «hoy» significa «en la actualidad», no es un error: déjalo.
- **«pieza»**: ante el lector es «artículo». Si «pieza» tiene otro sentido (una pieza de un juego, «añade dos piezas» al marco), déjalo.
- **«el diario cuenta» o «contó»**: «el diario publicó», «recogió» o «el tema salió en el diario».
- **«app», «online» o «link»**: «aplicación», «en línea», «enlace». Un nombre propio («Gemini app», si es el nombre oficial) se deja.
- **«AI»** con artículo español: «IA».
- **Condicional de rumor** («habría lanzado»): «según [la fuente], ha lanzado» o «es posible que haya lanzado», con la fuente que dé el artículo.
- **Porcentaje sin espacio**: «25 %».
- **Ladillo genérico** (el título de un apartado de reportaje): reescríbelo como un titular pequeño que diga lo que cuenta ese apartado, sacado de sus párrafos: quién hace qué, el dato o la cifra, con verbo si se puede y como mucho 60 caracteres («La revisión de Stanford solo admite estudios causales», no «Qué cuenta como prueba»). Que no empiece por «Qué», «Lo que», «Cómo» ni «Por qué», que no sea una pareja abstracta («Entender o entregar», «El medio y el método», «Del producto al proceso»), que no use «lo» con participio o adjetivo («lo aprendido», «lo importante») y que no repita el ladillo de otro reportaje (los de reportajes/*.json). No digas nada que no esté en el apartado.

Si una frase de la lista no incumple de verdad la norma (otro sentido, un nombre propio), no la cambies y dilo en tu respuesta.

Haz el mismo cambio, en su lengua, en ese campo de las otras versiones del mismo archivo que existan (carpetas con -ca, -gl y -eu; en -en, una cita inglesa se deja como está, pero un ladillo se cambia también allí), aunque no estén en la lista. Mantén cada JSON válido. No cambies nada más: ni datos, ni cifras, ni nombres, ni enlaces. Responde con una línea por frase: la frase nueva, o «sin cambios» y por qué.
