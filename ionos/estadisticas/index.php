<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Panel privado de las visitas del diario (ADR 0033), para sus dos autores. Lee las sumas en el
// momento; se guardan por hora en UTC y se muestran en hora de Madrid: por horas, días, semanas, meses o años.

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

/** Las páginas abiertas entre dos días de Madrid (incluidos), con sus títulos. */
function paginas(DateTimeImmutable $desde, DateTimeImmutable $hasta): array {
    global $UTC;
    $d1 = $desde->format('Y-m-d');
    $d2 = $hasta->format('Y-m-d');
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
        foreach ($datos['p'] as $ruta => $horas) {
            foreach ($horas as $hora => $n) {
                $dm = en_madrid($fecha, sprintf('%02d', (int) $hora))->format('Y-m-d');
                if ($dm >= $d1 && $dm <= $d2) {
                    $paginas[$ruta] = ($paginas[$ruta] ?? 0) + $n;
                }
            }
        }
        $titulos = ($datos['t'] ?? []) + $titulos;
    }
    return [$paginas, $titulos];
}

function idioma(string $ruta): string {
    return preg_match('#^/(ca|gl|eu|en)/#', $ruta, $m) ? $m[1] : 'es';
}

/**
 * La serie de la gráfica: una barra por hora, día, semana, mes o año, de más antigua a más reciente.
 * Cada punto: c (clave: la hora en UTC, el día, el lunes de la semana, el mes o el año), v (visitas)
 * y p (páginas abiertas). Las horas se piden en UTC y el navegador las pinta en hora de Madrid.
 */
