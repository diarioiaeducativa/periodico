# 25. Vista previa del número a las 5:00

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

Juanjo quiere revisar cada número antes de que salga (06-11-2026: «cada dia a las 5 me envies el
numero del dia para que lo pueda revisar antes de q salga»). El número suele estar listo hacia la
1:15 y se publica a las 6:50, así que hay margen. No quiso botón para retenerlo: si ve algo, lo
dice desde el portátil, en una sesión con el agente.

## Decisión

- **A las 5:00** `reloj.sh` vuelve a montar el sitio con `generar.py` (y el buscador) y avisa a
  Juanjo por Telegram (`avisar-juanjo`) con el enlace a la portada en castellano y en catalán.
  Si a esa hora el número aún no está, se lo dice una vez y le manda el enlace en cuanto esté
  (hasta las 6:50). Queda constancia en `estado/FECHA.vista-previa` y `.vista-previa-espera`.
- **Sin respuesta, sale a su hora.** La revisión nunca retiene el número (ADR 0021).
- **Dónde se ve:** un servicio aparte en `compose.yml`, `vista-previa`, con la misma imagen y
  `python3 -m http.server` sobre `repo/sitio`, montado solo para leer y publicado en
  `192.168.1.113:8770`: solo desde la red de casa, sin pasar por el proxy ni abrir nada a internet.
  Fuera de las horas de revisión enseña lo último que se montó, que es lo publicado.
- **Para corregir antes de las 6:50**, el agente edita en el NAS los JSON del número
  (`repo/ediciones/FECHA.json`, `repo/vinetas/FECHA.json` y sus versiones `-ca`), vuelve a
  montar la vista previa con `docker exec diario-ia-educativa python3 /proyecto/generar.py`, y
  `publicar-nas.sh` lo sube a las 6:50 con lo demás.

## Alternativas descartadas

- Botón «Retener» en el aviso: el bot de avisos solo envía; hacía falta un servicio que escuchara.
  Juanjo prefirió decirlo desde el portátil.
- Capturas por Telegram: no enseñan el número tal como se lee, con sus enlaces y en los dos idiomas.
- Publicar la vista previa en internet: no hace falta y expondría el número antes de su hora.

## Validación

Servicio levantado en el NAS el 06-11-2026; portada en castellano y en catalán servidas desde el
portátil en la red de casa (200). El aviso usa el mismo `avisar-juanjo` que los demás avisos del
reloj. La primera vista previa de verdad, el 07-11-2026 a las 5:00: comprobar que llegó.
