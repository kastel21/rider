package com.operations.rider

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.webkit.CookieManager
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity

/**
 * Local Django session login ([LoginView]) in WebView. Requires a successful landing sync first.
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var progress: ProgressBar
    private lateinit var status: TextView
    private lateinit var touchBlocker: View

    private var loginFormReady = false
    private var pageLoadProgress = 0
    private var loadingActive = false
    private var activeMessageRes = R.string.login_status_starting

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

        setContentView(R.layout.activity_login)
        webView = findViewById(R.id.login_webview)
        progress = findViewById(R.id.login_progress)
        status = findViewById(R.id.login_status)
        touchBlocker = findViewById(R.id.login_touch_blocker)

        showLoading(R.string.login_status_starting)

        Thread {
            try {
                OpsEmbeddedServer.ensureStarted(applicationContext)
                runOnUiThread {
                    setupWebView()
                    showLoading(R.string.login_status_loading_page)
                    webView.loadUrl("http://127.0.0.1:${OpsEmbeddedServer.PORT}/login/")
                }
            } catch (_: Exception) {
                runOnUiThread {
                    status.setText(R.string.login_server_failed)
                    progress.visibility = View.GONE
                    touchBlocker.visibility = View.GONE
                    webView.visibility = View.VISIBLE
                    Toast.makeText(this, R.string.landing_server_failed_toast, Toast.LENGTH_LONG).show()
                }
            }
        }.start()
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        CookieManager.getInstance().setAcceptCookie(true)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                pageLoadProgress = newProgress
                if (newProgress in 1..99) {
                    showLoading(activeMessageRes)
                } else if (newProgress >= 100 && loadingActive) {
                    maybeFinishLoading(pathFromUrl(view?.url))
                }
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                pageLoadProgress = 0
                webView.visibility = View.INVISIBLE
                val path = pathFromUrl(url)
                when {
                    path.contains("login") && loginFormReady ->
                        showLoading(R.string.login_status_signing_in)
                    path.contains("login") ->
                        showLoading(R.string.login_status_loading_page)
                    else ->
                        showLoading(R.string.login_status_signing_in)
                }
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                pageLoadProgress = 100
                maybeFinishLoading(pathFromUrl(url))
            }

            override fun onPageCommitVisible(view: WebView?, url: String?) {
                maybeFinishLoading(pathFromUrl(url))
            }

            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                val uri = request.url
                if (uri.host != "127.0.0.1" && uri.host != "localhost") {
                    return false
                }
                val path = uri.path ?: "/"
                if (path.startsWith("/static/") || path.startsWith("/media/")) {
                    return false
                }
                if (path == "/login" || path == "/login/" || path.startsWith("/login?")) {
                    return false
                }
                if (path == "/" || path.startsWith("/reports") || path.startsWith("/pc/") || path.startsWith("/me/")) {
                    showLoading(R.string.login_status_opening_app)
                    startActivity(
                        Intent(this@LoginActivity, MainActivity::class.java).apply {
                            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                        },
                    )
                    finish()
                    return true
                }
                return false
            }
        }
    }

    private fun maybeFinishLoading(path: String) {
        if (pageLoadProgress in 0..99) return
        if (path.contains("login")) {
            loginFormReady = true
            hideLoading()
        } else {
            showLoading(R.string.login_status_opening_app)
        }
    }

    private fun pathFromUrl(url: String?): String {
        if (url.isNullOrBlank()) return ""
        return try {
            android.net.Uri.parse(url).path ?: ""
        } catch (_: Exception) {
            ""
        }
    }

    private fun showLoading(@StringRes messageRes: Int) {
        loadingActive = true
        activeMessageRes = messageRes
        status.setText(messageRes)
        progress.visibility = View.VISIBLE
        touchBlocker.visibility = View.VISIBLE
    }

    private fun hideLoading() {
        loadingActive = false
        progress.visibility = View.GONE
        touchBlocker.visibility = View.GONE
        webView.visibility = View.VISIBLE
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
