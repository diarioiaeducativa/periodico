# 55. Correcciones a la vista, quién responde y reglas de mesa de edición

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

El 13-11-2026 se examinó el diario entero (unas 110 piezas en castellano contra sus fuentes, las cuatro
ediciones traducidas, los servicios y el diseño) para saber si tenía nivel profesional. El dictamen: sí en
diseño, servicios, técnica y exactitud; todavía no en edición. Lo que faltaba no era reporterismo, sino lo
que hace una mesa de edición: decir cuándo se corrige algo, decir cuándo el diario habla de sí mismo, que
el titular no diga más que el cuerpo y recordar lo ya contado. Y en transparencia, cuatro cosas que la
página «La redacción» no decía: quién responde de lo publicado, cómo se corrige, quién lo revisa y quién lo
paga.

Dos hechos que el examen no conocía y que cambian sus propuestas (Juanjo, 13-11-2026):

- **Una persona revisa cada número antes de que salga** (la vista previa de las 5:00, ADR 0025). La página
  no lo decía: hablaba de agentes que «se revisan entre ellos» y de personas que lo «supervisan».
- **El diario lo hace y lo mantiene una sola persona, con sus medios**; la idea es de Raül Torres, que
  aporta de vez en cuando.

## Decisión

- **Un solo aviso de IA, en el pie, que vale para todo el diario**, y no uno al inicio de cada pieza:
  «Redactado con IA a partir de las conversaciones de los grupos y revisado por una persona antes de
  salir». Juanjo, 13-11-2026: «todo está hecho con IA; en todo caso un mensaje que sirva para todos, pero
  que no moleste al leer».
- **«Las personas» dice quién responde**: quién ideó el diario, quién lo mantiene, que revisa cada número
  antes de que salga y responde de lo publicado, que los dos participan en los grupos que el diario
  cuenta y que no hay publicidad ni patrocinio.
- **Política de correcciones**, en un apartado nuevo de «La redacción»: cuando se corrige un dato, la
  pieza lo dice al final con la fecha y lo que cambió; una errata que no cambia el sentido se corrige sin
  nota. En los datos, el campo `correccion` (el texto de la nota) y `corregido` (el día, `AAAA-MM-DD`),
  que pasa a los datos estructurados como fecha de modificación (ADR 0039). El reportaje también la
  admite. Tres fórmulas: «Corregido el…» (había un error), «Actualización del…» (el dato era cierto y ha
  cambiado) y «Nota añadida el…» (falta algo que el lector debe saber).
- **Reglas nuevas en los encargos** del redactor y de los revisores (`encargos/redaccion.md`,
  `pasos/1-repaso.md`, `pasos/13-biblioteca-repaso.md`, `encargos/reportaje.md`, `pasos/9-reportaje-repaso.md`):
  - el titular y la entradilla no dicen más que el cuerpo ni que la fuente, y lo que anuncia una empresa
    lleva sus condiciones (plan, precio, plazo);
  - lo que no es de estos días lleva su fecha en el titular;
  - antes de escribir sobre un asunto ya tratado se leen las piezas anteriores;
  - si la pieza trata del propio diario, lo dice;
  - el crédito de un recurso lleva el nombre que consta en el recurso o el nombre completo de quien lo
    publica: un nombre de pila no se completa con un apellido;
  - nadie acapara el número: como norma, una pieza por persona y dos por producto o empresa. Es una regla
    del redactor, no un tope del programa, para no falsear un día que de verdad gira en torno a un asunto;
  - en la Biblioteca, las enumeraciones se cuentan en el documento y coinciden en el texto y en el dibujo.
- **El molde de la viñeta también varía** (amplía el ADR 0024): el resumen que leen el guionista y el juez
  (`vineta.py --recientes`) dice quién dijo la última frase y con qué cara acabó cada personaje, y avisa
  cuando el mismo ha rematado dos números seguidos.
- **Las dos últimas palabras de un titular solo se unen si juntas caben en una línea del móvil**
  (`sin_viuda()`, ADR 0045): unidas, dos palabras largas no cabían y el navegador partía la última por
  una letra. Pasaba en 25 titulares ya publicados.
- **Al traductor**, los tropiezos repetidos de cada lengua (`scripts/idiomas.py`): en inglés el diario es
  «the paper», no «the diary», y lo que en origen se dijo en inglés se copia de la fuente; en catalán,
  «soc» y las etapas en minúscula; en gallego, el género y los castellanismos más frecuentes.

