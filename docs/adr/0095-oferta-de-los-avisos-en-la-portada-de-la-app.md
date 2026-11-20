# 95. Oferta de los avisos del número en la portada de la app

Fecha: 2026-11-20 · Estado: aceptado

## Contexto

Los avisos del número (ADR 0043) solo se podían encender desde el enlace «Avisos del número» del pie, que sale
dentro de la app de Android. Juanjo pidió que se ofrecieran como en meteo-local (su ADR 0080): una tarjeta en la
portada, para encenderlos de un toque, en lugar de depender del enlace del pie. Vista la propuesta, la encargó («hazlo
así»): tarjeta, versión nueva de la app para encenderlos de un toque y el enlace del pie, que se queda.

## Decisión

- **Una tarjeta en la portada de cada idioma**, en el sitio y con la forma del anuncio de la app (ADR 0071), bajo la
  barra de secciones (`franja_avisos()` y `OFERTA_AVISOS` en `generar.py`): la campana que suena de Lucide, como en
  meteo-local, «Aviso del número cada mañana», la hora con su huso (ADR 0091) y dos botones, «Activar» y «Ahora no».
  Los dos anuncios no coinciden nunca: el de la app sale solo fuera de ella, y este solo dentro.
- **Solo dentro de la app**, con la misma marca de sesión que el enlace del pie (`diario.app`), y hasta que se pulsa
  uno de los dos botones o el enlace del pie (`diario.oferta-avisos` en `localStorage`). La web no sabe si los avisos
  están encendidos, porque eso lo guarda la parte de Android: por eso deja de salir al pulsar cualquiera de los dos.
- **«Activar»** abre la ventana nativa con `activar=1` (`intent://avisos?idioma=XX&activar=1…`). Desde la versión
  1.0.4 de la app (`AvisosActivity`), eso pide el permiso de notificaciones y los enciende sin enseñar la ventana; si
  ya estaban encendidos, solo lo dice. Las versiones anteriores no conocen el parámetro y enseñan la ventana de
  siempre, donde hay que pulsar «Activar» otra vez.
- **El enlace del pie se queda**, solo dentro de la app: es el único sitio para encenderlos si se dijo «Ahora no» y
  para apagarlos, como la campana de meteo-local.

## Alternativas descartadas

- **Quitar el enlace del pie**: quien dijo «Ahora no» ya no podría encenderlos; apagarlos sí se puede desde los
  ajustes de Android.
- **Que la app le diga a la web si los avisos están encendidos** (un parámetro en la dirección de inicio): otro cambio
  de la app y de la web para un caso que solo se da una vez por móvil.
- **Debajo de la apertura**, como se propuso al principio: el sitio del anuncio de la app ya está hecho para una
  franja así, a todo el ancho y sin huecos con ninguna anchura, y no parte la maqueta del periódico.

## Consecuencias

- Quien ya los había encendido desde el pie verá la tarjeta una vez; quien pulse el enlace del pie a partir de ahora,
  no.
- La versión 1.0.4 tiene que subirse a Google Play para que «Activar» sea de un toque; hasta entonces, funciona con
  la ventana.

## Riesgos y limitaciones

- La tarjeta depende de la misma marca de la app que el enlace del pie (ADR 0043): si Chrome dejara de pasar
  `android-app://…` como referencia, no saldría.

## Validación

20-11-2026:

- `probar-web` en Chromium, Firefox y WebKit, en escritorio, móvil y tableta, claro y oscuro, con la marca de la app:
  la tarjeta sale y el anuncio de Google Play no; sin errores ni desbordamiento. En el móvil, los botones bajaban al
  lado del texto y lo estrechaban: van en su propia fila.
- Textos comprobados en las cinco portadas, con el huso de cada lengua.
- Emulador `prueba-twa` (Android 15) con la app 1.0.4 compilada con `construeix.sh`, sin permiso y sin avisos: al
  pulsar «Activar» en la tarjeta, Android pide el permiso directamente; concedido, sale «Avisos activados», la
  tarjeta desaparece y quedan las dos alarmas para las 7:00 del día siguiente (`dumpsys alarm`). Al recargar, la
  tarjeta no vuelve. Con los avisos ya encendidos, `activar=1` solo dice «Avisos activados».
