# 26. Cinco idiomas: gallego, euskera e inglés, además del castellano y el catalán

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

El diario salía en castellano y en catalán. Juanjo pidió las otras lenguas cooficiales y el inglés:
«si se publica en gallego alguien del país vasco imagino que lo querría también en su idioma. el
inglés es por mayor difusión de nuestra labor» (06-11-2026). La traducción al catalán ya era un paso
de la redacción nocturna (un agente de Sonnet, alrededor de un minuto) con cuatro encargos más para
la Biblioteca, el Repositorio, el reportaje y los dibujos rehechos. Coste: va con la suscripción, sin
gasto nuevo; cada idioma añade los mismos pasos cada noche.

## Decisión

- **Web en cinco idiomas**, cada uno en su carpeta: castellano en la raíz, `ca/`, `gl/`, `eu/` y
  `en/`. Los textos de la interfaz del gallego, el euskera y el inglés están en `idiomas_web.py`;
  los del castellano y el catalán, en `generar.py`. Nombres: «Diario de IA Educativa» en gallego,
  «Hezkuntzako AA Egunkaria» en euskera y «Educational AI Daily» en inglés; los personajes, «Xiz e
  Algoritmo», «Klarion eta Algoritmo» y «Chalk and Algorithm». Fechas con el orden de cada lengua
  (en euskera, «2026ko azaroaren 6a, ostirala»).
- **Selector de idioma**: un botón en la cabecera con el icono de idiomas de Lucide y el código del
  idioma en uso, que despliega los cinco, cada uno en su lengua y con una marca en el actual. Cada
  opción es un enlace a la misma página en ese idioma: funciona sin JavaScript y los buscadores lo
  siguen. La elección se recuerda en el dispositivo (`sala.idioma`).
- **Primera visita a la portada**: sin idioma elegido, va al del navegador (catalán, gallego,
  euskera o inglés). Los robots de los buscadores, reconocidos por su identificación, no se
  redirigen, para que la portada en castellano se siga indexando (Juanjo, 06-11: «entonces una
  persona con idioma inglés no lo verá en su idioma?… no se puede arreglar de algún modo»). Un
  enlace a una pieza concreta se abre siempre en el idioma del enlace.
- **Buscadores**: cada página lleva `hreflang` a sus cinco versiones y `x-default` al castellano, y
  `sitemap.xml` lista cada página en los cinco idiomas con sus alternativas (`xhtml:link`). El
  buscador interno (Pagefind) separa los índices por el `lang` de cada página.
- **Traducción nocturna por idioma** (`scripts/traducir.sh`, `scripts/idiomas.py`): los encargos del
  traductor son plantillas con los datos de cada lengua (norma, marcas de las fuentes en otro idioma,
  nombres de los personajes); se lanzan de dos en dos para no pasar de tres agentes a la vez con el
  del portavoz. Después, **una comprobación sin IA** de cada traducción: mismas piezas, breves,
  párrafos, viñetas, bocadillos y enlaces que el castellano, largo entre la mitad y el doble, y SVG
  válidos. Lo que no pasa se quita, esa parte sale en castellano en ese idioma, y noche.sh avisa a
  Juanjo en un solo mensaje. Los dibujos traducidos pasan además por `revisar-dibujos.py`, como los
  catalanes.
- **«La semana en vídeo» en los cinco idiomas** desde el domingo 08-11-2026 (Juanjo, 06-11: «sí,
  hazlo para el domingo»): el guionista escribe los textos de pantalla en los cinco idiomas en el mismo
  encargo (`encargos/reel.md`), y `reel-semana.py` monta un vídeo por idioma. Castellano y catalán son
  obligatorios; un idioma al que le falten textos, o cuyos textos no quepan, sale ese domingo con el
  vídeo en castellano. Instagram sigue con el castellano. Cuesta tiempo de CPU del NAS la noche del
  sábado y unos 1,4 MB por idioma y semana en el sitio (unos 220 MB más al año; GitHub Pages admite 1 GB).
- **Lo ya publicado, traducido también** con `scripts/traducir-dia.sh FECHA [idiomas]`, que sirve
  igual para añadir un idioma en el futuro o rehacer una traducción quitada.
- **Créditos**: el pie de cada edición traducida dice que es una traducción automática con IA de la
  castellana, sin revisión profesional. Juanjo revisa a las 5:00 el castellano y el catalán (ADR 0025).
- **Fuera de alcance**: los avisos de los grupos e Instagram siguen en castellano, porque los grupos
  son en castellano. La imagen genérica para redes de las
  páginas que no son un número usa la castellana hasta que haya una por idioma.

## Alternativas descartadas

