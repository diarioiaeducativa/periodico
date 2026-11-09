# 43. Avisos del número en la app de Android, sin servidor

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

Con la app de Android ya hecha (ADR 0042), Juanjo preguntó si podía cargar cada día a las 7:00 el
número y avisar con una notificación si lo conseguía, y si no, volver a probar cada minuto. Preguntó
también si la notificación podía ser optativa. Vista la propuesta, la encargó («sí, hazlo así»).

Los avisos se habían descartado en el ADR 0013 porque, desde la web, exigen un servidor que guarde
las suscripciones y los envíe. Dentro de la app de Android no hace falta: el propio móvil puede mirar
un archivo del sitio y avisarse a sí mismo.

Lo que no se puede hacer como se pidió:

- **A las 7:00 en punto**: una alarma exacta necesita un permiso que Android 14 deniega de serie a las
  apps nuevas y que el usuario tendría que dar a mano; su variante automática, Google Play la reserva
  a despertadores y calendarios. Sin alarma exacta, la ventana más estrecha que admite Android es de
  10 minutos.
- **Cada minuto**: Android no despierta una app en segundo plano con esa frecuencia, y en reposo
  profundo espacia aún más las alarmas.
- **Dejar el número cargado**: la parte de Android no puede llenar la caché de la web, que solo se
  llena cuando la web se abre (ADR 0042). El aviso dice que el número ya está; al tocarlo, se carga.

## Decisión

- **El sitio publica `ultimo.json`** (`generar.py`, `ULTIMO`): el número, el día en que sale
  (AAAA-MM-DD, hora de Madrid) y, en cada idioma, la dirección de su portada, el nombre del diario y
  el titular de la primera pieza.
- **La app lo mira hacia las 7:00, hora de Madrid, y si aún no está, cada 15 minutos hasta las 9:30**
  (`android/avisos/java/Avisos.java`). El diario sale a las 6:50, y si falla reintenta cada 10 minutos
  hasta las 9:00 (ADR 0021): a las 9:30 ya ha salido o no saldrá esa mañana. Si a esa hora no lo ha
  encontrado, o no hay red, lo deja para el día siguiente.
- **Dos alarmas para cada comprobación**, con la misma hora: una con ventana de 10 minutos
  (`setWindow`), que suena a su hora con el móvil en uso o cargando, y otra que suena también en
  reposo profundo (`setAndAllowWhileIdle`), aunque Android puede retrasarla hasta una hora. La primera
  que suena mira; la que llega después ya no repite el aviso, porque el día queda marcado como avisado.
- **Las horas se calculan en Europe/Madrid y se programan en milisegundos UTC**: el cambio de hora no
  las mueve.
- **Apagados de serie.** Se encienden y se apagan en «Avisos del número», un enlace del pie que solo
  sale dentro de la app. Abre una ventana nativa (`AvisosActivity`) que explica qué hacen, cuándo miran
  y que el móvil solo consulta la web, y pide el permiso de notificaciones al encenderlos. Si se negó,
  lleva a los ajustes de Android. Nada sale al abrir la app (ninguna ventana al entrar). También se
  pueden quitar desde los ajustes de notificaciones de Android, como en cualquier app.
- **La app se reconoce** porque Chrome abre la primera página con `android-app://io.github.diarioiaeducativa`
  como referencia. La marca se guarda en la sesión (`sessionStorage`), no para siempre, porque la app
  comparte la memoria del sitio con Chrome y en Chrome el enlace no haría nada. La pone `CADUCIDAD`, el
  primer script de la cabecera, porque la portada de la raíz salta enseguida al idioma elegido y el
  resto de la página no llega a ejecutarse.
- **En el idioma del diario**: el enlace lleva el idioma de la página (`intent://avisos?idioma=XX…`) y la
  app lo recuerda para la ventana y para la notificación; si no lo sabe, el del móvil, o castellano.
  Textos en `android/avisos/res/values*/avisos.xml`.
- **La notificación** dice «Ya está el número N», con el titular de la primera pieza, y al tocarla abre
  la portada de su idioma dentro de la app. Icono «newspaper» de Lucide (ISC).
- **Al encender el móvil, al actualizar la app y al abrirla** se vuelven a programar: Android borra las
  alarmas al reiniciar, al actualizar y si se fuerza el cierre.
- **El código vive en `android/avisos/`** y lo engancha `android/avisos/aplicar.py`, que
  `construeix.sh` ejecuta antes de compilar: `bubblewrap update` rehace `AndroidManifest.xml` y
  `Application.java` y no sabe nada de los avisos.

