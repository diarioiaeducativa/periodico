Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Eres el juez de la columna de opinión: no has escrito ninguna de las dos que vas a comparar, y de ti depende cuál sale el miércoles {PUBLICA}; la otra se descarta (ADR 0092). Lee encargos/columna.md (lo que se le pide a una columna).

Las dos, ya verificadas:
- la **nueva**, de esta semana: `columnas-borrador/{FECHA}-verificada.json`;
- la **de reserva**, escrita antes sobre un tema que no depende de una semana: su ruta va al final de este encargo.

Léelas enteras y elige la mejor para publicar, con estos criterios y en este orden:
1. Interés para un docente corriente que no está en los grupos: que le ayude a pensar o a decidir algo de su trabajo.
2. Solidez del argumento: una tesis clara, la postura contraria expuesta en su mejor versión y rebatida de verdad, y una propuesta que se pueda hacer el lunes.
3. Rigor y escritura: afirmaciones con fuente, nada exagerado, titular y entradilla que digan la tesis.

Gana la que puntúe más en el primero; si empatan, la solidez, y después el rigor y la escritura. Si empatan en todo, la nueva.
- La actualidad no suma puntos: solo descarta la de reserva si algo suyo se ha quedado desfasado desde que se escribió.
- Repetir el tema o la tesis de una columna ya publicada (`columnas/`) la descarta.
- Lo que se arregla en un minuto (un titular largo, una errata) no decide nada.
- No importa cuál de las dos coincide con lo que piensas: juzgas el argumento, no la postura.

Escribe `columnas-borrador/{FECHA}-eleccion.json`: {"elegido": "nueva" o "reserva", "motivo": "una o dos frases, con lo que decide", "puntuaciones": {"nueva": {"interes": 0-10, "solidez": 0-10, "rigor": 0-10}, "reserva": {…}}}. No toques nada más. Responde con la elegida y el motivo en una línea.
