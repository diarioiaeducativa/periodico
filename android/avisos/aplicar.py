# SPDX-License-Identifier: AGPL-3.0-or-later
"""Añade los avisos del número (ADR 0043) al proyecto que genera Bubblewrap.

    python3 android/avisos/aplicar.py

`bubblewrap update` rehace AndroidManifest.xml y Application.java, y no sabe nada de los avisos: por eso
el código vive aquí, en android/avisos/, y este guion lo copia y lo engancha. Se puede repetir sin
duplicar nada; android/construeix.sh lo ejecuta antes de compilar.
"""

import pathlib
import shutil

AQUI = pathlib.Path(__file__).resolve().parent
APP = AQUI.parent / "app" / "src" / "main"
PAQUETE = APP / "java" / "io" / "github" / "diarioiaeducativa"
MARCA = "<!-- avisos del número (ADR 0043) -->"

# Una TWA no pide internet, porque quien navega es Chrome; la comprobación del número sí lo necesita
PERMISOS = ["android.permission.INTERNET", "android.permission.POST_NOTIFICATIONS",
            "android.permission.RECEIVE_BOOT_COMPLETED"]

PIEZAS = f"""        {MARCA}
        <activity android:name=".AvisosActivity"
            android:exported="true"
            android:excludeFromRecents="true"
            android:noHistory="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar">
            <intent-filter>
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.BROWSABLE"/>
                <data android:scheme="diarioia" android:host="avisos"/>
            </intent-filter>
        </activity>
        <receiver android:name=".ComprobarNumero" android:exported="false">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED"/>
            </intent-filter>
        </receiver>
"""


def main():
    for f in (AQUI / "java").glob("*.java"):
        shutil.copy(f, PAQUETE / f.name)
    for f in (AQUI / "res").rglob("*.xml"):
        destino = APP / "res" / f.relative_to(AQUI / "res")
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, destino)

    manifiesto = APP / "AndroidManifest.xml"
    m = manifiesto.read_text()
    assert m.count("    <application") == 1 and m.count("    </application>") == 1, "el manifiesto ha cambiado de forma"
    for permiso in PERMISOS:   # uno a uno, por si el manifiesto ya trae alguno
        if f'android:name="{permiso}"' not in m:
            m = m.replace("    <application", f'    <uses-permission android:name="{permiso}"/>   {MARCA}\n    <application', 1)
    if MARCA + "\n        <activity" not in m and ".AvisosActivity" not in m:
        m = m.replace("    </application>", PIEZAS + "    </application>", 1)
    manifiesto.write_text(m)

    # Al abrir la app, los avisos se vuelven a programar: Android los borra si se fuerza su cierre
    aplicacion = PAQUETE / "Application.java"
    a = aplicacion.read_text()
    if "Avisos.reanudar" not in a:
        assert a.count("super.onCreate();") == 1, "Application.java ha cambiado de forma"
        a = a.replace("super.onCreate();", "super.onCreate();\n      Avisos.reanudar(this);   // ADR 0043", 1)
        aplicacion.write_text(a)
    print("avisos aplicados")


if __name__ == "__main__":
    main()