Se corrigieron además 17 piezas publicadas, en los cinco idiomas, cada una con su nota.

## Alternativas descartadas

- **Un aviso de IA al inicio de cada pieza**, como proponía el examen apoyándose en el artículo 50 del
  Reglamento europeo de IA. Ese artículo exime del aviso cuando el texto pasa por una revisión humana y
  una persona tiene la responsabilidad editorial, que es el caso; y repetido en cada pieza estorba la
  lectura sin decir nada que el pie no diga.
- **Decir que ninguna persona revisa antes de publicar**, que el examen daba por hecho: no es cierto.
- **Un tope por persona y por producto aplicado por el programa**: un número fijo dejaría fuera noticias
  de un día monotemático o haría rellenar con piezas flojas.
- **Corregir también los hallazgos leves** (unos 45: giros poco naturales, matices de redacción) en
  números ya publicados: no cambian lo que el lector entiende.
- **Corregir sin comprobar** lo que el examen daba por erróneo: de ocho datos comprobados, uno estaba
  bien en la pieza (el plazo de los Gems de Google en educación, «verano de 2027», coincide con la ayuda
  de Google Workspace: «no sooner than June 1, 2027»).
- **Tocar lo que añadió la revisión manual**: la entradilla de la pieza sobre la autorización de las
  familias (07-11) lleva una nota de la redacción que dice que esos párrafos se añadieron a mano; se deja
  como está.

## Consecuencias

- Lo que afirma «La redacción» obliga: si un día el número sale sin esa revisión, la frase del pie deja de
  ser cierta ese día. La vista previa de las 5:00 es lo que la sostiene.
- Una pieza corregida cambia en los cinco idiomas a la vez; si no, las ediciones se contradicen.
- Los encargos son más largos. El redactor y el revisor leen ahora las piezas anteriores del mismo asunto,
  lo que añade lecturas a cada noche.

## Evidencia

- Artículo 50.4 del [Reglamento (UE) 2024/1689](https://www.boe.es/buscar/doc.php?id=DOUE-L-2024-81079):
  la obligación de informar no se aplica cuando el contenido «haya sido sometido a un proceso de revisión
  humana o de control editorial y cuando una persona física o jurídica tenga la responsabilidad editorial
  por la publicación del contenido».
- Datos comprobados el 13-11-2026 antes de corregir, cada uno en su fuente: la página «About» de
  MechSimulator (autor y publicidad); la ayuda de Anthropic sobre los artefactos (100 MB y 25.000
  registros en los nuevos, 20 MB en los anteriores al 16-09-2026) y sobre las ofertas de lanzamiento de
  Fable 5.2 (sin plan gratuito; en Pro, del 9 al 16 de noviembre); el PDF de las *Orientacions per a l'ús
  de la intel·ligència artificial als centres educatius* (las cinco razones, páginas 5 y 6); el PDF de
  *Tecnologies educatives al servei de l'aprenentatge* (tabla 2: nueve criterios); el resumen de Sonia
  Livingstone en Media@LSE (no contiene la fórmula que el titular le atribuía); los dos enlaces de
  Tongjiang Lab (404 y sin respuesta) y sus copias en la Wayback Machine.

## Riesgos y limitaciones

- No se ha podido comprobar si las *Orientacions* de 2026 están hoy en el repositorio oficial del
  Departament: lo protege una comprobación contra la lectura automática, que no se salta. La nota dice lo
  que sí consta: la página de la XTEC las da por «en desarrollo» y el enlace del que se descargaron dejó
  de existir, según se contó en el grupo.
- Las reglas de los encargos son instrucciones a agentes: reducen los fallos, no los impiden. No se ha
  medido todavía su efecto; se verá en los números siguientes.
- De los hallazgos medios del examen que dependían de una fuente no abierta por quien corrige (la
  publicación de «Buzz» en LinkedIn, las condiciones de edad de OpenAI), no se ha tocado nada.

## Validación

- `generar.py` sin errores en los cinco idiomas; `scripts/revisar-maqueta.js` sin avisos en «La redacción»
  (cinco idiomas), la portada y cuatro piezas corregidas, en Chromium y Firefox, ordenador, tableta y móvil.
- Vistos en pantalla los dos dibujos con el rótulo cambiado (en castellano, euskera e inglés), las notas
  de corrección y los titulares que antes se partían.
