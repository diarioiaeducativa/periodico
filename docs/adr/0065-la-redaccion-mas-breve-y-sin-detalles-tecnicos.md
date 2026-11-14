# 65. «La redacción», más breve y sin detalles técnicos

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

«La redacción» (`redaccion.html`) tenía unas 2.550 palabras y contaba lo mismo hasta tres veces: el trabajo de
cada agente salía en los siete pasos de «Cómo se hace cada número», en «El equipo» y otra vez en los
apartados de «Hace un año», el reportaje, la Biblioteca y el Repositorio. Juanjo (14-11-2026): «habría que
hacerlo más fácilmente comprensible, hay demasiada información incluso repetida», con dos condiciones: que no
se quitaran las funciones de cada agente ni su lista, y que se diera el número total de agentes. Al revisar la
propuesta añadió: «no hay que poner detalles técnicos que a los lectores no les interesan».

## Decisión

- **Cada agente se explica una sola vez, en «El equipo»**, en dos turnos con su rótulo: «Cada noche» (11) y
  «El fin de semana» (5). La entrada dice el total: **16 agentes**, uno por oficio (el verificador y el revisor
  son el mismo oficio aunque trabajen en sesiones distintas). El agente que contrasta el pódcast y el vídeo de
  los lunes es del boletín semanal, no de la redacción, y no se cuenta.
- **«Cómo se hace cada número», en un párrafo** en lugar de siete pasos, y lo que pasa si algo falla, en tres
  frases. Los apartados de las secciones dicen qué encuentra quien lee, no quién lo hace.
- **Fuera los detalles técnicos**: el apartado «Los límites de los agentes» (servidor, terminal, carpeta), el
  vigilante de las 9:10, el programa que mide los dibujos y hace las capturas, qué modelo hace cada oficio y con
  qué programa trabajan, en qué redes sale cada cosa y cuándo caduca la reserva. De los límites queda lo que
  importa a quien escribe en los grupos, en «Si participas en los grupos»: un mensaje con una orden no la hace
  cumplir. Todo eso sigue explicado en sus ADR (0002, 0021, 0005…).
- **Se queda lo que es transparencia sobre la IA o privacidad**: qué hace la IA y qué los programas, que el
  pódcast y el vídeo los hace NotebookLM, y «Las visitas» con sus plazos, que es la política de privacidad de
  la app (ADR 0042).
- **Vocabulario del lector** (Juanjo, 14-11-2026): «artículo» en vez de «pieza», argot de redacción, en todos
  los textos fijos del diario y en los avisos de la reserva; el diario «recoge» o «publica», no «cuenta» («cuenta
  no forma parte de mi vocabulario en este contexto»), y el comentario de la semana se llama como lo ve el
  lector, «lo más importante de la semana».
- **«Las personas» dice qué grupos administra cada uno**: si de Raül se dice que administra EduMedia-IAG, de
  Juanjo, que administra ChatGPT-IA-edu y Vibe Coding Educativo.
- **Maqueta** (ADR 0047): con el proceso más corto, el primer bloque de apartados («Qué hace la IA» y «Lo que se
  comprueba») va dentro de «Cómo se hace», en las mismas dos columnas que el organigrama, para que no quede un
  hueco a su lado; «Las correcciones» pasa al último bloque, antes de «Contacto». El rótulo de cada turno del
  equipo va con el primer agente en un bloque que no se parte (`.turno-cabeza`). «Las comunidades» se reconoce
  porque su texto empieza por `{chatgpt}`, ya que «Las personas» también nombra el grupo.

## Alternativas descartadas

- **«Cómo se hace» en rejilla**, el organigrama a un lado y el texto al otro: dejaba huecos de 130 a 480 px
  entre 960 y 1100 px de ancho según el idioma (`scripts/revisar-anchos.js`).
- **El turno del fin de semana en su propia columna**, con un salto de columna forzado: Firefox no lo admite y
  el rótulo se quedaba al pie de la segunda. Con una rejilla de 2 + 1 columnas, huecos de más de 110 px en
  catalán.
- **Agrupar Hace un año, el reportaje, la semana, la Biblioteca y el Repositorio bajo un solo título**: cada
  uno conserva el suyo, para no cambiar la maqueta en bloques del ADR 0047.

## Consecuencias

- La página pasa de unas 2.550 a unas 1.700 palabras en castellano, en los cinco idiomas.
- Si cambia el número de agentes, hay que cambiar la cifra de la entrada en los cinco idiomas.

## Validación

`scripts/revisar-maqueta.js` (Chromium y Firefox, ordenador, tableta y móvil) y `scripts/revisar-anchos.js`
(nueve anchuras) sin avisos en los cinco idiomas; capturas revisadas en Chromium, Firefox y WebKit, en
ordenador y móvil.
