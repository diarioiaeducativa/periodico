// SPDX-License-Identifier: AGPL-3.0-or-later
// Revisión automática de la maqueta (ADR 0041), para `probar-web -s`: busca en la página los fallos de
// composición que un diario de papel no tendría. Escribe una línea «MAQUETA» con lo que encuentra (vacía si
// nada). Se pasa por todas las páginas, idiomas y anchuras antes de dar por buena una maqueta:
//
//   probar-web http://localhost:8767/ -n chromium,firefox -d escritorio,tableta,movil -s scripts/revisar-maqueta.js --sin-capturas
//
// Lo que mira:
//   hueco        en una fila de piezas, la columna más corta acaba mucho antes que la más larga (> 90 px)
//   fecha sola   una fecha que ocupa ella sola su línea, encima de un titular o de un antetítulo
//   solape       una fecha que pisa otro texto
//   miniaturas   dibujos de una misma fila con distinta altura
//   tamaños      fechas de distinto tamaño en la misma página
//   columna      un título de bloque al lado de sus piezas con una columna vacía debajo
//   pegados      dos bloques seguidos con menos de 12 px entre ellos
module.exports = async (page) => {
  const r = await page.evaluate(() => {
    const fallos = [];
    const vis = el => { const s = getComputedStyle(el); const b = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && b.width > 0 && b.height > 0; };
    const nombre = el => (el.closest('section[class*="sec-"], section, article')?.className || el.tagName).toString().slice(0, 40);
    const fondoTexto = el => { let m = el.getBoundingClientRect().top; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim() || !vis(n.parentElement)) continue; const rg = document.createRange(); rg.selectNodeContents(n);
        for (const x of rg.getClientRects()) m = Math.max(m, x.bottom); }
      for (const f of el.querySelectorAll('figure, img, svg')) if (vis(f)) m = Math.max(m, f.getBoundingClientRect().bottom);
      return m; };
    // Huecos en filas: hijos de una rejilla agrupados por su línea superior
    for (const g of document.querySelectorAll('main *')) {
      const s = getComputedStyle(g);
      if (s.display !== 'grid' || g.children.length < 2 || !vis(g)) continue;
      if (g.closest('.ilu, svg, .vineta, figure')) continue;
      const filas = {};
      for (const c of g.children) { if (!vis(c)) continue; const t = Math.round(c.getBoundingClientRect().top / 8); (filas[t] = filas[t] || []).push(c); }
      for (const fila of Object.values(filas)) {
        if (fila.length < 2) continue;
        const fondos = fila.map(fondoTexto); const d = Math.max(...fondos) - Math.min(...fondos);
        if (d > 90) fallos.push(`hueco de ${Math.round(d)} px en ${nombre(g)} (${g.className.toString().slice(0, 30)})`);
        const ilus = fila.map(c => c.querySelector(':scope > .ilu, :scope > figure')).filter(x => x && vis(x)).map(x => Math.round(x.getBoundingClientRect().height));
        if (ilus.length > 1 && Math.max(...ilus) - Math.min(...ilus) > 4) fallos.push(`miniaturas de ${ilus.join('/')} px en ${nombre(g)}`);
      }
    }
    // Fechas solas en su línea o pisando otro texto
    const tamanos = new Set();
    for (const f of document.querySelectorAll('main .fecha-pieza')) {
      if (!vis(f) || f.closest('.breve, li, .semana-rotulo')) continue;
      tamanos.add(getComputedStyle(f).fontSize);
      if (f.classList.contains('lectura')) continue;   // el tiempo de lectura del reportaje, en su línea tras la entradilla
      const R = f.getBoundingClientRect(); const caja = f.closest('article, section, header, li, .texto') || f.parentElement;
      let junto = false; const w = document.createTreeWalker(caja, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) { const n = w.currentNode; if (f.contains(n) || !n.textContent.trim() || !vis(n.parentElement)) continue;
        const rg = document.createRange(); rg.selectNodeContents(n);
        for (const x of rg.getClientRects()) {
          const vert = x.top < R.bottom - 2 && x.bottom > R.top + 2;
          if (vert) junto = true;
          if (vert && x.left < R.right - 1 && x.right > R.left + 1) fallos.push(`la fecha pisa «${n.textContent.trim().slice(0, 30)}» en ${nombre(f)}`);
        } }
      for (const ico of caja.querySelectorAll('svg.ico')) { const x = ico.getBoundingClientRect(); if (vis(ico) && !f.contains(ico) && x.top < R.bottom - 2 && x.bottom > R.top + 2) junto = true; }
      if (!junto) fallos.push(`fecha sola en su línea («${f.textContent.trim()}») en ${nombre(f)}`);
    }
    if (tamanos.size > 1) fallos.push(`fechas de distinto tamaño: ${[...tamanos].join(', ')}`);
    // Bloques seguidos que casi se tocan
    for (const m of document.querySelectorAll('main')) {
      const hs = [...m.children].filter(x => vis(x) && /^(SECTION|DIV|ASIDE|ARTICLE)$/.test(x.tagName));
      for (let i = 1; i < hs.length; i++) {
        const d = hs[i].getBoundingClientRect().top - hs[i - 1].getBoundingClientRect().bottom;
        if (d < 12 && hs[i].getBoundingClientRect().left < hs[i - 1].getBoundingClientRect().right) fallos.push(`pegados (${Math.round(d)} px): ${nombre(hs[i - 1])} y ${nombre(hs[i])}`);
      }
    }
    // Título de bloque al lado de sus piezas
    for (const b of document.querySelectorAll('.bloque')) {
      const t = b.querySelector('.bloque-titulo'), p = b.querySelector('.bloque-piezas');
      if (t && p && vis(t) && t.getBoundingClientRect().right < p.getBoundingClientRect().left + 5 && p.getBoundingClientRect().height > t.getBoundingClientRect().height + 80)
        fallos.push(`columna vacía bajo el título «${t.textContent.trim()}»`);
    }
    return [...new Set(fallos)];
  });
  console.log('MAQUETA ' + JSON.stringify(r));
};
