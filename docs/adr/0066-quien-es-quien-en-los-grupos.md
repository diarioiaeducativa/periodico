# 66. Quién es quién en los grupos: por la cuenta, no por el nombre

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

En los grupos, el nombre visible no distingue a las personas. El 11-11-2026 un miembro de Vibe Coding
Educativo que firma «Juanjo» compartió Eduvers, una web de simulaciones de Física y Química. El diario la
atribuyó a Juan José de Haro, que en los grupos firma «Juanjo de Haro»: en la pieza del 11-11 (corregida el
13-11, ADR 0055), en su aviso del 12-11 en el grupo y en el carrusel de Instagram de ese día, y otra vez en
el borrador del reportaje del 14-11, corregido antes de publicarse a petición de Juanjo («dice que eduvers es
mío y no es cierto»).

La causa: el material que leen los agentes (`preparar.py`, `semana.py`, `hace_un_ano.py`, el buscador de
mensajes y las presentaciones del repositorio) solo llevaba el nombre visible, y los encargos decían que
Juan José de Haro «firma Juanjo en los grupos». Así, cualquier «Juanjo» se tomaba por él. La corrección del
13-11 arregló el texto, pero no la causa. El problema no es solo suyo: en los tres grupos hay 51 nombres
visibles que usan cuentas distintas.

## Decisión

- **El material marca a cada persona por su cuenta** (`scripts/personas.py`). Cada mensaje del bot trae
  `autor_id`, el número fijo de la cuenta de Telegram. A los autores del diario se les marca
  `Juanjo de Haro [autor del diario: Juan José de Haro]`; a quien comparte nombre visible con otra cuenta,
  `[@usuario]` o, sin usuario, `[cuenta N de «Nombre»]` (N, por el orden de su primer mensaje). Lo usan
  `preparar.py` (y con él `semana.py` y `hace_un_ano.py`), `buscar_mensajes.py` y `repositorio.py`.
- **Los números de cuenta de los autores no van en el repositorio, que es público**: están en
  `~/.config/diario-autores.json` del contenedor (`{"<autor_id>": {"nombre": …, "en_grupos": [...]}}`). Las
  marcas tampoco: el material (`dias/`, `semanas/`…) no se sube.
- **Los encargos** (redacción, reportaje, biblioteca, repositorio) dicen que Juan José de Haro y Raül Torres
  son solo los mensajes con la marca `[autor del diario: …]`, y que otro «Juanjo» o «Raül» es otra persona.
- **Una comprobación sin IA** (`scripts/revisar-autoria.py`), en `noche.sh` antes de traducir la edición y
  escribir los avisos. Busca las frases que nombran a un autor del diario y tienen al lado (a 45 caracteres
  como mucho, sin otro nombre propio en medio) un recurso que en los grupos solo han compartido otras cuentas
  (por su enlace o por su nombre: «Eduvers» por eduvers.org), o un enlace a un mensaje de otra cuenta con su
  mismo nombre de pila. También avisa de la pieza que nombra a un autor y cuyos mensajes enlazados son de
  otra cuenta con su nombre de pila, sin ninguno suyo. Si encuentra algo, el verificador de autoría
  (`encargos/pasos/28-autoria.md`, Sonnet) lo comprueba y lo corrige en todos los idiomas. Se repite tras la
  traducción y los avisos, y lo que quede se le dice a Juanjo por Telegram, antes de la vista previa.

## Alternativas descartadas

- **Solo cambiar los encargos**: sin la marca, el agente no tiene con qué distinguir a dos personas.
- **Poner el número de cuenta de todos en el material**: no hace falta para quien tiene un nombre único, y
  llena el material; basta con marcar a los autores y a quien comparte nombre.
- **Parar el número si la comprobación salta**: es una regla aproximada, y el número sale siempre (ADR 0021).

## Consecuencias

- Una persona nueva que comparta nombre visible con otra cambia la marca de las dos, pero solo la de la
  cuenta nueva lleva el número más alto: las anteriores conservan el suyo.
- Si se suma otro autor al diario, se añade a `diario-autores.json` en el NAS.
- Lo que se haya escrito con la confusión antes de este día se corrige a mano (ADR 0055).

## Evidencia

- Mensajes del bot: `vce` 14858 (`autor` «Juanjo», sin usuario, otra cuenta) y 14905 (`autor` «Juanjo de Haro»,
  `usuario` jjdeharo), en `/bot-datos/vce/mensajes.jsonl`.
- Nombres visibles con más de una cuenta en los tres grupos, el 15-11-2026: 51 (entre ellos Antonio, Carlos,
  David, Javier, con seis cuentas, y 40 cuentas sin nombre).

## Riesgos y limitaciones

- La comprobación solo ve los recursos que se han compartido en los grupos con su enlace, y no entiende la
  frase: puede callar una atribución errónea escrita de otra forma, o señalar una correcta (por eso la
  revisa un agente en vez de corregirse sola).
- Sin `diario-autores.json`, el material solo distingue los nombres repetidos y la comprobación no hace nada
  (lo dice en el registro).

## Validación

- Sobre todo lo publicado hasta el 15-11-2026 (secciones y avisos, cinco idiomas), solo señala el aviso del
  12-11 («Eduvers, de Juan José de Haro, reúne…»), que es el error real. Las primeras versiones de la regla
  daban unas cuarenta falsas alarmas: palabras corrientes que coinciden con una web («diario», diario.red),
  listas con un recurso de cada persona, el enlace a la web de Raül en una frase que nombra a los dos y la
  lista de lo descartado (que no se publica). Se quitaron con la cercanía, las mayúsculas y la frecuencia
  de la palabra en los grupos.
- Señala el error en los dos borradores del reportaje del 14-11 y en la versión de la pieza del 11-11
  anterior a su corrección (commit 09d8c88).
- `preparar.py` del 11-11 marca «Juanjo de Haro [autor del diario: Juan José de Haro]» y deja al otro
  «Juanjo» sin marca.
