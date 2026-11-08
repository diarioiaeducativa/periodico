<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Contador de visitas del diario (ADR 0033): lo común al contador y al panel.
// Solo se guardan sumas por hora (UTC) y página; nada de quien lee.

declare(strict_types=1);

const DATOS = __DIR__ . '/data';
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
        borrar_antiguos($ahora);
    }
}

/** Una vez al día: fuera lo que pasa de 25 meses. */
function borrar_antiguos(DateTimeImmutable $ahora): void {
    $limite = $ahora->modify('-' . MESES_CONSERVADOS . ' months')->format('Y-m-d');
    foreach (glob(DATOS . '/????-??-??.json') ?: [] as $f) {
        if (basename($f, '.json') < $limite) {
            @unlink($f);
        }
    }
}

function es_robot(string $ua): bool {
    return $ua === '' || (bool) preg_match('/bot|crawl|spider|slurp|preview|lighthouse|headless|curl|wget|python|scrapy|monitor/i', $ua);
}
