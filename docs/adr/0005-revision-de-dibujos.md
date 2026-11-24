# 5. Revisión de los dibujos en su página

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

La infografía del primer reportaje (03-11-2026) salió con los círculos negros en el tema
claro: la sección nueva definía el color de trazo pero no el de relleno, y una variable CSS
sin definir deja el relleno en negro. En oscuro casi no se notaba. Nadie miraba los dibujos
pintados: el ilustrador solo comprobaba que el SVG fuera válido y sin colores escritos a mano.
Juanjo lo vio en pantalla y preguntó si no había un revisor de imágenes; se le propuso una
comprobación con programa y un revisor con IA, y lo aprobó.

## Decisión

- **Un programa sin IA** (`scripts/revisar-dibujos.py`) abre en un Chromium sin pantalla la
  página de cada pieza con dibujo, en tema claro y oscuro, y comprueba: ningún relleno negro
  puro (la tinta del diario nunca es #000), todas las formas con una clase de la hoja de
  estilo, rótulos dentro del dibujo y sin pisarse, contraste de rótulos (4,5:1) y trazos
  (3:1) con el fondo. Deja capturas en `revision/FECHA/` (no se sube).
- **Un revisor visual** (Sonnet 5.5, `encargos/pasos/2b-revision-dibujos.md`) mira esas
  capturas y la pieza, y devuelve lo que no se ve bien o no explica la noticia; solo errores
  de bulto, no de gusto.
- **Una vuelta al ilustrador** (`2c-ilustraciones-rehacer.md`) con todos los motivos. Si tras
  ella el dibujo sigue mal, la pieza sale sin dibujo, el SVG se guarda en
  `revision/FECHA/retirados/` y se avisa a Juanjo. Nunca retrasa ni impide el número.
- Se aplica a los dibujos del día (tras el paso 2 de `noche.sh`) y a la infografía del
  reportaje (en `reportaje.sh`). Los dibujos catalanes pasan solo el programa tras la
  traducción: el que falla se retira y la página catalana usa el castellano, ya revisado.
- La imagen del NAS lleva Playwright 1.61.0 con el Chromium sin pantalla más ligero
  (`--only-shell`), dentro del tope de 2 GB del contenedor; el navegador se cierra siempre.
- «La redacción» presenta al revisor de dibujos (ocho agentes cada día) y el organigrama le
  pone una marca junto al ilustrador.

## Consecuencias

- Uno o dos minutos más por noche, sin coste nuevo.
- Validación (03-11-2026): sobre todo lo publicado, en los dos idiomas y temas, sin falsos
  avisos; con la hoja de estilo de antes de la corrección marca los 9 rellenos negros; con un
  dibujo estropeado a propósito (forma sin clase, rótulos pisados y fuera del dibujo) detecta
  todo, el revisor dice qué quitar, el ilustrador lo arregla y la segunda ronda lo aprueba en un
  minuto; con un ilustrador simulado que no arregla nada, la pieza sale sin dibujo y se avisa.

## Ampliación del 23-11-2026: rótulos con contorno

El número del 22-11-2026 salió con dos rótulos ilegibles: «Dirección creativa» y «IA revela»
llevaban `class="a lbl"` para destacarlos, y la clase `a` les ponía el trazo de 2,5 de los dibujos,
que emborronaba las letras hasta no leerse. Pasó las dos revisiones: el programa no miraba el
contorno de los rótulos y el revisor visual dio el dibujo por bueno con una captura a tamaño real
(514 px de ancho), donde el borrón parece una negrita. Juanjo lo vio en la web.

- **La hoja de estilo** (`estaticos/comun.css`) quita el contorno a todo `<text>` con clase de
  trazo (`t`, `a`, `r`) y pinta del color de la clase los que llevan `a` o `r`: destacar un rótulo
  con su color es útil y el ilustrador lo seguirá haciendo, así que se admite y se dice en
  `encargos/ilustraciones.md`. Arregla también lo ya publicado, la tarjeta de compartir e Instagram,
  que usan la misma hoja.
- **El programa** avisa de cualquier rótulo con contorno, venga de donde venga.
- **Las capturas** se hacen a doble resolución, para que el revisor visual vea la letra.

Validación (23-11-2026), sobre el día 22 en los cinco idiomas: con la hoja anterior, el programa
marca los dos rótulos en los dos temas; con la nueva, los cuatro dibujos pasan, también el contraste
del rótulo en color (4,5:1), y las capturas se leen bien.

## Ampliación del 24-11-2026: colores con significado y rótulos que cambian de sentido

La vista previa del 23-11-2026 traía un semáforo («Guía de privacidad de herramientas educativas») con
la luz roja solo dibujada en su contorno, la de en medio vacía y la de abajo con el color de la sección,
y con el rótulo «Sin datos» para las herramientas que no tratan datos personales. Juanjo preguntó qué
quería decir «Sin datos» y pidió las luces de rojo, amarillo o naranja y verde, y que no volviera a pasar.
La causa: la hoja de los dibujos no tenía más colores que la tinta, el de la sección y el rojo de trazo,
y ni el ilustrador ni el revisor miraban si un acortamiento cambiaba el sentido.

- La hoja (`estaticos/comun.css`) suma tres rellenos fijos, iguales en los dos temas: `sr` (rojo),
  `sa` (ámbar) y `sv` (verde), solo para lo que en la realidad significa algo por su color. El
  programa los admite como clases de la hoja.
- La guía del ilustrador (`encargos/ilustraciones.md`) dice que un semáforo lleva siempre sus tres
  colores y que un rótulo, leído solo, dice lo mismo que la pieza.
- El revisor visual (`encargos/pasos/2b-revision-dibujos.md`) devuelve el dibujo si faltan los colores
  de verdad o si un rótulo acortado cambia de sentido.

Hipótesis sin comprobar: que el revisor visual detecte en adelante los rótulos ambiguos; es un juicio,
no una medida, y se verá en los próximos números. El dibujo del 23-11 se corrigió a mano en los cinco
idiomas antes de publicarse.