## Alternativas descartadas

- **Alarma exacta** a las 7:00: permiso que el usuario tendría que dar en los ajustes y que Play
  restringe (véase el contexto).
- **Reintentar cada minuto**: Android no lo permite en segundo plano; cada 15 minutos basta, porque el
  diario reintenta cada 10.
- **Encendidos de serie**, o pedir el permiso al abrir la app por primera vez: interrumpe a quien llega
  a leer, y no todo el mundo los quiere.
- **WorkManager**: una dependencia más en un proyecto que rehace Bubblewrap, y su intervalo mínimo
  también es de 15 minutos; `AlarmManager` va incluido en Android.
- **Web Push o un servicio de avisos ajeno** (Firebase, OneSignal, ntfy): necesitan servidor (ADR 0013).
- **Leer `noticias.json` o el RSS**: más grandes y pensados para otra cosa; `ultimo.json` cabe en un
  kilobyte.

## Consecuencias

- Quien los enciende recibe cada mañana un aviso, sin que el diario sepa quién es: el móvil solo
  descarga un archivo público, sin identificarse (agente `DiarioIAEducativa-Android`).
- Solo en la app de Android; en la web y en iPhone, nada cambia.
- `ultimo.json` no puede cambiar de nombre ni de forma sin una versión nueva de la app que lo entienda:
  hay apps instaladas que lo leen.
- Si se cambian las horas de publicación del diario, revisar `HORA`, `FIN_HORA` y `FIN_MINUTO` en
  `Avisos.java`.

## Evidencia

- Alarmas exactas denegadas de serie en Android 14 y restricción de `USE_EXACT_ALARM` en Play:
  [Schedule exact alarms are denied by
  default](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms) y [Permissions
  and APIs that Access Sensitive
  Information](https://support.google.com/googleplay/android-developer/answer/16558241); ventana mínima de
  10 minutos: [Schedule alarms](https://developer.android.com/develop/background-work/services/alarms)
  (consultadas el 09-11-2026).
- En el emulador (Android 15), `dumpsys alarm` muestra la alarma de `setAndAllowWhileIdle` con una
  ventana de una hora y la de `setWindow` con una de 10 minutos.

## Riesgos y limitaciones

- Algunos fabricantes (Xiaomi, Huawei, Samsung con ahorro de batería agresivo) retrasan o cancelan las
  alarmas de las apps que no se abren a menudo; ahí el aviso puede llegar tarde o no llegar.
- Si el móvil pasa la mañana en reposo profundo, el aviso puede llegar hasta una hora tarde o al
  despertarlo.
- La marca de la app depende de que Chrome pase `android-app://…` como referencia en la primera página;
  si una versión de Chrome dejara de hacerlo, el enlace del pie no saldría (los avisos ya encendidos
  seguirían funcionando).

## Validación

09-11-2026, con la app compilada con `android/construeix.sh` en un emulador de Android 15 con Google
Play y Chrome:

- La ventana se abre con `diarioia://avisos?idioma=es` sobre la app, en castellano aunque el móvil está
  en inglés; «Activar» pide el permiso de notificaciones y, concedido, programa las dos alarmas para el
  día siguiente a las 7:00 (activados después de las 7:00).
- Con el reloj del emulador a las 6:59 y los avisos encendidos de nuevo, las alarmas quedan para las
  7:00 de ese día. A las 7:00 sonaron, pero la descarga falló: una TWA no pide el permiso de internet,
  porque quien navega es Chrome, y la comprobación sí lo necesita. Se añadió (`aplicar.py`) y se dejó
  el fallo en el registro de Android (`adb logcat -s Avisos`) para diagnosticar otros.
- Con el permiso, la notificación salió en catalán («Ja és aquí el número 8» y el titular), las
  alarmas siguientes quedaron para el día siguiente a las 7:00 y, al tocarla, se abrió
  https://diarioiaeducativa.github.io/ca/ dentro de la app.
- En la app, el enlace «Avisos del número» del pie aparece (y no en Chrome), y al pulsarlo se abre la
  ventana con los avisos activados y el botón para quitarlos.
- Tras `bubblewrap update`, que deja el manifiesto sin nada de los avisos, `construeix.sh` los vuelve a
  poner todos.
- Queda por ver en un móvil real el comportamiento de cada mañana con el ahorro de batería del
  fabricante.
