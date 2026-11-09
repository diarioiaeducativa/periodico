// SPDX-License-Identifier: AGPL-3.0-or-later
package io.github.diarioiaeducativa;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Toast;

/**
 * La ventana de «Avisos del número» (ADR 0043), que abre el enlace del pie de la app
 * (intent://avisos?idioma=XX#Intent;scheme=diarioia;…). Dice qué hacen los avisos, deja encenderlos o
 * apagarlos y, al encenderlos, pide el permiso de notificaciones si Android lo exige. Sin pantalla
 * propia: solo el cuadro de diálogo, sobre la app, con el tema claro u oscuro del sistema.
 */
public class AvisosActivity extends Activity {
    private static final int PERMISO = 1;

    @Override
    protected void onCreate(Bundle guardado) {
        super.onCreate(guardado);
        Uri d = getIntent().getData();
        String idioma = d != null ? d.getQueryParameter("idioma") : null;
        if (idioma != null && Avisos.IDIOMAS.contains(idioma)) {
            Avisos.prefs(this).edit().putString("idioma", idioma).apply();
        }
        mostrar();
    }

    private int tema() {
        boolean oscuro = (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK)
                == Configuration.UI_MODE_NIGHT_YES;
        return oscuro ? android.R.style.Theme_DeviceDefault_Dialog_Alert
                : android.R.style.Theme_DeviceDefault_Light_Dialog_Alert;
    }

    private void mostrar() {
        Context l = Avisos.localizado(this);
        boolean activos = Avisos.activos(this) && Avisos.permitidas(this);
        new AlertDialog.Builder(this, tema())
                .setTitle(l.getString(R.string.avisos_dialogo))
                .setMessage(l.getString(activos ? R.string.avisos_texto_activos : R.string.avisos_texto))
                .setPositiveButton(l.getString(activos ? R.string.avisos_desactivar : R.string.avisos_activar),
                        (dialogo, boton) -> { if (activos) apagar(); else activar(); })
                .setNegativeButton(l.getString(activos ? R.string.avisos_cerrar : R.string.avisos_ahora_no),
                        (dialogo, boton) -> finish())
                .setOnCancelListener(dialogo -> finish())
                .show();
    }

    private void activar() {
        if (Build.VERSION.SDK_INT >= 33
                && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[] {Manifest.permission.POST_NOTIFICATIONS}, PERMISO);
            return;
        }
        if (!Avisos.permitidas(this)) {
            sinPermiso();
            return;
        }
        encender();
    }

    @Override
    public void onRequestPermissionsResult(int codigo, String[] permisos, int[] resultados) {
        if (codigo != PERMISO) return;
        if (resultados.length > 0 && resultados[0] == PackageManager.PERMISSION_GRANTED && Avisos.permitidas(this)) {
            encender();
        } else {
            sinPermiso();
        }
    }

    private void encender() {
        Avisos.encender(this);
        Toast.makeText(this, Avisos.localizado(this).getString(R.string.avisos_activados), Toast.LENGTH_SHORT).show();
        finish();
    }

    private void apagar() {
        Avisos.apagar(this);
        Toast.makeText(this, Avisos.localizado(this).getString(R.string.avisos_desactivados), Toast.LENGTH_SHORT).show();
        finish();
    }

    /** Android no deja volver a pedir el permiso si se negó: se lleva a sus ajustes. */
    private void sinPermiso() {
        Context l = Avisos.localizado(this);
        new AlertDialog.Builder(this, tema())
                .setTitle(l.getString(R.string.avisos_dialogo))
                .setMessage(l.getString(R.string.avisos_sin_permiso))
                .setPositiveButton(l.getString(R.string.avisos_ajustes), (dialogo, boton) -> {
                    Intent ajustes = Build.VERSION.SDK_INT >= 26
                            ? new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                                    .putExtra(Settings.EXTRA_APP_PACKAGE, getPackageName())
                            : new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                                    Uri.parse("package:" + getPackageName()));
                    startActivity(ajustes);
                    finish();
                })
                .setNegativeButton(l.getString(R.string.avisos_cerrar), (dialogo, boton) -> finish())
                .setOnCancelListener(dialogo -> finish())
                .show();
    }
}
