<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Recibe el aviso del navegador (ADR 0033): p = página, n = 1 si empieza una visita, t = título.
// No guarda IP, navegador ni ningún identificador: solo suma.

declare(strict_types=1);
require __DIR__ . '/comun.php';

$origen = config()['origen'] ?? 'https://diarioiaeducativa.github.io';
header('Access-Control-Allow-Origin: ' . $origen);
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST' || ($_SERVER['HTTP_ORIGIN'] ?? '') !== $origen
    || es_robot($_SERVER['HTTP_USER_AGENT'] ?? '')) {
    http_response_code(204);
    exit;
}

$ruta = (string) ($_POST['p'] ?? '');
if (!preg_match('#^/[A-Za-z0-9/_.\-]{0,200}$#', $ruta) || str_contains($ruta, '..')) {
    $ruta = '';
}
$visita = ($_POST['n'] ?? '') === '1';
$titulo = trim(preg_replace('/\s+/u', ' ', mb_substr((string) ($_POST['t'] ?? ''), 0, 200)) ?? '');

if ($ruta !== '' || $visita) {
    sumar($ruta, $visita, $titulo);
}
http_response_code(204);
