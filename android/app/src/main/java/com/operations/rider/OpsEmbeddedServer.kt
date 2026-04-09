package com.operations.rider

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.util.UUID

/**
 * Starts the embedded Django WSGI server once (Chaquopy). Used from Landing, Login, and Main.
 */
object OpsEmbeddedServer {

    const val PORT = 8765
    private const val KEY_SECRET = "django_secret"

    @Synchronized
    fun ensureStarted(context: Context) {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        val prefs = context.applicationContext.getSharedPreferences(OpsPrefs.NAME, Context.MODE_PRIVATE)
        var secret = prefs.getString(KEY_SECRET, null)
        if (secret.isNullOrBlank()) {
            secret = UUID.randomUUID().toString()
            prefs.edit().putString(KEY_SECRET, secret).apply()
        }
        val py = Python.getInstance()
        val server = py.getModule("server")
        val out = server.callAttr(
            "start_server",
            PORT,
            secret,
            BuildConfig.OPS_REMOTE_API_BASE,
            if (BuildConfig.DEBUG) 1 else 0,
            BuildConfig.JWT_SIGNING_KEY,
            BuildConfig.OPS_EMBEDDED_IMPORT_SECRET,
        )
        if (out?.toString() != "1") {
            throw IllegalStateException("Local Django server did not start on port $PORT")
        }
    }
}
