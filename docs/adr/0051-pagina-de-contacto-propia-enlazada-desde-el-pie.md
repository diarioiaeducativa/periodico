# 51. Página de contacto propia, enlazada desde el pie

Fecha: 2026-11-12 · Estado: aceptado

## Contexto

Google Play rechazó el primer envío de la app (versión 1, 12-11-2026) por la política de noticias y revistas:
«Doesn't contain a dedicated website and in-app page that's easy to find and clearly shows relevant contact
information». El contacto existía desde el ADR 0042, con el correo, pero como último apartado de «La
redacción» (`redaccion.html#contacto`) y sin ningún enlace que se llamase «Contacto». La captura que adjunta
el revisor recorre la portada, el pie, «Vídeos» y el buscador; «La redacción» no la abrió. La ficha de la
tienda (web y correo) y la declaración de noticias, que apuntaba a ese apartado, estaban completas.

## Decisión

- **El contacto tiene página propia**, `contacto.html`, en los cinco idiomas (`pagina_contacto()`): el título,
  para qué sirve, el correo a la vista en una franja y, debajo, las otras vías (una incidencia en GitHub o las
  personas que administran cada grupo). Juanjo la encargó el 12-11-2026, a propuesta del agente.
- **«Contacto» está en el pie de todas las páginas**, en la columna «El diario», justo después de «La
  redacción»: el pie es lo que se ve desde cualquier pantalla de la app.
- **En «La redacción» queda un apartado breve** que remite a la página, con el mismo `id="contacto"`: la
  dirección antigua sigue llevando a algo que habla de contacto. Lo decidió el agente por la maqueta: sin
  ese apartado, el último bloque dejaba una columna unos 100 px más corta en castellano, catalán y gallego
  (el diagrama de las comunidades no se puede partir; ADR 0047).
- **La declaración de noticias de Play Console lleva la dirección de la página nueva**, que por eso no se
  renombra.
- La página entra en el mapa del sitio y pasa por `cabeza()`, como las demás (ADR 0039).

## Alternativas descartadas

- **Solo un enlace «Contacto» en el pie hacia el apartado de «La redacción»**: más rápido, pero el correo
  seguía al final de una página larga y el rechazo pide literalmente una «contact page».
- **Quitar del todo el apartado de «La redacción»**, con un salto por JavaScript desde `#contacto`: dejaba el
  hueco de columna descrito arriba, y ningún orden de los apartados lo evitaba en castellano.
- **Un formulario**: exigiría un servidor que reciba los datos; el correo basta y es lo que pide la política
  («a phone number or email address»).

## Consecuencias

- Cualquier cambio de la dirección de contacto se hace en `CORREO_CONTACTO`, y es el mismo correo que el del
  contacto de la ficha de Google Play (ADR 0042).
- Si la página cambia de nombre, hay que cambiar también la declaración de noticias en Play Console.
- El pie tiene una línea más en la columna «El diario».

## Evidencia

- Correo de Google Play del 12-11-2026, «Action Required: Your app is not compliant with Google Play
  Policies (Diario de IA Educativa)», con la captura `IN_APP_EXPERIENCE-855.png`.
- [Requirements for news and magazine apps](https://support.google.com/googleplay/android-developer/answer/10523915)
  y [How to declare a news and magazine app](https://support.google.com/googleplay/android-developer/answer/16189314)
  (consultadas el 12-11-2026): el contacto se da con una dirección que también se encuentre dentro de la
  app, fácil de encontrar y al día, con un correo o un teléfono; solo redes sociales no vale. No dicen si
  tiene que ser una página entera: lo dice el correo del rechazo («Create a valid website and in-app contact
  page»).

## Riesgos y limitaciones

- Que Google lo acepte no está comprobado: la app se reenvió a revisión el 12-11-2026, con la página ya
  publicada, la dirección nueva en la declaración de noticias y la versión 1.0.1 (ADR 0048); la revisión
  suele tardar hasta siete días.
- El correo va en entidades HTML (ADR 0042): se lee igual, pero un recolector que las interprete lo obtiene.

## Validación

12-11-2026, con el sitio generado en local: la página, en los cinco idiomas, en Chromium, Firefox y WebKit,
en escritorio, tableta y móvil, sin errores ni desbordamiento; `scripts/revisar-maqueta.js` y
`scripts/revisar-anchos.js` sin avisos en «La redacción», la página de contacto y la portada. El último
bloque de «La redacción», medido con Playwright en los tres navegadores y los cinco idiomas a 1000, 1100,
1280, 1366 y 1600 px: ninguna columna acaba más de 67 px antes que las otras (el límite del ADR 0047 es 90).
