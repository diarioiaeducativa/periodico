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
- **Lo ya publicado, traducido también** con `scripts/traducir-dia.sh FECHA [idiomas]`, que sirve
  igual para añadir un idioma en el futuro o rehacer una traducción quitada.
- **Créditos**: el pie de cada edición traducida dice que es una traducción automática con IA de la
  castellana, sin revisión profesional. Juanjo revisa a las 5:00 el castellano y el catalán (ADR 0025).
- **Fuera de alcance**: los avisos de los grupos e Instagram siguen en castellano, porque los grupos
  son en castellano; «La semana en vídeo» sigue en castellano y catalán, y en los otros idiomas se
  enseña el castellano con la nota «Vídeo en castellano». La imagen genérica para redes de las
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
