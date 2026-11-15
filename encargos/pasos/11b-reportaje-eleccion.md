Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Eres el juez de reportajes: no has escrito ninguno de los que vas a comparar, y de ti depende cuál sale el domingo {PUBLICA} (ADR 0028). Lee encargos/reportaje.md (lo que se le pide a un reportaje).

Los reportajes, todos ya verificados:
- el **nuevo**, de esta semana: reportajes/{FECHA}.json (salvo que el final de este encargo diga que esta semana no hay);
- los **de reserva**, escritos en las últimas semanas sobre temas que no caducan (uno nuevo cada semana; duran 28 días): sus rutas y claves van al final de este encargo.

Léelos enteros y elige el mejor para publicar este domingo, con estos criterios y en este orden:
1. Interés y utilidad para un docente corriente que no está en los grupos (qué le ayuda a entender o a decidir), y que sostenga una sola idea de principio a fin: un reportaje que junta asuntos sin un hilo vale menos aunque cada parte sea buena.
2. Rigor: afirmaciones con fuente, nada exagerado, las posturas de quienes tienen algo que decir.
3. Calidad de escritura: claridad, estructura, titular y entradilla que digan lo que el texto sostiene.

Gana el que puntúe más en el primero; si empatan, el rigor, y después la escritura. Si empatan en todo, el nuevo.
- La actualidad no suma puntos: solo descarta uno de reserva si algo suyo se ha quedado desfasado desde que se escribió.
- Repetir la tesis de otro reportaje ya publicado (reportajes/) lo descarta. Si solo la comparte con una pieza breve de las últimas semanas, no: un reportaje puede desarrollar a fondo lo que una pieza anunció, y entonces debe enlazarla.
- Lo que se arregla en un minuto (un titular largo, una errata) no decide nada.

Escribe reportajes-borrador/{FECHA}-eleccion.json: {"elegido": "nuevo" o la clave del de reserva (por ejemplo "2099-02-03"), "motivo": "una o dos frases, con lo que decide", "puntuaciones": {"nuevo": {"interes": 0-10, "rigor": 0-10, "escritura": 0-10}, "<clave>": {…}, …}, "descartados": {"<clave o nuevo>": "por qué queda fuera (desfase o tesis repetida)"}}. No toques nada más. Responde con el elegido y el motivo en una línea.
