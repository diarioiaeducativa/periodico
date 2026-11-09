// SPDX-License-Identifier: AGPL-3.0-or-later
package io.github.diarioiaeducativa;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * Lo despiertan la alarma de cada comprobación (ADR 0043) y, para volver a programarla, el arranque del
 * móvil y la actualización de la app. La red, fuera del hilo principal y con goAsync(), que da hasta
 * 10 segundos: las conexiones de Avisos esperan 10 como mucho.
 */
public class ComprobarNumero extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Context c = context.getApplicationContext();
        String accion = intent.getAction();
        if (Intent.ACTION_BOOT_COMPLETED.equals(accion) || Intent.ACTION_MY_PACKAGE_REPLACED.equals(accion)) {
            Avisos.reanudar(c);
            return;
        }
        if (!Avisos.activos(c)) return;
        PendingResult pendiente = goAsync();
        new Thread(() -> {
            try {
                Avisos.comprobar(c);
            } finally {
                pendiente.finish();
            }
        }).start();
    }
}
