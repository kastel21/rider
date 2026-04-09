package com.operations.rider

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

/**
 * Main WebView shell after local session login. Loads app root; Django redirects by role.
 */
class MainActivity : AppCompatActivity() {

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val prefs = getSharedPreferences(OpsPrefs.NAME, MODE_PRIVATE)
        if (!prefs.getBoolean(OpsPrefs.KEY_LAST_SYNC_OK, false)) {
            startActivity(
                Intent(this, LandingActivity::class.java).apply {
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                },
            )
            finish()
            return
        }

        OpsEmbeddedServer.ensureStarted(applicationContext)

        val wv = WebView(this)
        wv.settings.javaScriptEnabled = true
        wv.settings.domStorageEnabled = true
        wv.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                val uri = request.url
                val host = uri.host
                if (host != "127.0.0.1" && host != "localhost") {
                    return false
                }
                val path = uri.path ?: "/"
                if (path.startsWith("/static/") || path.startsWith("/media/")) {
                    return false
                }
                if (path == "/login" || path == "/login/" || path.startsWith("/login?")) {
                    startActivity(
                        Intent(this@MainActivity, LoginActivity::class.java).apply {
                            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                        },
                    )
                    finish()
                    return true
                }
                return false
            }
        }
        setContentView(wv)
        wv.loadUrl("http://127.0.0.1:${OpsEmbeddedServer.PORT}/")
    }
}
