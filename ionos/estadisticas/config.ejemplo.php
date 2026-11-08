<?php
// SPDX-License-Identifier: AGPL-3.0-or-later
// Copia como config.php en el hosting (no va al repositorio). Las contraseñas, con password_hash().
return [
    'origen' => 'https://diarioiaeducativa.github.io',
    'secreto' => 'una cadena aleatoria larga, para firmar la sesión',
    'usuarios' => [
        'juanjo' => '$2y$10$...',
        'raul' => '$2y$10$...',
    ],
];
