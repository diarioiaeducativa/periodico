# 64. Correo de contacto propio del diario

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

La página de contacto (ADR 0051) y «La redacción» daban como correo el personal de Juanjo. Un medio con
dirección propia se presenta mejor, también ante las políticas de transparencia de Google Noticias (ADR 0063),
y el correo personal no tiene por qué estar en una página pública si funciona igual sin él. Además, la
herramienta de privacidad del agente bloqueaba cualquier orden que ejecutara `generar.py` mientras tuviera
dentro el correo personal, y eso impedía probar el diario sin pedírselo a Juanjo. Él aprobó una dirección
propia y dejó elegir el nombre al agente.

## Decisión

- **`diarioiaeducativa@bilateria.org`**, en `CORREO_CONTACTO`. Lleva el nombre del diario porque bilateria.org
  aloja también otros proyectos: con `redaccion@` o `diario@` no quedaría claro de qué medio es.
- Es un **reenvío** de IONOS (incluido en el plan de hosting de bilateria.org, sin coste) al correo de Juanjo.
  No es un buzón: no guarda nada y no se puede escribir desde ella.

## Alternativas descartadas

- **Un buzón básico** de IONOS (también incluido): permitiría responder desde la dirección del diario, pero es
  un buzón más que mirar. Si hace falta responder como el diario, se puede pasar a él más adelante.
- **Sacar el correo personal del código a una variable de entorno**: quita el bloqueo, pero lo deja en la web y
  obliga a ponerlo en el contenedor del NAS y en el vigilante; sin la variable, la página saldría sin correo.

## Consecuencias

- Las respuestas salen del correo personal de Juanjo: quien escribe al diario lo verá en la respuesta, en un
  trato privado.
- Los mensajes reenviados no pasan por el filtro de spam de IONOS; los filtra Gmail al llegar.
- La dirección del reenvío se cambia en el panel de IONOS (Correo > Vista general).

## Evidencia

- Panel de IONOS (14-11-2026): en «Crear una nueva dirección de correo electrónico», el reenvío y el correo
  básico se ofrecen con «Crear», sin precio, y los buzones Business y Exchange, con «Solicitar»; la página del
  reenvío dice que no es un buzón independiente, que no se puede enviar desde él y que lo entrante no pasa por
  el filtro antispam.
- `dig MX bilateria.org`: `mx00.ionos.es` y `mx01.ionos.es`; no hizo falta tocar los DNS.

## Riesgos y limitaciones

- Una dirección publicada recibe spam; si llega mucho, se puede pasar al buzón básico, que sí lo filtra.

## Validación

- Un mensaje enviado a la dirección desde el hosting de IONOS llegó a la bandeja de entrada de Juanjo
  (14-11-2026). Uno enviado desde su propio Gmail no aparece en la bandeja: Gmail descarta la copia reenviada de
  lo que manda uno mismo, así que esa prueba no vale.
- Web generada en una copia: la página de contacto, en castellano, catalán e inglés, solo lleva la dirección
  nueva.
