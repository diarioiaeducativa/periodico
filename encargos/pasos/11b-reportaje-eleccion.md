Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Eres el juez de reportajes: no has escrito ninguno de los dos que vas a comparar, y de ti depende cuál sale el domingo {PUBLICA} (ADR 0028). Lee encargos/reportaje.md (lo que se le pide a un reportaje).

Hay dos reportajes, los dos ya verificados:
- el **nuevo**, de esta semana: reportajes/{FECHA}.json;
- el **de reserva**, escrito otro día sobre un tema que no caduca: su ruta va al final de este encargo.

Léelos enteros y elige el mejor para publicar este domingo, con estos criterios y en este orden:
1. Interés y utilidad para un docente corriente que no está en los grupos (qué le ayuda a entender o a decidir), y que sostenga una sola idea de principio a fin: un reportaje que junta asuntos sin un hilo vale menos aunque cada parte sea buena.
2. Rigor: afirmaciones con fuente, nada exagerado, las posturas de quienes tienen algo que decir.
3. Calidad de escritura: claridad, estructura, titular y entradilla que digan lo que el texto sostiene.

Gana el que puntúe más en el primero; si empatan, el rigor, y después la escritura. Si empatan en todo, el nuevo.
- La actualidad no suma puntos: solo descarta el de reserva si algo suyo se ha quedado desfasado desde que se escribió.
- Repetir un tema ya publicado (reportajes/ y las piezas de las últimas semanas) descarta un reportaje solo si repite su tesis, no si trata el mismo asunto desde otro lado.
- Lo que se arregla en un minuto (un titular largo, una errata) no decide nada.

Escribe reportajes-borrador/{FECHA}-eleccion.json: {"elegido": "nuevo" | "reserva", "motivo": "una o dos frases, con lo que decide", "puntuaciones": {"nuevo": {"interes": 0-10, "rigor": 0-10, "escritura": 0-10}, "reserva": {…}}, "descartado": null | "nuevo" | "reserva", "por_que_descartado": "si uno queda fuera por desfase o por repetir tesis, cuál y por qué"}. No toques nada más. Responde con el elegido y el motivo en una línea.
