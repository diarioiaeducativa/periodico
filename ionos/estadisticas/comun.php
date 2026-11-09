<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Contador de visitas del diario (ADR 0033): lo común al contador y al panel.
// Solo se guardan sumas por hora (UTC) y página; nada de quien lee. Pasados 25 meses queda el total
// de cada año.

declare(strict_types=1);

const DATOS = __DIR__ . '/data';
const TOTALES = DATOS . '/totales.json';   // sumas por día y por año de Madrid de los días ya cerrados
const MESES_CONSERVADOS = 25;      // la AEPD fija 25 meses como máximo
const MAX_PAGINAS_DIA = 5000;      // tope de páginas distintas por día, contra el relleno malintencionado

function config(): array {
    static $c = null;
    if (isset($GLOBALS['config_nueva'])) {   // recién cambiada una contraseña (index.php)
        return $GLOBALS['config_nueva'];
    }
    if ($c === null) {
        $c = is_file(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : [];
    }
    return $c;
}

function archivo_dia(string $fecha): string {
    return DATOS . '/' . $fecha . '.json';
}

/** Lee el día (UTC) $fecha: ['v' => [hora => n], 'p' => [ruta => [hora => n]], 't' => [ruta => título]]. */
function leer_dia(string $fecha): array {
    $f = archivo_dia($fecha);
    if (!is_file($f)) {
        return ['v' => [], 'p' => [], 't' => []];
    }
    $fp = fopen($f, 'rb');
    flock($fp, LOCK_SH);
    $txt = stream_get_contents($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    $d = json_decode((string) $txt, true);
    return is_array($d) ? $d + ['v' => [], 'p' => [], 't' => []] : ['v' => [], 'p' => [], 't' => []];
}

/** Suma una visita nueva y/o una apertura de página, leyendo y escribiendo dentro del mismo bloqueo. */
function sumar(string $ruta, bool $visita, string $titulo): void {
    if (!is_dir(DATOS)) {
        mkdir(DATOS, 0755, true);
    }
    $ahora = new DateTimeImmutable('now', new DateTimeZone('UTC'));
    $fecha = $ahora->format('Y-m-d');
    $hora = $ahora->format('H');
    $f = archivo_dia($fecha);
    $nuevo = !is_file($f);
    $fp = fopen($f, 'c+b');
    if (!$fp) {
        return;
    }
    flock($fp, LOCK_EX);
    $d = json_decode((string) stream_get_contents($fp), true);
    if (!is_array($d)) {
        $d = [];
    }
    $d += ['v' => [], 'p' => [], 't' => []];
    if ($visita) {
        $d['v'][$hora] = ($d['v'][$hora] ?? 0) + 1;
    }
    if ($ruta !== '' && (isset($d['p'][$ruta]) || count($d['p']) < MAX_PAGINAS_DIA)) {
        $d['p'][$ruta][$hora] = ($d['p'][$ruta][$hora] ?? 0) + 1;
        if ($titulo !== '') {
            $d['t'][$ruta] = $titulo;
        }
    }
    rewind($fp);
    ftruncate($fp, 0);
    fwrite($fp, json_encode($d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    if ($nuevo) {
        mantenimiento($ahora);
    }
}

/** El momento de Madrid de una hora UTC de un día. */
function en_madrid(string $fecha, string $hora): DateTimeImmutable {
    static $utc = null, $madrid = null;
    $utc ??= new DateTimeZone('UTC');
    $madrid ??= new DateTimeZone('Europe/Madrid');
    return (new DateTimeImmutable($fecha . ' ' . $hora . ':00:00', $utc))->setTimezone($madrid);
}

/** Las sumas de un día UTC por hora: ['00' => [visitas, páginas abiertas], …]. */
function horas_dia(string $fecha): array {
    $d = leer_dia($fecha);
    $h = [];
    foreach ($d['v'] as $hora => $n) {
        $k = sprintf('%02d', (int) $hora);
        $h[$k] = [($h[$k][0] ?? 0) + (int) $n, $h[$k][1] ?? 0];
    }
    foreach ($d['p'] as $horas) {
        foreach ($horas as $hora => $n) {
            $k = sprintf('%02d', (int) $hora);
            $h[$k] = [$h[$k][0] ?? 0, ($h[$k][1] ?? 0) + (int) $n];
        }
    }
    return $h;
}

/** Suma un día UTC a las cuentas por día y por año de Madrid: [clave => [visitas, páginas abiertas]]. */
function repartir(string $fecha, array &$dias, array &$anios): void {
    foreach (horas_dia($fecha) as $hora => [$v, $p]) {
        $m = en_madrid($fecha, sprintf('%02d', (int) $hora));
        $dia = $m->format('Y-m-d');
        $anio = $m->format('Y');
        $dias[$dia] = [($dias[$dia][0] ?? 0) + $v, ($dias[$dia][1] ?? 0) + $p];
        $anios[$anio] = [($anios[$anio][0] ?? 0) + $v, ($anios[$anio][1] ?? 0) + $p];
    }
}

/**
 * Los totales de los días ya cerrados: ['hasta' => último día UTC sumado, 'dias' => […], 'anios' => […]].
 * null si el archivo está pero no se entiende: entonces no se toca nada, para no perder los años.
 */
function leer_totales(): ?array {
    if (!is_file(TOTALES)) {
        return ['hasta' => '', 'dias' => [], 'anios' => []];
    }
    $t = json_decode((string) file_get_contents(TOTALES), true);
    return is_array($t) && isset($t['hasta'], $t['dias'], $t['anios']) && is_array($t['dias']) && is_array($t['anios']) ? $t : null;
}

/**
 * Una vez al día, al llegar la primera visita. Suma a los totales los días cerrados (hasta anteayer
 * UTC: en el de ayer aún podría estar escribiendo una petición rezagada) y borra el detalle de más de
 * 25 meses. De lo borrado queda solo el total de su año. Cada día se suma una sola vez: «hasta» se
 * guarda en el mismo archivo que las sumas, que se sustituye de golpe.
 */
function mantenimiento(DateTimeImmutable $ahora): void {
    $cerrojo = fopen(DATOS . '/totales.lock', 'cb');
    if (!$cerrojo) {
        return;
    }
    flock($cerrojo, LOCK_EX);
    $t = leer_totales();
    if ($t !== null) {
        $ayer = $ahora->modify('-1 day')->format('Y-m-d');
        $limite = $ahora->modify('-' . MESES_CONSERVADOS . ' months')->format('Y-m-d');
        $archivos = glob(DATOS . '/????-??-??.json') ?: [];
        $hasta = $t['hasta'];
        foreach ($archivos as $f) {
            $fecha = basename($f, '.json');
            if ($fecha > $t['hasta'] && $fecha < $ayer) {
                repartir($fecha, $t['dias'], $t['anios']);
                $hasta = $fecha;
            }
        }
        $t['hasta'] = $hasta;
        foreach (array_keys($t['dias']) as $dia) {
            if ($dia < $limite) {
                unset($t['dias'][$dia]);
            }
        }
        ksort($t['dias']);
        ksort($t['anios']);
        $tmp = TOTALES . '.tmp';
        $guardado = file_put_contents($tmp, json_encode($t)) !== false && rename($tmp, TOTALES);
        if ($guardado) {
            foreach ($archivos as $f) {
                $fecha = basename($f, '.json');
                if ($fecha < $limite && $fecha <= $t['hasta']) {   // solo lo que ya está en los totales
                    @unlink($f);
                }
            }
        }
    }
    flock($cerrojo, LOCK_UN);
    fclose($cerrojo);
}

/** Las sumas al día por día y por año de Madrid: los totales guardados más los días aún sin sumar. */
function sumas_al_dia(): array {
    $t = leer_totales() ?? ['hasta' => '', 'dias' => [], 'anios' => []];
    $dias = $t['dias'];
    $anios = $t['anios'];
    foreach (glob(DATOS . '/????-??-??.json') ?: [] as $f) {
        $fecha = basename($f, '.json');
        if ($fecha > $t['hasta']) {
            repartir($fecha, $dias, $anios);
        }
    }
    ksort($dias);
    ksort($anios);
    return [$dias, $anios];
}

function es_robot(string $ua): bool {
    return $ua === '' || (bool) preg_match('/bot|crawl|spider|slurp|preview|lighthouse|headless|curl|wget|python|scrapy|monitor/i', $ua);
}
