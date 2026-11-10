// SPDX-License-Identifier: AGPL-3.0-or-later
// revisar-maqueta.js a nueve anchuras, también las intermedias que no cubren los dispositivos de probar-web
// (entre la tableta y el ordenador cambia la composición; ADR 0045). Escribe una línea «ANCHO n: MAQUETA [...]»
// por cada anchura con avisos; nada si todo está bien.
//
//   probar-web http://localhost:8767/ -n chromium,firefox -d escritorio -s scripts/revisar-anchos.js --sin-capturas
const revisar = require('./revisar-maqueta.js');
module.exports = async (page) => {
  for (const w of [1366, 1100, 960, 900, 840, 800, 700, 640, 390]) {
    await page.setViewportSize({ width: w, height: 900 }); await page.waitForTimeout(900);   // que la página iguale las filas
    const orig = console.log; let linea = '';
    console.log = (x) => { linea = x; }; await revisar(page); console.log = orig;
    if (linea !== 'MAQUETA []') console.log(`ANCHO ${w}: ${linea}`);
  }
};
