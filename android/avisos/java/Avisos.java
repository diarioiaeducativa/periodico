// SPDX-License-Identifier: AGPL-3.0-or-later
package io.github.diarioiaeducativa;

import android.Manifest;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Build;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;

/**
 * Los avisos del número (ADR 0043), sin servidor: el propio móvil mira cada mañana ultimo.json del
 * diario publicado y, si ya ha salido el número del día, lo avisa con una notificación. Apagados de
 * serie; se encienden y se apagan desde «Avisos del número», en el pie de la app (AvisosActivity).
 *
 * Las horas se calculan en Europe/Madrid, porque el diario sale a las 7:00 de allí, y se guardan y se
 * programan en milisegundos desde 1970 (UTC): el cambio de hora no las mueve. Sin alarmas exactas, que
 * Google Play reserva a despertadores y calendarios: Android puede retrasar la comprobación unos minutos,
 * y la adelanta si el móvil se despierta antes.
 */
final class Avisos {
    static final String WEB = "https://diarioiaeducativa.github.io/ultimo.json";
    static final TimeZone MADRID = TimeZone.getTimeZone("Europe/Madrid");
    static final List<String> IDIOMAS = Arrays.asList("es", "ca", "gl", "eu", "en");
    static final int HORA = 7, FIN_HORA = 9, FIN_MINUTO = 30;   // la primera, a las 7:00; la última, a las 9:30
    static final long REINTENTO = 15 * 60 * 1000L;
    private static final String CANAL = "numero";

    private Avisos() {}

    static SharedPreferences prefs(Context c) {
        return c.getSharedPreferences("avisos", Context.MODE_PRIVATE);
    }

    static boolean activos(Context c) {
        return prefs(c).getBoolean("activos", false);
    }

    /** El idioma que se eligió en el diario al abrir los avisos; si no, el del móvil, o castellano. */
    static String idioma(Context c) {
        String elegido = prefs(c).getString("idioma", null);
        if (elegido != null && IDIOMAS.contains(elegido)) return elegido;
        String sistema = Locale.getDefault().getLanguage();
        return IDIOMAS.contains(sistema) ? sistema : "es";
    }

    /** Los textos en el idioma del diario, aunque el móvil esté en otro. */
    static Context localizado(Context c) {
        Configuration cf = new Configuration(c.getResources().getConfiguration());
        cf.setLocale(new Locale(idioma(c)));
        return c.createConfigurationContext(cf);
    }

    static boolean permitidas(Context c) {
        if (Build.VERSION.SDK_INT >= 33
                && c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            return false;
        }
        return c.getSystemService(NotificationManager.class).areNotificationsEnabled();
    }

    /** El día de hoy en Madrid, AAAA-MM-DD, como «sale» en ultimo.json. */
    static String hoy() {
        Calendar k = Calendar.getInstance(MADRID);
        return String.format(Locale.ROOT, "%04d-%02d-%02d",
                k.get(Calendar.YEAR), k.get(Calendar.MONTH) + 1, k.get(Calendar.DAY_OF_MONTH));
    }

    /** Una hora de Madrid, hoy o dentro de unos días, en milisegundos UTC. */
    static long hora(int dias, int h, int m) {
        Calendar k = Calendar.getInstance(MADRID);
        k.add(Calendar.DAY_OF_YEAR, dias);
        k.set(Calendar.HOUR_OF_DAY, h);
        k.set(Calendar.MINUTE, m);
        k.set(Calendar.SECOND, 0);
        k.set(Calendar.MILLISECOND, 0);
        return k.getTimeInMillis();
    }

    private static PendingIntent pendiente(Context c) {
        Intent i = new Intent(c, ComprobarNumero.class);
        return PendingIntent.getBroadcast(c, 0, i, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
    }

    static void programar(Context c, long cuando) {
        c.getSystemService(AlarmManager.class).setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, cuando, pendiente(c));
        prefs(c).edit().putLong("proxima", cuando).apply();
    }

