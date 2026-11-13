# 57. El resumen del vídeo semanal de cada grupo, traducido

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

Cada lunes el boletín semanal deja en `multimedia/AAAA-WW.json` el vídeo y el pódcast de NotebookLM de cada
grupo y unas 70 palabras, en castellano, sobre lo que cuenta el vídeo (ADR 0034). En las ediciones en
catalán, gallego, euskera e inglés ese resumen salía en castellano; desde el ADR 0056 iba al menos marcado
como castellano y con una línea que lo decía. Traducirlo quedó entonces como posibilidad, porque llega
fuera de la redacción nocturna y pide un paso con agentes los lunes.

Juanjo, 13-11-2026, sabiendo que el vídeo y el pódcast seguirán en castellano: que se traduzca.

## Decisión

- **Un traductor por idioma (Sonnet) traduce el resumen de cada grupo** cuando llega o cambia el archivo de
  la semana: `scripts/multimedia-traducir.sh`, que lanza `publicar-web.sh` antes de montar la web, con el
  encargo `encargos/pasos/27-multimedia-traduccion.md` y el mismo mecanismo de las demás traducciones
  (`scripts/traducir.sh`, ADR 0026). La traducción vive en `multimedia-XX/AAAA-WW.json`, solo con el resumen
  de cada grupo.
- **Un programa, sin IA, la comprueba y apunta de qué texto salió** (`scripts/multimedia.py`): que estén
  todos los grupos, que no sea el castellano copiado y que el largo cuadre; si no vale, la quita. Si vale,
  guarda en `origen` el resumen en castellano del que salió cada uno.
- **Solo vale la traducción del texto de ahora**: el boletín cambia el archivo después de dejarlo (el
  09-11-2026 lo cambió dos veces en una mañana). `generar.py` usa la traducción de un grupo solo si su
  `origen` es el resumen actual; si no, vuelve a enseñar el castellano, marcado y dicho como antes, y la
  semana vuelve a estar pendiente. Solo se traduce lo pendiente: las semanas y los idiomas sin traducción al
  día.
- **Con el resumen traducido desaparece la línea «Resumen, vídeo y pódcast en castellano»** de ese grupo: la
  cabecera del bloque ya dice que el pódcast y el vídeo están en castellano.

## Alternativas descartadas

- **Dejarlo en castellano con su aviso** (lo que había): era honesto, pero la página de la semana quedaba a
  medias en cuatro ediciones.
- **Traducirlo en la redacción nocturna**: el archivo llega el lunes por la mañana, con el número ya
  publicado; esperar a la noche lo dejaría un día en castellano.
- **Publicar primero y traducir después, en segundo plano**: dos publicaciones seguidas de la web y un
  proceso con agentes suelto, que podría coincidir con la redacción. Hecho en `publicar-web.sh`, el reloj
  espera a que acabe y no lanza nada más mientras tanto.
- **Guardar una huella del texto en lugar del texto**: el resumen es corto, y con el texto se ve de qué
  salió cada traducción sin calcular nada.
- **Que el traductor copie el resto del archivo** (enlaces del vídeo y del pódcast): serían dos copias de
  los mismos datos que podrían no coincidir. Los enlaces se leen siempre del original.

## Consecuencias

- Cuatro agentes cortos más cada vez que llega o cambia el archivo de la semana, de dos en dos; cada uno
  tiene 8 minutos como mucho y hay dos intentos. Mientras tanto el reloj del NAS no hace otra cosa: la web
  con el vídeo de la semana sale unos minutos más tarde que antes.
- La nota de git de esos commits ya no dice «Sin IA»: dice qué parte hace un modelo y cuál.
- Lo traducido lo vigila la comprobación nocturna de castellano colado (ADR 0056), porque ya no va marcado
  como castellano.
- Si un idioma falla, su edición enseña el resumen en castellano y lo dice. No impide publicar.

## Evidencia

- `git log -- multimedia`: el archivo de la semana 2026-45 llegó el lunes 09-11-2026 a las 8:51 y cambió a
  las 12:52.
- `generar.py`, `bloque_notebook()`: la cabecera del bloque lleva «Están en castellano» (`nb_es`) en las
  ediciones traducidas.

## Riesgos y limitaciones

- La traducción es automática y sale sin que nadie la lea antes: llega con el número del día ya revisado.
  La comprobación solo descarta errores de bulto.
- Si el archivo llega mientras se prepara o se publica el número, espera a que esté fuera, como ya hacía
  (ADR 0034).
- El resumen traducido dice lo que cuenta un vídeo que está en castellano: quien no lo entienda sabrá de
  qué trata, pero no podrá seguirlo.

## Validación

- Sin IA, con una traducción de pega: la comprobación la da por buena y apunta `origen`; al cambiar una
  cifra del resumen en castellano, ese grupo vuelve al castellano con su aviso y la semana vuelve a estar
  pendiente; una traducción con el castellano copiado o sin un grupo se quita.
- En el NAS, el 13-11-2026, con la semana 2026-45: `publicar-web.sh` tradujo los tres resúmenes a los cuatro
  idiomas y publicó la web en 1 minuto y 45 segundos; `multimedia.py pendientes` no deja nada. Comprobado
  en la web pública que las cuatro ediciones enseñan el resumen en su lengua, sin la línea de aviso.
- Leídas las doce traducciones: dos errores de sentido, corregidos a mano («sociolingüística» traducida al
  gallego como «socioloxía da linguaxe»; en inglés, «exporting Gemini to Google Sites» por exportar desde
  Gemini). El encargo pide desde entonces no cambiar un término por otro parecido.
