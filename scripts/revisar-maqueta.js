// SPDX-License-Identifier: AGPL-3.0-or-later
// Revisión automática de la maqueta (ADR 0041), para `probar-web -s`: busca en la página los fallos de
// composición que un diario de papel no tendría. Escribe una línea «MAQUETA» con lo que encuentra (vacía si
// nada). Se pasa por todas las páginas, idiomas y anchuras antes de dar por buena una maqueta:
//
//   probar-web http://localhost:8767/ -n chromium,firefox -d escritorio,tableta,movil -s scripts/revisar-maqueta.js --sin-capturas
//
// Lo que mira:
//   hueco        en una fila de piezas, la columna más corta acaba mucho antes que la más larga (> 90 px);
//                no cuenta una columna fija al bajar (sticky), como el calendario de la hemeroteca
//   fecha sola   una fecha que ocupa ella sola su línea, encima de un titular o de un antetítulo
//   solape       una fecha que pisa otro texto
//   miniaturas   dibujos de una misma fila con distinta altura
//   tamaños      fechas de distinto tamaño en la misma página
//   columna      un título de bloque al lado de sus piezas con una columna vacía debajo
//   pegados      dos bloques seguidos con menos de 12 px entre ellos
//   cabecera     el titular o la entradilla de una pieza sin dibujo deja vacía la derecha (> 250 px)
//   incompleta   la última fila de una rejilla de piezas deja columnas vacías a la derecha (> 90 px)
// La comprobación en sí está en maqueta-pagina.js, que comparte con la revisión de cada madrugada (revisar-maqueta.py)
const fs = require('fs');
const COMPROBAR = fs.readFileSync(require('path').join(__dirname, 'maqueta-pagina.js'), 'utf8').replace(/^\/\/.*\n/gm, '');
module.exports = async (page) => {
  const r = await page.evaluate(`(${COMPROBAR.trim()})()`);
  console.log('MAQUETA ' + JSON.stringify(r));
};