function serie(string $tipo, array $dias, array $anios, DateTimeImmutable $hoy): array {
    global $UTC;
    $entre = function (string $d1, string $d2) use ($dias): array {
        $v = $p = 0;
        foreach ($dias as $d => $x) {
            if ($d >= $d1 && $d <= $d2) {
                $v += $x[0];
                $p += $x[1];
            }
        }
        return ['v' => $v, 'p' => $p];
    };
    $primero = array_key_first($dias);   // el primer día con datos: la gráfica no empieza con ceros
    $puntos = [];
    if ($tipo === 'hora') {
        $ahora = new DateTimeImmutable('now', $UTC);
        $leidos = [];
        for ($i = 23; $i >= 0; $i--) {
            $h = $ahora->modify('-' . $i . ' hours');
            $fecha = $h->format('Y-m-d');
            $leidos[$fecha] ??= horas_dia($fecha);
            $x = $leidos[$fecha][$h->format('H')] ?? [0, 0];
            $puntos[] = ['c' => $h->format('Y-m-d\TH:00:00\Z'), 'v' => $x[0], 'p' => $x[1]];
        }
    } elseif ($tipo === 'semana') {
        $lunes = $hoy->modify('monday this week');
        for ($i = 11; $i >= 0; $i--) {
            $l = $lunes->modify('-' . $i . ' weeks');
            $domingo = $l->modify('+6 days')->format('Y-m-d');
            if ($primero === null || $domingo < $primero) {
                continue;
            }
            $puntos[] = ['c' => $l->format('Y-m-d')] + $entre($l->format('Y-m-d'), $domingo);
        }
    } elseif ($tipo === 'mes') {
        $este = $hoy->modify('first day of this month');
        for ($i = 23; $i >= 0; $i--) {
            $m = $este->modify('-' . $i . ' months');
            if ($primero === null || $m->format('Y-m') < substr($primero, 0, 7)) {
                continue;
            }
            $puntos[] = ['c' => $m->format('Y-m')] + $entre($m->format('Y-m-01'), $m->format('Y-m-t'));
        }
    } elseif ($tipo === 'anio') {
        $a1 = $anios ? (int) array_key_first($anios) : (int) $hoy->format('Y');
        for ($a = $a1; $a <= (int) $hoy->format('Y'); $a++) {
            $puntos[] = ['c' => (string) $a, 'v' => $anios[$a][0] ?? 0, 'p' => $anios[$a][1] ?? 0];
        }
    } else {
        $ini = $hoy->modify('-29 days');
        if ($primero !== null && $primero > $ini->format('Y-m-d')) {
            $ini = new DateTimeImmutable($primero, $hoy->getTimezone());
        }
        for ($d = $ini; $d <= $hoy; $d = $d->modify('+1 day')) {
            $k = $d->format('Y-m-d');
            $puntos[] = ['c' => $k, 'v' => $dias[$k][0] ?? 0, 'p' => $dias[$k][1] ?? 0];
        }
    }
    return $puntos;
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
    $tipo = (string) ($_GET['serie'] ?? 'dia');
    if (!in_array($tipo, ['hora', 'dia', 'semana', 'mes', 'anio'], true)) {
        $tipo = 'dia';
    }
    [$dias, $anios] = sumas_al_dia();
    $suma = function (int $k) use ($dias, $hoy): array {
        $desde = $hoy->modify('-' . ($k - 1) . ' days')->format('Y-m-d');
        $v = $p = 0;
        foreach ($dias as $d => $x) {
            if ($d >= $desde) {
                $v += $x[0];
                $p += $x[1];
            }
        }
        return ['visitas' => $v, 'paginas' => $p];
    };
    // Las páginas y los idiomas, solo del periodo elegido
    [$paginas, $titulos] = paginas($hoy->modify('-' . ($n - 1) . ' days'), $hoy);
    arsort($paginas);
    $idiomas = ['es' => 0, 'ca' => 0, 'gl' => 0, 'eu' => 0, 'en' => 0];
    foreach ($paginas as $r => $c) {
        $idiomas[idioma($r)] += $c;
    }
    $top = [];
    foreach (array_slice($paginas, 0, 30, true) as $r => $c) {
        $top[] = ['ruta' => $r, 'titulo' => $titulos[$r] ?? '', 'n' => $c];
    }
    echo json_encode([
        'hoy' => $suma(1), 'semana' => $suma(7), 'mes' => $suma(30),
        'periodo' => $periodo, 'top' => $top, 'idiomas' => $idiomas,
        'tipo' => $tipo, 'serie' => serie($tipo, $dias, $anios, $hoy),
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
svg { display:block; width:100%; height:200px; touch-action:pan-y; }
svg .b { fill:var(--barra); }
svg .b.sel { fill:var(--tinta); }
svg text { font-size:13px; fill:var(--tinta-2); text-anchor:middle; font-variant-numeric:tabular-nums; }
.detalle { margin:.5rem 0 0; font-size:.95rem; min-height:1.45em; }
.periodos + .aviso { margin-top:.5rem; }
.periodos + .caja, .aviso + .caja { margin-top:.6rem; }
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
  <h2>Visitas en el tiempo</h2>
  <div class="periodos" id="series" role="group" aria-label="Qué cuenta cada barra de la gráfica">
    <button type="button" data-s="hora">Horas</button><button type="button" data-s="dia">Días</button><button type="button" data-s="semana">Semanas</button><button type="button" data-s="mes">Meses</button><button type="button" data-s="anio">Años</button>
  </div>
  <p class="aviso" id="resumen">&nbsp;</p>
  <div class="caja"><svg id="grafica" role="img"></svg><p class="detalle" id="detalle" aria-live="polite">&nbsp;</p></div>
  <h2>Páginas más abiertas</h2>
  <div class="periodos" id="periodos" role="group" aria-label="Periodo">
    <button type="button" data-p="hoy">Hoy</button><button type="button" data-p="7">7 días</button><button type="button" data-p="30">30 días</button><button type="button" data-p="90">90 días</button><button type="button" data-p="todo">Todo</button>
  </div>
  <p class="idiomas" id="idiomas"></p>
  <div class="caja" style="margin-top:.6rem"><table><tbody id="top"></tbody></table></div>
  <p class="aviso" style="margin-top:1rem">Cada página suma una vez por visita. Sin cookies ni datos de quien lee: solo sumas por hora, que se borran a los 25 meses; de lo anterior queda el total de cada año. Las visitas desde los navegadores en los que habéis abierto este panel no cuentan. Para que tampoco cuente otro navegador, abre allí una vez <a href="https://diarioiaeducativa.github.io/redaccion.html?nocontar=1" target="_blank" rel="noopener">el diario con esta dirección</a>.</p>
</main>
<script>
(function(){
  var periodo = '7', serie = 'dia', datos = null, elegida = null;
  var IDI = {es:'castellano', ca:'catalán', gl:'gallego', eu:'euskera', en:'inglés'};
  var fmt = new Intl.NumberFormat('es-ES');
  function el(id){ return document.getElementById(id); }
  function texto(t){ var d=document.createElement('div'); d.textContent=t; return d.innerHTML; }
  function cuantas(n, uno, varios){ return fmt.format(n)+' '+(n===1 ? uno : varios); }
  function sumas(v, p){ return cuantas(v,'visita','visitas')+' · '+cuantas(p,'página abierta','páginas abiertas'); }
  function mayus(t){ return t.charAt(0).toUpperCase()+t.slice(1); }

  // Las fechas, siempre en hora de España, esté donde esté quien mira
  var TZ = 'Europe/Madrid';
  var fDia = new Intl.DateTimeFormat('es-ES', {weekday:'long', day:'numeric', month:'long', timeZone:TZ});
  var fDiaMes = new Intl.DateTimeFormat('es-ES', {day:'numeric', month:'long', timeZone:TZ});
  var fMes = new Intl.DateTimeFormat('es-ES', {month:'long', year:'numeric', timeZone:TZ});
  var fMesCorto = new Intl.DateTimeFormat('es-ES', {month:'short', timeZone:TZ});
  var fPartes = new Intl.DateTimeFormat('es-ES', {day:'numeric', month:'numeric', hour:'numeric', hourCycle:'h23', timeZone:TZ});
  function mediodia(c){ return new Date(c+'T12:00:00Z'); }   // un día, sin que la zona lo cambie
  function partes(f){ var o={}; fPartes.formatToParts(f).forEach(function(x){ o[x.type]=+x.value; }); return o; }
  function semana(f){   // número de semana ISO, el mismo que usa el diario
    var d=new Date(Date.UTC(f.getUTCFullYear(), f.getUTCMonth(), f.getUTCDate()));
    d.setUTCDate(d.getUTCDate()+4-(d.getUTCDay()||7));
    return Math.ceil(((d-Date.UTC(d.getUTCFullYear(),0,1))/864e5+1)/7);
  }
  // De cada clase de barra: de cuándo es todo lo que se ve, su rótulo corto y su nombre completo
  var SERIES = {
    hora: {rango:'Últimas 24 horas', hueco:24,
      corto:function(c){ return partes(new Date(c)).hour+' h'; },
      largo:function(c){ var f=new Date(c), h=partes(f).hour; return mayus(fDia.format(f))+', de '+h+' a '+((h+1)%24)+' h'; }},
    dia: {rango:'Últimos 30 días', hueco:30,
      corto:function(c){ return c.slice(8)+'/'+c.slice(5,7); },
      largo:function(c){ return mayus(fDia.format(mediodia(c))); }},
    semana: {rango:'Últimas 12 semanas, de lunes a domingo', hueco:12,
      corto:function(c){ return 'S'+semana(mediodia(c)); },
      largo:function(c){
        var l=mediodia(c), d=new Date(+l+6*864e5), mismo=l.getUTCMonth()===d.getUTCMonth();
        return 'Semana '+semana(l)+', del '+(mismo ? l.getUTCDate() : fDiaMes.format(l))+' al '+fDiaMes.format(d);
      }},
    mes: {rango:'Últimos 24 meses', hueco:24,
      corto:function(c){ return fMesCorto.format(mediodia(c+'-15')).replace('.','')+' '+c.slice(2,4); },
      largo:function(c){ return mayus(fMes.format(mediodia(c+'-15'))); }},
    anio: {rango:'Todos los años', hueco:6,
      corto:function(c){ return c; },
      largo:function(c){ return 'Año '+c; }}
  };

  function detalle(){
    if(!datos || !datos.serie.length){ el('detalle').innerHTML='&nbsp;'; return; }
    var i = elegida===null ? datos.serie.length-1 : elegida, s=datos.serie[i];
    el('detalle').innerHTML='<b>'+texto(SERIES[datos.tipo].largo(s.c))+':</b> '+sumas(s.v, s.p);
    document.querySelectorAll('#grafica .b').forEach(function(b){ b.classList.toggle('sel', elegida!==null && +b.dataset.i===elegida); });
  }
  function grafica(){
    var S=SERIES[datos.tipo], serie=datos.serie, svg=el('grafica');
    var W=Math.max(280, svg.clientWidth||600), H=200, abajo=24, arriba=20;
    var max=Math.max(1, Math.max.apply(null, serie.map(function(s){return s.v;})));
    var paso=W/Math.max(serie.length, S.hueco), barra=Math.min(paso-Math.min(4, paso*.3), 48), h='';
    var tv=0, tp=0; serie.forEach(function(s){ tv+=s.v; tp+=s.p; });
    el('resumen').textContent=S.rango+': '+sumas(tv, tp);
    svg.setAttribute('viewBox', '0 0 '+W+' '+H);
    svg.setAttribute('aria-label', 'Gráfica de visitas. '+S.rango+': '+sumas(tv, tp)+'.');
    // Los rótulos de abajo, cada tantos como quepan, contando desde la barra más reciente
    var anchoRotulo=Math.max.apply(null, serie.map(function(s){return S.corto(s.c).length;}).concat(1))*7.5+10;
    var cada=Math.max(1, Math.ceil(anchoRotulo/paso));
    // Las cifras de arriba, en todas las barras si caben; si no, solo en la más alta y en la última
    var todas=fmt.format(max).length*8+4 <= paso, iMax=-1;
    serie.forEach(function(s,i){ if(s.v===max && iMax<0) iMax=i; });
    serie.forEach(function(s,i){
      var alto=(H-abajo-arriba)*s.v/max, x=i*paso+(paso-barra)/2, y=H-abajo-alto, medio=i*paso+paso/2;
      if(alto) h+='<rect class="b" data-i="'+i+'" x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+barra.toFixed(1)+'" height="'+alto.toFixed(1)+'" rx="2"/>';
      var ultima=i===serie.length-1, lejos=Math.abs(i-iMax)*paso > fmt.format(max).length*8+12;
      var mitad=fmt.format(s.v).length*4+1;   // la cifra no se sale por los lados
      if(s.v && (todas || i===iMax || (ultima && lejos))) h+='<text x="'+Math.min(Math.max(medio, mitad), W-mitad).toFixed(1)+'" y="'+(y-4).toFixed(1)+'">'+fmt.format(s.v)+'</text>';
      if((serie.length-1-i)%cada===0) h+='<text x="'+Math.min(Math.max(medio, anchoRotulo/2-4), W-anchoRotulo/2+4).toFixed(1)+'" y="'+(H-6)+'">'+texto(S.corto(s.c))+'</text>';
    });
    h+='<line x1="0" x2="'+W+'" y1="'+(H-abajo)+'" y2="'+(H-abajo)+'" stroke="var(--linea)"/>';
    // Encima, una franja por barra de arriba abajo, para acertar con el dedo
    serie.forEach(function(s,i){
      h+='<rect data-i="'+i+'" x="'+(i*paso).toFixed(1)+'" y="0" width="'+paso.toFixed(1)+'" height="'+H+'" fill="transparent"><title>'+texto(S.largo(s.c)+': '+sumas(s.v, s.p))+'</title></rect>';
    });
    svg.innerHTML=h;
    if(elegida!==null && elegida>=serie.length) elegida=null;
    detalle();
  }
  function pinta(d){
    el('hora').textContent=d.actualizado;
    el('c-hoy').textContent=fmt.format(d.hoy.visitas);
    el('c-semana').textContent=fmt.format(d.semana.visitas);
    el('c-mes').textContent=fmt.format(d.mes.visitas);
    if(datos && datos.tipo!==d.tipo) elegida=null;
    datos=d;
    grafica();
    var total=0; for(var k in d.idiomas) total+=d.idiomas[k];
    el('idiomas').innerHTML = total ? '<span>Por idioma:</span>' + Object.keys(d.idiomas).filter(function(k){return d.idiomas[k];}).map(function(k){
      return '<span>'+IDI[k]+' '+Math.round(100*d.idiomas[k]/total)+' %</span>';}).join('') : '';
    el('top').innerHTML = d.top.length ? d.top.map(function(p){
      var url='https://diarioiaeducativa.github.io'+p.ruta, t=(p.titulo||p.ruta).replace(/ \| (Diario|Diari|Daily|Egunkaria).*$/,'');
      return '<tr><td><a href="'+texto(url)+'" target="_blank" rel="noopener">'+texto(t)+'</a><small>'+texto(p.ruta)+'</small></td><td class="n">'+fmt.format(p.n)+'</td></tr>';
    }).join('') : '<tr><td>Todavía no hay visitas en este periodo.</td></tr>';
  }
  function carga(){
    fetch('?datos=1&periodo='+encodeURIComponent(periodo)+'&serie='+serie, {cache:'no-store'})
      .then(function(r){ if(r.status===401){ location.reload(); throw 0; } return r.json(); })
      .then(pinta).catch(function(){});
  }
  // Los dos grupos de botones: qué cuenta cada barra y de qué periodo son las páginas
  function botones(grupo, dato, actual, alElegir){
    var bs=document.querySelectorAll('#'+grupo+' button');
    bs.forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset[dato]===actual ? 'true' : 'false');
      b.addEventListener('click', function(){
        bs.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true' : 'false'); });
        alElegir(b.dataset[dato]);
        carga();
      });
    });
  }
  botones('series', 's', serie, function(v){ serie=v; });
  botones('periodos', 'p', periodo, function(v){ periodo=v; });
  // Al pasar el ratón o tocar una barra, su detalle debajo; con el ratón fuera, vuelve la más reciente
  var g=el('grafica');
  function elige(e){ var i=e.target && e.target.dataset ? e.target.dataset.i : undefined; if(i!==undefined && +i!==elegida){ elegida=+i; detalle(); } }
  g.addEventListener('pointermove', elige);
  g.addEventListener('click', elige);
  g.addEventListener('pointerleave', function(e){ if(e.pointerType==='mouse'){ elegida=null; detalle(); } });
  var ancho=0;
  window.addEventListener('resize', function(){ if(datos && g.clientWidth!==ancho){ ancho=g.clientWidth; grafica(); } });
  carga();
  setInterval(function(){ if(!document.hidden) carga(); }, 60000);
  document.addEventListener('visibilitychange', function(){ if(!document.hidden) carga(); });
})();
</script>
<?php endif; ?>
</body>
</html>
