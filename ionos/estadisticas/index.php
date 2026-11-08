<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Panel privado de las visitas del diario (ADR 0033), para sus dos autores. Lee las sumas en el
// momento; se guardan por hora en UTC y se muestran por día en hora de Madrid.

declare(strict_types=1);
require __DIR__ . '/comun.php';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

const COOKIE = 'diario_panel';
const DURACION = 90 * 86400;
$MADRID = new DateTimeZone('Europe/Madrid');
$UTC = new DateTimeZone('UTC');

function firma(string $usuario, int $caduca): string {
    // Con la contraseña dentro: al cambiarla, se cierran las sesiones abiertas en otros navegadores
    $clave = (string) (config()['usuarios'][$usuario] ?? '');
    return hash_hmac('sha256', $usuario . '|' . $caduca, (string) (config()['secreto'] ?? '') . $clave);
}

function usuario_actual(): ?string {
    $c = explode('|', (string) ($_COOKIE[COOKIE] ?? ''));
    if (count($c) !== 3 || (int) $c[1] < time() || !isset(config()['usuarios'][$c[0]])) {
        return null;
    }
    return hash_equals(firma($c[0], (int) $c[1]), $c[2]) ? $c[0] : null;
}

function abrir_sesion(string $usuario): void {
    $caduca = time() + DURACION;
    setcookie(COOKIE, $usuario . '|' . $caduca . '|' . firma($usuario, $caduca),
        ['expires' => $caduca, 'path' => dirname($_SERVER['SCRIPT_NAME']) . '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
}

// Entrar y salir
$error = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && isset($_POST['usuario'])) {
    $u = strtolower(trim((string) $_POST['usuario']));
    $h = config()['usuarios'][$u] ?? null;
    if ($h && password_verify((string) ($_POST['clave'] ?? ''), $h)) {
        abrir_sesion($u);
        header('Location: ./');
        exit;
    }
    usleep(800000);
    $error = 'Usuario o contraseña incorrectos.';
}
if (isset($_GET['salir'])) {
    setcookie(COOKIE, '', ['expires' => 1, 'path' => dirname($_SERVER['SCRIPT_NAME']) . '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
    header('Location: ./');
    exit;
}
$yo = usuario_actual();

// Cambiar la propia contraseña: se reescribe config.php con el nuevo hash
$cambio = isset($_GET['clave']) && $yo;
$cambio_error = '';
if ($cambio && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && isset($_POST['actual'])) {
    $nueva = (string) ($_POST['nueva'] ?? '');
    if (!password_verify((string) $_POST['actual'], config()['usuarios'][$yo])) {
        usleep(800000);
        $cambio_error = 'La contraseña actual no es correcta.';
    } elseif (mb_strlen($nueva) < 8) {
        $cambio_error = 'La nueva contraseña tiene que tener al menos 8 caracteres.';
    } elseif ($nueva !== (string) ($_POST['repite'] ?? '')) {
        $cambio_error = 'Las dos contraseñas nuevas no coinciden.';
    } else {
        $c = config();
        $c['usuarios'][$yo] = password_hash($nueva, PASSWORD_DEFAULT);
        $f = __DIR__ . '/config.php';
        $tmp = $f . '.tmp';
        if (file_put_contents($tmp, "<?php\nreturn " . var_export($c, true) . ";\n", LOCK_EX) !== false && chmod($tmp, 0604) && rename($tmp, $f)) {
            if (function_exists('opcache_invalidate')) {
                opcache_invalidate($f, true);
            }
            $GLOBALS['config_nueva'] = $c;
            abrir_sesion($yo);
            header('Location: ' . rtrim(dirname($_SERVER['SCRIPT_NAME']), '/') . '/?cambiada=1');
            exit;
        }
        $cambio_error = 'No se ha podido guardar. Inténtalo otra vez.';
    }
}

/** Las sumas entre dos días de Madrid (incluidos), repartidas por día de Madrid. */
function recoger(DateTimeImmutable $desde, DateTimeImmutable $hasta): array {
    global $MADRID, $UTC;
    $dias = [];
    for ($d = $desde; $d <= $hasta; $d = $d->modify('+1 day')) {
        $dias[$d->format('Y-m-d')] = ['visitas' => 0, 'paginas' => 0];
    }
    $paginas = [];
    $titulos = [];
    $ini = $desde->setTimezone($UTC)->modify('-1 day');
    $fin = $hasta->setTimezone($UTC)->modify('+1 day');
    for ($u = $ini; $u <= $fin; $u = $u->modify('+1 day')) {
        $fecha = $u->format('Y-m-d');
        if (!is_file(archivo_dia($fecha))) {
            continue;
        }
        $datos = leer_dia($fecha);
        $dia_de = function (string $hora) use ($fecha, $UTC, $MADRID): string {
            return (new DateTimeImmutable($fecha . ' ' . $hora . ':00:00', $UTC))->setTimezone($MADRID)->format('Y-m-d');
        };
        foreach ($datos['v'] as $hora => $n) {
            $dm = $dia_de((string) $hora);
            if (isset($dias[$dm])) {
                $dias[$dm]['visitas'] += $n;
            }
        }
        foreach ($datos['p'] as $ruta => $horas) {
            foreach ($horas as $hora => $n) {
                $dm = $dia_de((string) $hora);
                if (isset($dias[$dm])) {
                    $dias[$dm]['paginas'] += $n;
                    $paginas[$ruta] = ($paginas[$ruta] ?? 0) + $n;
                }
            }
        }
        $titulos = ($datos['t'] ?? []) + $titulos;
    }
    return [$dias, $paginas, $titulos];
}

function idioma(string $ruta): string {
    return preg_match('#^/(ca|gl|eu|en)/#', $ruta, $m) ? $m[1] : 'es';
}

if (isset($_GET['datos'])) {
    header('Content-Type: application/json; charset=utf-8');
    if (!$yo) {
        http_response_code(401);
        echo '{}';
        exit;
    }
    $hoy = new DateTimeImmutable('today', $MADRID);
    $periodo = (string) ($_GET['periodo'] ?? '7');
    $n = ['hoy' => 1, '7' => 7, '30' => 30, '90' => 90, 'todo' => MESES_CONSERVADOS * 31][$periodo] ?? 7;
    $inicio_serie = $hoy->modify('-29 days');
    // La gráfica empieza el primer día con datos, no con un mes de ceros
    $primero = (glob(DATOS . '/????-??-??.json') ?: [null])[0];
    if ($primero) {
        $p = (new DateTimeImmutable(basename($primero, '.json'), $UTC))->setTimezone($MADRID)->setTime(0, 0);
        if ($p > $inicio_serie) {
            $inicio_serie = $p;
        }
    }
    $inicio = $hoy->modify('-' . ($n - 1) . ' days');
    [$dias, $paginas, $titulos] = recoger(min($inicio, $inicio_serie), $hoy);
    $suma = function (int $k) use ($dias, $hoy): array {
        $desde = $hoy->modify('-' . ($k - 1) . ' days')->format('Y-m-d');
        $v = $p = 0;
        foreach ($dias as $d => $x) {
            if ($d >= $desde) {
                $v += $x['visitas'];
                $p += $x['paginas'];
            }
        }
        return ['visitas' => $v, 'paginas' => $p];
    };
    // Las páginas y los idiomas, solo del periodo elegido
    if ($n < 30) {
        [, $paginas, $titulos] = recoger($inicio, $hoy);
    }
    arsort($paginas);
    $idiomas = ['es' => 0, 'ca' => 0, 'gl' => 0, 'eu' => 0, 'en' => 0];
    foreach ($paginas as $r => $c) {
        $idiomas[idioma($r)] += $c;
    }
    $top = [];
    foreach (array_slice($paginas, 0, 30, true) as $r => $c) {
        $top[] = ['ruta' => $r, 'titulo' => $titulos[$r] ?? '', 'n' => $c];
    }
    $serie = [];
    foreach ($dias as $d => $x) {
        if ($d >= $inicio_serie->format('Y-m-d')) {
            $serie[] = ['dia' => $d] + $x;
        }
    }
    echo json_encode([
        'hoy' => $suma(1), 'semana' => $suma(7), 'mes' => $suma(30),
        'periodo' => $periodo, 'top' => $top, 'idiomas' => $idiomas, 'serie' => $serie,
        'actualizado' => (new DateTimeImmutable('now', $MADRID))->format('H:i'),
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
?><!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Visitas del diario</title>
<?php if ($yo): ?>
<script>
// Cada navegador desde el que entran los autores queda marcado en el diario para no contar sus visitas:
// salto de ida y vuelta, una sola vez por navegador (ADR 0033)
try {
  var q = new URLSearchParams(location.search);
  if (q.get('marcado') === '1') { localStorage.setItem('diario.marcado', '1'); history.replaceState(null, '', location.pathname); }
  else if (!localStorage.getItem('diario.marcado')) {
    localStorage.setItem('diario.prueba', '1'); localStorage.removeItem('diario.prueba');   // sin memoria, no salta: no habría vuelta atrás
    location.replace('https://diarioiaeducativa.github.io/redaccion.html?nocontar=1&volver=1');
  }
} catch (_) {}
</script>
<?php endif; ?>
<style>
:root { --fondo:#f6f4ef; --papel:#fff; --tinta:#1c1d21; --tinta-2:#5d6068; --linea:#dedad0; --acento:#b3261e; --barra:#2f5d8a; }
@media (prefers-color-scheme: dark) { :root { --fondo:#16181d; --papel:#1f2229; --tinta:#eceae4; --tinta-2:#a3a6ad; --linea:#363a44; --acento:#ff7a6e; --barra:#7fb0e0; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--fondo); color:var(--tinta); font:16px/1.45 system-ui, sans-serif; }
main { max-width: 60rem; margin: 0 auto; padding: 1rem; }
header { display:flex; flex-wrap:wrap; align-items:baseline; justify-content:space-between; gap:.5rem; }
h1 { font-size:1.4rem; margin:.3rem 0; }
h2 { font-size:1.05rem; margin:1.4rem 0 .5rem; }
.aviso { color:var(--tinta-2); font-size:.9rem; margin:0; }
.cifras { display:grid; grid-template-columns:repeat(3, 1fr); gap:.6rem; margin-top:.8rem; }
.cifra { background:var(--papel); border:1px solid var(--linea); border-radius:10px; padding:.7rem .8rem; }
.cifra b { display:block; font-size:2rem; line-height:1.1; }
.cifra span { color:var(--tinta-2); font-size:.85rem; }
.caja { background:var(--papel); border:1px solid var(--linea); border-radius:10px; padding:.8rem; }
svg { display:block; width:100%; height:auto; }
.periodos { display:flex; flex-wrap:wrap; gap:.3rem; }
.periodos button { font:inherit; font-size:.9rem; padding:.3rem .7rem; border:1px solid var(--linea); border-radius:99px; background:var(--papel); color:var(--tinta); cursor:pointer; }
.periodos button[aria-pressed="true"] { background:var(--tinta); color:var(--papel); border-color:var(--tinta); }
table { width:100%; border-collapse:collapse; font-size:.95rem; }
td { padding:.35rem .3rem; border-top:1px solid var(--linea); vertical-align:top; }
td.n { text-align:right; font-variant-numeric:tabular-nums; width:4rem; }
td small { color:var(--tinta-2); display:block; word-break:break-all; }
a { color:inherit; }
.idiomas { display:flex; flex-wrap:wrap; gap:.4rem 1rem; margin:.5rem 0 0; color:var(--tinta-2); font-size:.9rem; }
form.entrar { max-width:22rem; margin:4rem auto; background:var(--papel); border:1px solid var(--linea); border-radius:10px; padding:1.2rem; }
form.entrar label { display:block; margin:.7rem 0 .25rem; font-weight:600; }
form.entrar input { width:100%; font:inherit; padding:.5rem .6rem; border:1px solid var(--linea); border-radius:6px; background:var(--fondo); color:var(--tinta); }
form.entrar button { margin-top:1rem; font:inherit; font-weight:600; padding:.55rem 1rem; border:0; border-radius:6px; background:var(--tinta); color:var(--papel); cursor:pointer; }
.error { color:var(--acento); }
@media (max-width: 30rem) { .cifra b { font-size:1.5rem; } }
</style>
</head>
<body>
<?php if (!$yo): ?>
<form class="entrar" method="post">
  <h1>Visitas del diario</h1>
  <p class="aviso">Acceso para los autores del Diario de IA Educativa.</p>
  <?php if ($error): ?><p class="error"><?= htmlspecialchars($error) ?></p><?php endif; ?>
  <label for="usuario">Usuario</label>
  <input id="usuario" name="usuario" autocomplete="username" required>
  <label for="clave">Contraseña</label>
  <input id="clave" name="clave" type="password" autocomplete="current-password" required>
  <button type="submit">Entrar</button>
</form>
<?php elseif ($cambio): ?>
<form class="entrar" method="post" action="?clave">
  <h1>Cambiar contraseña</h1>
  <p class="aviso">Usuario: <?= htmlspecialchars($yo) ?>. Al cambiarla se cierra la sesión en los demás navegadores.</p>
  <?php if ($cambio_error): ?><p class="error"><?= htmlspecialchars($cambio_error) ?></p><?php endif; ?>
  <input type="text" name="usuario_oculto" value="<?= htmlspecialchars($yo) ?>" autocomplete="username" hidden>
  <label for="actual">Contraseña actual</label>
  <input id="actual" name="actual" type="password" autocomplete="current-password" required>
  <label for="nueva">Nueva contraseña</label>
  <input id="nueva" name="nueva" type="password" autocomplete="new-password" minlength="8" required>
  <label for="repite">Repite la nueva</label>
  <input id="repite" name="repite" type="password" autocomplete="new-password" minlength="8" required>
  <button type="submit">Guardar</button>
  <p class="aviso" style="margin-top:1rem"><a href="./">Volver sin cambiarla</a></p>
</form>
<?php else: ?>
<main>
  <header>
    <h1>Visitas del <a href="https://diarioiaeducativa.github.io/" target="_blank" rel="noopener">Diario de IA Educativa</a></h1>
    <p class="aviso">Al día a las <span id="hora">…</span> · <a href="?clave">Cambiar contraseña</a> · <a href="?salir">Salir</a></p>
    <?php if (isset($_GET['cambiada'])): ?><p class="aviso" role="status">Contraseña cambiada.</p><?php endif; ?>
  </header>
  <p class="aviso">Una visita es una persona que entra en el diario; si vuelve tras 30 minutos sin abrir ninguna página, cuenta otra vez. Los días van en hora de España.</p>
  <div class="cifras">
    <div class="cifra"><b id="c-hoy">–</b><span>visitas hoy</span></div>
    <div class="cifra"><b id="c-semana">–</b><span>visitas en 7 días</span></div>
    <div class="cifra"><b id="c-mes">–</b><span>visitas en 30 días</span></div>
  </div>
  <h2>Visitas por día, últimos 30 días</h2>
  <div class="caja"><svg id="grafica" viewBox="0 0 600 200" role="img" aria-label="Visitas por día en los últimos 30 días"></svg></div>
  <h2>Páginas más abiertas</h2>
  <div class="periodos" role="group" aria-label="Periodo">
    <button type="button" data-p="hoy">Hoy</button><button type="button" data-p="7">7 días</button><button type="button" data-p="30">30 días</button><button type="button" data-p="90">90 días</button><button type="button" data-p="todo">Todo</button>
  </div>
  <p class="idiomas" id="idiomas"></p>
  <div class="caja" style="margin-top:.6rem"><table><tbody id="top"></tbody></table></div>
  <p class="aviso" style="margin-top:1rem">Cada página suma una vez por visita. Sin cookies ni datos de quien lee: solo sumas por hora, que se borran a los 25 meses. Las visitas desde los navegadores en los que habéis abierto este panel no cuentan. Para que tampoco cuente otro navegador, abre allí una vez <a href="https://diarioiaeducativa.github.io/redaccion.html?nocontar=1" target="_blank" rel="noopener">el diario con esta dirección</a> (<a href="https://diarioiaeducativa.github.io/redaccion.html?nocontar=0" target="_blank" rel="noopener">volver a contar</a>).</p>
</main>
<script>
(function(){
  var periodo = '7', IDI = {es:'castellano', ca:'catalán', gl:'gallego', eu:'euskera', en:'inglés'};
  var fmt = new Intl.NumberFormat('es-ES');
  function el(id){ return document.getElementById(id); }
  function texto(t){ var d=document.createElement('div'); d.textContent=t; return d.innerHTML; }
  function grafica(serie){
    var W=600, H=200, abajo=24, arriba=18, max=Math.max(1, Math.max.apply(null, serie.map(function(s){return s.visitas;})));
    var ancho=W/Math.max(serie.length,30), svg='';
    serie.forEach(function(s,i){
      var h=(H-abajo-arriba)*s.visitas/max, x=i*ancho+2, y=H-abajo-h, d=s.dia.slice(8)+'/'+s.dia.slice(5,7);
      svg+='<rect x="'+x+'" y="'+y+'" width="'+(ancho-4)+'" height="'+h+'" rx="2" fill="var(--barra)"><title>'+d+': '+s.visitas+' visitas, '+s.paginas+' páginas</title></rect>';
      if(s.visitas) svg+='<text x="'+(x+(ancho-4)/2)+'" y="'+(y-3)+'" font-size="13" text-anchor="middle" fill="var(--tinta-2)">'+s.visitas+'</text>';
      if(i%5===0||i===serie.length-1) svg+='<text x="'+(x+(ancho-4)/2)+'" y="'+(H-5)+'" font-size="13" text-anchor="middle" fill="var(--tinta-2)">'+d+'</text>';
    });
    svg+='<line x1="0" x2="'+W+'" y1="'+(H-abajo)+'" y2="'+(H-abajo)+'" stroke="var(--linea)"/>';
    el('grafica').innerHTML=svg;
  }
  function pinta(d){
    el('hora').textContent=d.actualizado;
    el('c-hoy').textContent=fmt.format(d.hoy.visitas);
    el('c-semana').textContent=fmt.format(d.semana.visitas);
    el('c-mes').textContent=fmt.format(d.mes.visitas);
    grafica(d.serie);
    var total=0; for(var k in d.idiomas) total+=d.idiomas[k];
    el('idiomas').innerHTML = total ? '<span>Por idioma:</span>' + Object.keys(d.idiomas).filter(function(k){return d.idiomas[k];}).map(function(k){
      return '<span>'+IDI[k]+' '+Math.round(100*d.idiomas[k]/total)+' %</span>';}).join('') : '';
    el('top').innerHTML = d.top.length ? d.top.map(function(p){
      var url='https://diarioiaeducativa.github.io'+p.ruta, t=(p.titulo||p.ruta).replace(/ \| (Diario|Diari|Daily|Egunkaria).*$/,'');
      return '<tr><td><a href="'+texto(url)+'" target="_blank" rel="noopener">'+texto(t)+'</a><small>'+texto(p.ruta)+'</small></td><td class="n">'+fmt.format(p.n)+'</td></tr>';
    }).join('') : '<tr><td>Todavía no hay visitas en este periodo.</td></tr>';
  }
  function carga(){
    fetch('?datos=1&periodo='+encodeURIComponent(periodo), {cache:'no-store'})
      .then(function(r){ if(r.status===401){ location.reload(); throw 0; } return r.json(); })
      .then(pinta).catch(function(){});
  }
  document.querySelectorAll('.periodos button').forEach(function(b){
    b.setAttribute('aria-pressed', b.dataset.p===periodo ? 'true' : 'false');
    b.addEventListener('click', function(){
      periodo=b.dataset.p;
      document.querySelectorAll('.periodos button').forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true' : 'false'); });
      carga();
    });
  });
  carga();
  setInterval(function(){ if(!document.hidden) carga(); }, 60000);
  document.addEventListener('visibilitychange', function(){ if(!document.hidden) carga(); });
})();
</script>
<?php endif; ?>
</body>
</html>
