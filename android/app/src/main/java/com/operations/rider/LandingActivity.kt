package com.operations.rider

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/**
 * Landing: online sync (service account) into local SQLite via POST /api/embedded/import-bootstrap/,
 * then user may continue to local WebView login. Service account bootstrap is scoped to that rider's
 * district; see `operations.services.embedded_bootstrap_import` module docstring.
 */
class LandingActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_landing)

        val status = findViewById<TextView>(R.id.landing_status)
        val syncBtn = findViewById<Button>(R.id.sync_button)
        val continueBtn = findViewById<Button>(R.id.continue_button)
        val err = findViewById<TextView>(R.id.sync_error)

        val prefs = getSharedPreferences(OpsPrefs.NAME, MODE_PRIVATE)
        refreshContinueState(continueBtn, prefs)

        Thread {
            try {
                OpsEmbeddedServer.ensureStarted(applicationContext)
                runOnUiThread {
                    status.setText(R.string.landing_status_ready)
                    syncBtn.isEnabled = true
                }
            } catch (e: Exception) {
                runOnUiThread {
                    status.text = getString(R.string.landing_server_failed, e.message ?: "")
                    Toast.makeText(this, R.string.landing_server_failed_toast, Toast.LENGTH_LONG).show()
                }
            }
        }.start()

        syncBtn.setOnClickListener {
            err.visibility = View.GONE
            val base = BuildConfig.OPS_REMOTE_API_BASE.trim().trimEnd('/')
            val user = BuildConfig.OPS_SYNC_USERNAME.trim()
            val pass = BuildConfig.OPS_SYNC_PASSWORD
            val emb = BuildConfig.OPS_EMBEDDED_IMPORT_SECRET.trim()
            if (base.isEmpty() || user.isEmpty() || pass.isEmpty() || emb.isEmpty()) {
                err.text = getString(R.string.landing_config_error)
                err.visibility = View.VISIBLE
                return@setOnClickListener
            }
            syncBtn.isEnabled = false
            status.setText(R.string.landing_status_syncing)
            Thread {
                try {
                    val loginUrl = "$base/api/rider/login/"
                    val loginJson = JSONObject().apply {
                        put("username", user)
                        put("password", pass)
                    }
                    val loginReq = Request.Builder()
                        .url(loginUrl)
                        .post(loginJson.toString().toRequestBody(JSON))
                        .build()
                    val loginResp = client.newCall(loginReq).execute()
                    loginResp.use { lr ->
                        val body = lr.body?.string().orEmpty()
                        if (!lr.isSuccessful) {
                            val msg = parseError(body, lr.message)
                            runOnUiThread {
                                syncBtn.isEnabled = true
                                status.setText(R.string.landing_status_ready)
                                err.text = msg
                                err.visibility = View.VISIBLE
                            }
                            return@Thread
                        }
                        val access = JSONObject(body).getString("access")

                        val bootReq = Request.Builder()
                            .url("$base/api/rider/bootstrap/")
                            .header("Authorization", "Bearer $access")
                            .get()
                            .build()
                        val profReq = Request.Builder()
                            .url("$base/api/rider/profile/")
                            .header("Authorization", "Bearer $access")
                            .get()
                            .build()

                        client.newCall(bootReq).execute().use { br ->
                            val bootBody = br.body?.string().orEmpty()
                            if (!br.isSuccessful) {
                                runOnUiThread {
                                    syncBtn.isEnabled = true
                                    status.setText(R.string.landing_status_ready)
                                    err.text = parseError(bootBody, br.message)
                                    err.visibility = View.VISIBLE
                                }
                                return@Thread
                            }
                            val bootObj = JSONObject(bootBody)

                            client.newCall(profReq).execute().use { pr ->
                                val profBody = pr.body?.string().orEmpty()
                                if (!pr.isSuccessful) {
                                    runOnUiThread {
                                        syncBtn.isEnabled = true
                                        status.setText(R.string.landing_status_ready)
                                        err.text = parseError(profBody, pr.message)
                                        err.visibility = View.VISIBLE
                                    }
                                    return@Thread
                                }
                                val profObj = JSONObject(profBody)

                                val combined = JSONObject().apply {
                                    put("bootstrap", bootObj)
                                    put("profile", profObj)
                                }
                                val importReq = Request.Builder()
                                    .url("http://127.0.0.1:${OpsEmbeddedServer.PORT}/api/embedded/import-bootstrap/")
                                    .header("X-Ops-Embedded-Secret", emb)
                                    .post(combined.toString().toRequestBody(JSON))
                                    .build()
                                client.newCall(importReq).execute().use { ir ->
                                    val ib = ir.body?.string().orEmpty()
                                    if (!ir.isSuccessful) {
                                        runOnUiThread {
                                            syncBtn.isEnabled = true
                                            status.setText(R.string.landing_status_ready)
                                            err.text = parseError(ib, ir.message)
                                            err.visibility = View.VISIBLE
                                        }
                                        return@Thread
                                    }
                                    val bootstrapOk = try {
                                        JSONObject(ib).optBoolean("ok", false)
                                    } catch (_: Exception) {
                                        false
                                    }
                                    if (!bootstrapOk) {
                                        runOnUiThread {
                                            syncBtn.isEnabled = true
                                            status.setText(R.string.landing_status_ready)
                                            err.text = ib.ifEmpty { getString(R.string.landing_import_failed) }
                                            err.visibility = View.VISIBLE
                                        }
                                        return@Thread
                                    }

                                    val districtId = resolveDistrictId(bootObj, profObj)
                                    if (districtId == null) {
                                        runOnUiThread {
                                            finishSyncSuccess(prefs, continueBtn, status, syncBtn)
                                        }
                                        return@Thread
                                    }

                                    val userExportUrl =
                                        "$base/api/rider/mobile-user-export/?district_id=$districtId"
                                    val userExportReq = Request.Builder()
                                        .url(userExportUrl)
                                        .header("Authorization", "Bearer $access")
                                        .get()
                                        .build()
                                    client.newCall(userExportReq).execute().use { ur ->
                                        val ub = ur.body?.string().orEmpty()
                                        if (!ur.isSuccessful) {
                                            runOnUiThread {
                                                syncBtn.isEnabled = true
                                                status.setText(R.string.landing_status_ready)
                                                err.text = parseError(ub, ur.message)
                                                    .ifEmpty { getString(R.string.landing_user_import_failed) }
                                                err.visibility = View.VISIBLE
                                            }
                                            return@Thread
                                        }
                                        val userImportReq = Request.Builder()
                                            .url("http://127.0.0.1:${OpsEmbeddedServer.PORT}/api/embedded/import-users/")
                                            .header("X-Ops-Embedded-Secret", emb)
                                            .post(ub.toRequestBody(JSON))
                                            .build()
                                        client.newCall(userImportReq).execute().use { uir ->
                                            val uib = uir.body?.string().orEmpty()
                                            runOnUiThread {
                                                syncBtn.isEnabled = true
                                                if (!uir.isSuccessful) {
                                                    status.setText(R.string.landing_status_ready)
                                                    err.text = parseError(uib, uir.message)
                                                        .ifEmpty { getString(R.string.landing_user_import_failed) }
                                                    err.visibility = View.VISIBLE
                                                    return@runOnUiThread
                                                }
                                                val uOk = try {
                                                    JSONObject(uib).optBoolean("ok", false)
                                                } catch (_: Exception) {
                                                    false
                                                }
                                                if (!uOk) {
                                                    status.setText(R.string.landing_status_ready)
                                                    err.text = uib.ifEmpty { getString(R.string.landing_user_import_failed) }
                                                    err.visibility = View.VISIBLE
                                                    return@runOnUiThread
                                                }
                                                finishSyncSuccess(prefs, continueBtn, status, syncBtn)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        syncBtn.isEnabled = true
                        status.setText(R.string.landing_status_ready)
                        err.text = e.message ?: getString(R.string.login_error_network)
                        err.visibility = View.VISIBLE
                    }
                }
            }.start()
        }

        continueBtn.setOnClickListener {
            startActivity(
                Intent(this, LoginActivity::class.java).apply {
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                },
            )
        }
    }

    private fun finishSyncSuccess(
        prefs: android.content.SharedPreferences,
        continueBtn: Button,
        status: TextView,
        syncBtn: Button,
    ) {
        prefs.edit()
            .putBoolean(OpsPrefs.KEY_LAST_SYNC_OK, true)
            .putLong(OpsPrefs.KEY_LAST_SYNC_AT, System.currentTimeMillis())
            .apply()
        status.setText(R.string.landing_status_synced)
        refreshContinueState(continueBtn, prefs)
        syncBtn.isEnabled = true
    }

    private fun refreshContinueState(continueBtn: Button, prefs: android.content.SharedPreferences) {
        continueBtn.isEnabled = prefs.getBoolean(OpsPrefs.KEY_LAST_SYNC_OK, false)
    }

    private fun parseError(body: String, fallback: String): String {
        return try {
            JSONObject(body).optString("error", body.ifEmpty { fallback })
        } catch (_: Exception) {
            body.ifEmpty { fallback }
        }
    }

    companion object {
        /** Match [RiderBootstrapView] root and profile district id for mobile-user-export. */
        private fun resolveDistrictId(bootstrap: JSONObject, profile: JSONObject): Int? {
            if (bootstrap.has("district_id") && !bootstrap.isNull("district_id")) {
                try {
                    return bootstrap.getInt("district_id")
                } catch (_: Exception) {
                }
            }
            if (profile.has("district")) {
                try {
                    val d = profile.getJSONObject("district")
                    if (d.has("id")) {
                        return d.getInt("id")
                    }
                } catch (_: Exception) {
                }
            }
            return null
        }

        private val JSON = "application/json; charset=utf-8".toMediaType()
        private val client = OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .build()
    }
}
