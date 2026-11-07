# 29. Las comunidades, en tres círculos

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

Juanjo pidió tres círculos, uno por grupo, con los miembros de solo cada grupo, los de dos en dos, los de
los tres y el total de personas distintas: «esto sería informativo pero sería también una especie de
logotipo» (06-11-2026). Las cifras las cuenta el Bot de IA Educativa, administrador de los tres grupos
(ADR 0032 del repositorio del bot): cada día deja `datos/comunidades/AAAA-MM-DD.json` (hasta el 07-11-2026, cada semana), solo cifras.

## Decisión

- **Dónde**: en «La redacción», bajo «Las comunidades», el diagrama con sus cifras, a la derecha del
  texto (380 px en el ordenador; en el móvil, todo el ancho bajo el título), ampliable al pulsarlo. En el
  pie de todas las páginas, bajo los tres grupos de «Únete a la conversación», el emblema sin cifras y
  «5210 personas en tres comunidades», que lleva al diagrama (`redaccion.html#comunidades`). En la
  cabecera no: el nombre del diario ya es su identidad.
- **Cómo**: tres círculos iguales, cada uno con el color de su sección (ChatGPT-IA-edu, el azul de
  Herramientas; Vibe Coding Educativo, el verde de Vibe coding; EduMedia-IAG, el magenta de Multimedia),
  translúcidos para que los cruces se oscurezcan solos. Los nombres de los grupos, en su color (contraste
  de 5,1:1 a 10:1 en los dos temas) y con sus miembros debajo; cada cifra, en el centro calculado de su
  zona; debajo, el total y la fecha abreviada entre paréntesis. Iguales y no proporcionales: con tres
  círculos no se pueden ajustar a la vez todas las áreas a sus cifras, y las zonas pequeñas (92, 145) no
  dejarían sitio al número. Girado 30° con Vibe Coding Educativo arriba, el nombre más largo centrado
  sobre su círculo: así el de EduMedia-IAG no cae encima del total y el dibujo es más estrecho.
- **Cifras**: sin punto de miles hasta cuatro cifras (RAE e IEC), con espacio fino desde cinco; en
  inglés, con coma. El texto para lectores de pantalla las da todas, con la fecha completa.
- **De dónde salen**: el contenedor del diario ve la carpeta del bot en `/bot-datos` (solo lectura);
  `publicar-nas.sh` copia las cifras nuevas a `comunidades/` del repositorio y las sube con el número, para
  que el sitio que monta el vigilante desde GitHub (ADR 0021) también las tenga. `generar.py` usa la
  última; si no hay ninguna, no sale ni el diagrama ni el emblema.

## Validación

Cifras del 06-11-2026 (5.210 personas distintas), en las cinco lenguas, tema claro y oscuro, en el
ordenador y en un móvil de 375 px, revisado en pantalla por Juanjo antes de publicar.