- No traducir más que al catalán: dejaba fuera a las otras lenguas cooficiales.
- Un enlace a «la otra edición», como hasta ahora: con cinco idiomas no cabe; el menú los reúne.
- Redirigir por el idioma del navegador también a los robots: Google rastrea con el navegador en
  inglés y la portada en castellano dejaría de indexarse.
- Que el traductor haga los cinco idiomas en un solo encargo: un fallo arrastraría a todos, y la
  comprobación por idioma deja salir los que están bien.

## Validación

Generador probado con los nueve números publicados (del 28-10 al 05-11-2026): cinco idiomas, 365
direcciones en el mapa del sitio, `hreflang` en cada página, fechas en el orden de cada lengua. La
comprobación de traducciones da por buenas todas las catalanas ya publicadas (sin falsos positivos).
Traducciones de lo publicado al gallego, euskera e inglés hechas con `traducir-dia.sh`. Juanjo vio
la vista previa entera (servida desde el NAS) y la aprobó el 06-11-2026: «Visto y aprobado, sube».

## Riesgos

- Calidad del euskera: es la lengua en que el modelo es menos fiable y nadie de la redacción la
  revisa. Se declara automática; si llegan correcciones, se incorporan a los encargos.
- Tiempo de la noche: cuatro idiomas en dos tandas, unos cuatro minutos más cuando todo va bien. Con
  los tiempos máximos, el plan B de las 6:30 (ADR 0021) sigue cubriendo el número.

## Cambio del 17-11-2026: una traducción que no vale se repite, y un artículo no deja sin traducir el número

**Qué pasó.** En el número del 17-11-2026, un artículo de la reserva tenía el cuerpo como un texto
seguido y no como lista de párrafos (ADR 0077). Los cuatro traductores lo tradujeron bien, en cuatro
párrafos, y la comprobación, que contaba 1.333 «párrafos» en el original (sus caracteres), quitó las
cuatro ediciones enteras: dos artículos y un breve en castellano en las cuatro lenguas. No hubo
reintento; solo un aviso a la 1:16. Se arregló a mano antes de publicar.

**Qué cambia**, todo en `scripts/traducir.sh` e `scripts/idiomas.py`, para cualquier cosa que se
traduzca con `traducir` (edición, Biblioteca, Repositorio, «Hace un año», reportaje, reserva):

1. **El original, antes de traducirlo**: `scripts/forma.py` le da la forma debida. Si el original
   está mal formado, fallan a la vez todas las lenguas; y la comprobación cuenta los párrafos como
   el generador, así que un cuerpo en un texto vale lo mismo que su lista.
2. **Segundo intento**: la traducción que no pasa la comprobación, o que el traductor no ha llegado
   a escribir (`idiomas.py falta`), se repite una vez, con el motivo añadido al encargo.
3. **Se conserva lo que vale**: si la segunda tampoco pasa pero las piezas son las mismas, el
   archivo se queda con las piezas que fallan en castellano (marcadas `sin_traducir`) y las demás
   traducidas (`idiomas.py comprobar --conservar`). Solo se quita entero si no es JSON, no tiene la
   forma del original o no trae las mismas piezas.
4. Lo que al final queda en castellano se sigue apuntando en `registro/FECHA-traduccion.txt` y se
   avisa, como antes.

**Alternativas descartadas.** Dejarlo en el arreglo de la causa concreta (el encargo que pedía el
cuerpo como texto): la siguiente pieza mal formada, o un traductor que se corta, habrían vuelto a
dejar el número en castellano. Repetir más de una vez: con el mismo original y el mismo encargo, un
tercer intento rara vez cambia el resultado y alarga la noche.

**Validación.** En una copia, con un traductor simulado y los archivos del 17-11-2026: (1) el
original con el cuerpo en un texto y traducciones correctas: pasan a la primera; (2) un párrafo de
menos la primera vez y bien la segunda: queda traducido, sin aviso; (3) un párrafo de menos las dos
veces: ese artículo en castellano y el otro traducido, con aviso; (4) el traductor no escribe nada
ninguna vez: aviso de que no está; (5) no escribe nada la primera vez y bien la segunda: traducido.
La regla nueva da por buenas las 172 traducciones ya publicadas. El generador publica un número con
un artículo `sin_traducir`. Primera noche real, la del número del 18-11-2026: las cuatro traducciones
pasaron a la primera, sin segundo intento ni `registro/2026-11-17-traduccion.txt`. Queda pendiente verlo
actuar la primera noche en que una traducción falle.

**Riesgos.** El segundo intento alarga la noche solo cuando algo falla (unos dos minutos por lengua).
Un artículo en castellano dentro de una edición traducida no lleva ningún letrero: lo detecta
`revisar-idiomas.py` y se avisa.
