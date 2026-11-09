# 33. Contador de visitas sin datos de quien lee

Fecha: 2026-11-08 · Estado: aceptado

## Contexto

El diario no tenía ninguna forma de saber cuánta gente lo lee: GitHub Pages no da visitas y sus
estadísticas de tráfico solo cuentan las del repositorio. Raül Torres propuso un contador «aunque sea
interno» (08-11-2026), y Juanjo lo aceptó con dos condiciones: que no recoja datos de ningún tipo y que
sirva para ver qué páginas se leen más y cuántas visitas recibe el diario, no cuántas personas distintas.
Él mismo propuso cómo: que el navegador lleve la cuenta de lo que ha visto y que una visita vuelva a
contar tras un rato sin actividad. Quiso además las cifras al momento, en una página privada para los
dos autores.

Contar personas distintas exige reconocerlas (una marca guardada o la IP), y eso se descartó. Para lo
que sí se cuenta, la guía de la AEPD [*Uso de cookies para herramientas de medición de
audiencia*](https://www.aepd.es/guias/guia-cookies-analiticas-externas.pdf) (enero de 2024) exime de
consentimiento la medición que hace el propio editor, solo para estadísticas anónimas, sin ceder datos
a terceros, página por página y agregada, informando de ello. Para lo guardado en el navegador pide una
vida útil limitada «como es el caso de una duración de trece meses, y que no se extenderá
automáticamente en nuevas visitas» (apartado III.A, «Garantías mínimas», garantía 2, p. 4): los 13 meses
son el ejemplo que pone, lo esencial es que no se renueve sola. Los datos, «durante un período máximo de
veinticinco meses» (garantía 3, p. 4).

## Decisión

- **El navegador lleva la cuenta** (`CONTADOR` en `generar.py`, en la cabecera de todas las páginas
  salvo la 404). Guarda en `localStorage` (`diario.visita`) la hora de la última página abierta y la
  lista de las ya contadas. Si han pasado más de 30 minutos sin abrir ninguna, empieza una visita
  nueva y la lista se vacía. Cada página que no está en la lista suma una apertura. Las pestañas
  comparten la cuenta. Juanjo propuso entre media hora y una hora; se tomaron 30 minutos, la medida
  habitual de una sesión, para que las cifras se puedan comparar con otras webs.
- **La cuenta de la visita caduca a los 13 meses** de guardarse por primera vez, la duración que pone
  de ejemplo la AEPD (garantía 2), y las visitas nuevas no la alargan (`CADUCIDAD` en `generar.py`, el
  primer script de cada página, añadido el 09-11-2026). `diario.desde` apunta cuándo se guardó;
  pasados 13 meses se borran `diario.visita` y la propia fecha, y se empieza de cero. Si en ese momento
  hay una visita en curso, se conserva, para no contarla dos veces: el recuento no cambia. Se eligió
  esta forma y no borrar la visita a los 30 minutos porque una página web no puede borrar nada mientras
  no está abierta: lo de la última visita se quedaría igualmente hasta la siguiente. **El tema y el
  idioma no caducan**: son preferencias de quien lee, y la guía solo pide la caducidad para la medición
  (el mismo día se probó a hacerlos caducar también, y Juanjo lo descartó). Tampoco la marca de los
  autores (`diario.nocontar`): solo está en sus navegadores y la quitan ellos.
- **Al servidor solo llega la suma**: con `navigator.sendBeacon`, la ruta de la página, si empieza una
  visita y el título, para mostrarlo en el panel. Nada de IP, navegador ni identificador.
- **No se cuentan** los robots (por el agente de usuario, en el navegador y en el servidor), los
  navegadores automatizados (`navigator.webdriver`, también las pruebas con Playwright), la portada que
  salta a otro idioma (`window.SALTO`) ni los navegadores marcados con `?nocontar=1` (`?nocontar=0`
  lo deshace), para que los autores no cuenten sus propias visitas. La marca la pone el panel: la
  primera vez que un autor lo abre en un navegador, salta a `redaccion.html?nocontar=1&volver=1` del
  diario, que guarda la marca y vuelve al panel (`?marcado=1`), y el panel recuerda que ese navegador
  ya está marcado. Hace falta el salto porque una web no puede escribir en la memoria de otra, ni
  desde un marco, que los navegadores separan. La vuelta es fija, al panel, para que nadie use el
  salto para llevar a otra web; se salta desde una página sin cambio de idioma, para que la portada
  no se adelante, y si el navegador no deja guardar nada no se salta, para no entrar en un bucle.
  Juanjo pidió que fuera automático (08-11-2026), y que el pie del panel conservara el enlace manual
  para marcar a mano otro navegador. Los navegadores en los que
  los autores leen el diario sin abrir nunca el panel siguen contando. El widget para otras webs
  (`insertar.html`, ADR 0032) no lleva contador: se ve dentro de webs ajenas.
- **El servidor es el hosting de IONOS** (`https://bilateria.org/app/diario-ia-educativa/`, código en
  `ionos/estadisticas/`): siempre encendido y sin abrir la red de casa a los lectores. `contar.php`
  solo acepta peticiones cuyo origen es el diario, y valida la ruta. Guarda un archivo por día UTC
  (`data/AAAA-MM-DD.json`) con las sumas por hora: visitas y aperturas de cada página. Por hora y en
  UTC para que el panel reparta los días en hora de España sin que el cambio de hora los descuadre. El
  archivo se lee y se escribe dentro de un mismo bloqueo, para que dos visitas a la vez no se pisen.
  `data/` no se puede leer desde la web.
- **Pasados 25 meses queda solo el total de cada año** (09-11-2026; Juanjo pidió guardar «las visitas
  totales anuales, no el detalle»). Con la primera visita de cada día (UTC), `mantenimiento()` suma a
  `data/totales.json` los días ya cerrados, por día y por año de España, y borra los archivos de más
  de 25 meses: de lo borrado queda el total de visitas y de páginas abiertas de su año, que no caduca.
  La garantía 3 de la guía limita a 25 meses «la información recopilada»; el total de un año es la
  estadística agregada que la medición produce, sin páginas ni horas. La guía no habla expresamente
  de los totales que se derivan de lo recogido: es la lectura que se hace aquí. Cada día se suma una
  sola vez: hasta qué día se ha sumado se guarda en el mismo archivo que las sumas, que se sustituye
  de golpe. Se suma hasta anteayer, por si una petición rezagada aún escribe en el de ayer; ayer y
  hoy se leen del detalle. Si `totales.json` no se entiende, no se suma ni se borra nada, para no
  perder los años: hay que repararlo a mano. Los totales por día sirven además para que el panel no
  tenga que leer cientos de archivos.
- **El panel** (`index.php`) pide usuario y contraseña, uno para cada autor (`config.php`, solo en el
  hosting, con `password_hash`), para poder quitar el acceso a uno sin cambiar el del otro. La sesión
  es una cookie firmada de 90 días, solo para ellos. Cada uno cambia su contraseña desde el panel
  («Cambiar contraseña», a petición de Juanjo el 08-11-2026), que reescribe `config.php`; la firma
  de la sesión incluye la contraseña, así que al cambiarla se cierran las sesiones de los demás
  navegadores. Muestra las visitas de hoy, de 7 y de 30 días; la
  gráfica de visitas; y las páginas más abiertas y el reparto por idioma en el periodo elegido. Se
  pone al día cada minuto mientras está a la vista.
- **La gráfica se elige por horas, días, semanas, meses o años** (09-11-2026, a petición de Juanjo):
  las últimas 24 horas, los últimos 30 días, las últimas 12 semanas (de lunes a domingo, con el
  número de semana que usa el diario), los últimos 24 meses (los que están enteros dentro de los 25
  que se guardan) y todos los años; siempre desde el primer periodo con datos. Encima, el total de
  visitas y de páginas abiertas de lo que se ve; debajo, el detalle de la barra que se señala con el
  ratón o con el dedo y, si no se señala ninguna, el de la más reciente. Las fechas se pintan en hora
  de España esté donde esté quien mira. Las cifras van sobre todas las barras si caben; si no, solo
  sobre la más alta y la última.
- **Se dice en «La redacción»**, en los cinco idiomas: qué se cuenta, que no hay cookies ni datos de
  quien lee, cuánto se guarda (la cuenta de la visita en el navegador, 13 meses; las cifras, 25 meses, y después solo el total de cada año, con la guía de la AEPD
  enlazada, solo en castellano) y quién lo ve.

## Consecuencias

- Una persona que lee el diario por la mañana y vuelve por la tarde son dos visitas; quien borra los
  datos del navegador o usa una ventana privada vuelve a contar. Son visitas, no personas.
- Quien bloquea el `localStorage` no se cuenta.
- Las cifras empiezan el 08-11-2026; no hay datos anteriores.
- Al conectarse al contador, el navegador del lector se conecta al hosting, que ve su IP como la ve
  GitHub Pages al servir el diario; el contador no la guarda.

## Validación

- Lógica del navegador probada en Chromium, Firefox y WebKit, en escritorio y en móvil: primera página
  (visita y apertura), segunda página (solo apertura), recarga (nada), vuelta tras 31 minutos (visita
  nueva), `?nocontar=1` y `?nocontar=0`, y portada que salta (nada). El salto de ida y vuelta desde
  el panel, comprobado en la web publicada.
- Caducidad (09-11-2026), en Chromium, Firefox y WebKit, en escritorio y en móvil, en local y en la web
  publicada: la primera página guarda la fecha; una visita nueva no la cambia; pasados 13 meses se borra
  la visita y se empieza de cero, y el tema y el idioma elegidos siguen; si pasan en mitad de una visita,
  no cuenta otra; elegir el tema no guarda ninguna fecha.
- Envío real desde los tres navegadores con origen `diarioiaeducativa.github.io`: 204 y suma guardada.
  Sin el origen del diario no se guarda nada; `config.php` sale vacío y `data/` da 403.
- Panel comprobado con contraseña y sin ella (401), en escritorio y en móvil, con tema claro y oscuro.
  Los datos de prueba se borraron.
- Totales y gráfica (09-11-2026), en una copia local con dos años y medio de datos simulados (892
  días, 63.337 visitas): tras el mantenimiento quedan los 762 días de los últimos 25 meses, los
  totales de cada año son los mismos que antes de borrar, también el de 2024, cuyo detalle se borra en
  parte; una segunda pasada no cambia nada; una visita nueva sube el año en uno; con `totales.json`
  estropeado no se toca nada. Las cinco vistas, en Chromium, Firefox y WebKit, en escritorio, móvil y
  tableta, con tema claro y oscuro: sin errores, sin desbordamiento y sin rótulos que se pisen o se
  salgan. En el hosting (PHP 8.4), el mantenimiento escribe `totales.json`, que da 403 desde la web,
  y las cinco series devuelven las mismas sumas que el detalle de los dos días que hay.
