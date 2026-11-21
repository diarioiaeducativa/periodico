# 96. La app abre también sin Chrome, con el navegador interno de Android

Fecha: 2026-11-21 · Estado: aceptado

## Contexto

Google Play rechazó el 21-11-2026 la versión 1.0.4 de la app (ADR 0095) por «funcionalidad defectuosa»: «la
aplicación no se abre o no se carga», sin más detalle, sin informe previo al lanzamiento y sin decir en qué
dispositivo. La 1.0.3, con el mismo código de arranque, se había aceptado.

Probada la 1.0.4 en el emulador, abre bien con Chrome, con y sin conexión. El único caso en que no abre es un
móvil sin un navegador compatible con TWA: la app, con el respaldo de Bubblewrap en `customtabs`, no encuentra
navegador al que pasar la web y se cierra sin enseñar nada. La 1.0.3 hace lo mismo, así que puede ser el móvil del
revisor y no la versión; pero el caso es real (móviles sin Chrome o con Chrome desactivado), y Juanjo decidió
enviar la versión que lo resuelve («así solucionamos un problema que puede ser real»).

## Decisión

- **Respaldo en WebView** (`fallbackType: webview` en `android/twa-manifest.json` y `android/app/build.gradle`):
  sin navegador compatible, la app abre el diario en el navegador interno de Android (`WebViewFallbackActivity` de
  android-browser-helper), a pantalla completa. Con Chrome, todo sigue igual: TWA.
- Versión **1.0.5** (código 6), con lo mismo que la 1.0.4, que no llegó a publicarse.

## Alternativas descartadas

- **Reenviar la 1.0.4 sin cambios**: puede pasar con otro revisor, pero deja la app sin abrir en un móvil sin Chrome.
- **Apelar**: tarda de 5 a 8 días y no arregla ese caso.

## Consecuencias

- Abierta con el respaldo, la web no recibe el referrer `android-app://io.github.diarioiaeducativa`, así que no se
  sabe dentro de la app: no salen la tarjeta de los avisos ni el enlace del pie (ADR 0043 y 0095), y salía el
  anuncio de la app (ADR 0071), que se retira el 22-11-2026. Los avisos solo se pueden encender con Chrome.
- El WebView guarda sus datos aparte de Chrome: lo guardado para leer sin conexión es de la app.

## Evidencia

- Registro del emulador con la 1.0.4 y Chrome desactivado: `TWAProviderPicker: Found no TWA providers, using
  first browser: null`, y la app se cierra.
- Con la 1.0.5 y Chrome desactivado: `START … WebViewFallbackActivity`, y la portada se ve entera.

## Riesgos y limitaciones

- No se sabe con certeza por qué falló la revisión: es la causa más probable encontrada, no una confirmada.
- El navegador interno no abre los enlaces `intent://` de la web; por eso los avisos se quedan fuera en ese caso.

## Validación

21-11-2026, emulador `prueba-twa` (Android 15): la 1.0.4 abre con Chrome, con y sin conexión, y «Activar» pide el
permiso y enciende los avisos; con Chrome desactivado no abre. La 1.0.5 con Chrome desactivado abre la portada en el
navegador interno.
