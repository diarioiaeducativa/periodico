# 91. Las horas, con su huso

Fecha: 2026-11-18 · Estado: aceptado

## Contexto

Juanjo pidió que, cuando el diario habla de horas, diga el huso horario «o lo más apropiado, ya que se lee en
todo el mundo». Las horas salían sin él: en la web, «Sale cada mañana a las 7:00» (solo el inglés decía «Spanish
time») y el anuncio de la app («aviso opcional a las 7»); en «Cómo se hace», la tabla del horario; y en los
artículos, el del 13-11-2026 daba las sesiones de una jornada del INTEF «a las 10:30» y «a las 13:30». El libro de
estilo y el del traductor fijaban cómo se escribe una hora en cada lengua, pero no pedían el huso.

## Decisión

- **Hora local con su desfase respecto a UTC**, que cualquier lector puede pasar a su hora sin que la web tenga
  que calcularla en su navegador. Las de España, «hora peninsular española (UTC+1)»: «peninsular», porque
  Canarias va una hora por detrás, y «española», porque mucha gente de los grupos lee desde Latinoamérica.
- **En la web, el desfase se calcula cada día** (`huso()` en `generar.py`, a partir de `hora_de_salida()`):
  UTC+1 en invierno y UTC+2 en verano, sin tocar nada al cambiar la hora. Lo llevan la entradilla de «La
  redacción», que es también la descripción de la página, y el anuncio de la app, en las cinco lenguas: «hora
  peninsular espanyola» en catalán, «hora peninsular española» en gallego, «Espainiako penintsulako ordua» en
  euskera y «CET» o «CEST» en inglés, con la hora a su manera («7am»).
- **Una vez por texto**: en «La redacción» va en la entradilla y no se repite en el resto de la página; en «Cómo se
  hace», en la primera hora y en una frase sobre la tabla del horario.
- **Los artículos**: norma nueva del libro de estilo (`encargos/estilo.md`), «Toda hora, con su huso». La de
  España, con su huso; la de fuera, con la de origen y la equivalente en España («a las 10:00 de California
  (19:00 en la España peninsular, UTC+1)»). Si un texto da varias horas del mismo sitio, el huso va la primera
  vez. El libro del traductor (`encargos/traduccion.md`) da la forma de cada lengua.
- **Lo ya publicado se queda como está**: la norma vale desde ahora.

## Pendiente

Los textos de la propia app de Android («cada mañana, a las 7») no cambian hasta su próxima versión, que pasa por
la revisión de Google Play.

## Validación

`generar.py` montado en el NAS el 18-11-2026: la entradilla y el anuncio salen con el huso en las cinco lenguas,
sin ningún `{huso}` sin sustituir. `huso()` da UTC+1 el 28-03-2026 y el 25-10-2026, y UTC+2 el 29-03-2026 y el
01-07-2026 (los días del cambio de hora, con las 7:00 ya pasado el cambio). `scripts/revisar-maqueta.py` a las
nueve anchuras: sin huecos.