    /** Hoy, si aún no se ha avisado y no han pasado las 9:30; si no, mañana a las 7:00. */
    static void programarSiguiente(Context c) {
        long ahora = System.currentTimeMillis();
        boolean avisado = hoy().equals(prefs(c).getString("avisado", ""));
        if (!avisado && ahora < hora(0, FIN_HORA, FIN_MINUTO)) {
            programar(c, Math.max(ahora, hora(0, HORA, 0)));
        } else {
            programar(c, hora(1, HORA, 0));
        }
    }

    /** Al encenderlos desde la app, el número de hoy ya se está viendo: el primer aviso, mañana. */
    static void encender(Context c) {
        SharedPreferences.Editor e = prefs(c).edit().putBoolean("activos", true);
        if (System.currentTimeMillis() >= hora(0, HORA, 0)) e.putString("avisado", hoy());
        e.apply();
        programarSiguiente(c);
    }

    static void apagar(Context c) {
        prefs(c).edit().putBoolean("activos", false).apply();
        c.getSystemService(AlarmManager.class).cancel(pendiente(c));
    }

    /** Al abrir la app o al encender el móvil: las alarmas no sobreviven a un reinicio ni a una actualización. */
    static void reanudar(Context c) {
        if (activos(c)) programarSiguiente(c);
    }

    /** Lo que hace cada comprobación; corre fuera del hilo principal (ComprobarNumero). */
    static void comprobar(Context c) {
        if (!activos(c)) return;
        String hoy = hoy();
        try {
            JSONObject u = leer();
            if (hoy.equals(u.getString("sale"))) {
                if (!hoy.equals(prefs(c).getString("avisado", ""))) {
                    notificar(c, u);
                    prefs(c).edit().putString("avisado", hoy).apply();
                }
                programar(c, hora(1, HORA, 0));
                return;
            }
        } catch (Exception sinRed) {
            // sin conexión o la web no responde: se vuelve a mirar como si aún no hubiera salido
        }
        long siguiente = System.currentTimeMillis() + REINTENTO;
        programar(c, siguiente <= hora(0, FIN_HORA, FIN_MINUTO) ? siguiente : hora(1, HORA, 0));
    }

    private static JSONObject leer() throws Exception {
        // La consulta distinta cada vez salta la caché de GitHub Pages (10 minutos)
        HttpURLConnection con = (HttpURLConnection) new URL(WEB + "?t=" + System.currentTimeMillis()).openConnection();
        con.setConnectTimeout(10000);
        con.setReadTimeout(10000);
        con.setUseCaches(false);
        con.setRequestProperty("User-Agent", "DiarioIAEducativa-Android");
        try {
            if (con.getResponseCode() != 200) throw new Exception("HTTP " + con.getResponseCode());
            InputStream in = con.getInputStream();
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] b = new byte[8192];
            for (int n; (n = in.read(b)) > 0; ) out.write(b, 0, n);
            return new JSONObject(new String(out.toByteArray(), StandardCharsets.UTF_8));
        } finally {
            con.disconnect();
        }
    }

    static void notificar(Context c, JSONObject u) throws Exception {
        if (!permitidas(c)) return;
        Context l = localizado(c);
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel canal = new NotificationChannel(CANAL, l.getString(R.string.avisos_canal),
                    NotificationManager.IMPORTANCE_DEFAULT);
            canal.setDescription(l.getString(R.string.avisos_canal_desc));
            nm.createNotificationChannel(canal);
        }
        JSONObject idiomas = u.getJSONObject("idiomas");
        JSONObject d = idiomas.optJSONObject(idioma(c));
        if (d == null) d = idiomas.getJSONObject("es");
        String titular = d.optString("titular", "");
        // Al tocarla se abre la portada de su idioma dentro de la app
        Intent abrir = new Intent(Intent.ACTION_VIEW, Uri.parse(d.getString("url")), c, LauncherActivity.class)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pi = PendingIntent.getActivity(c, 1, abrir,
                PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(c, CANAL) : new Notification.Builder(c);
        b.setSmallIcon(R.drawable.ic_aviso)
                .setColor(0xFF16181D)
                .setContentTitle(l.getString(R.string.avisos_titulo, u.getInt("numero")))
                .setContentText(titular)
                .setStyle(new Notification.BigTextStyle().bigText(titular))
                .setContentIntent(pi)
                .setAutoCancel(true);
        nm.notify(1, b.build());
    }
}
