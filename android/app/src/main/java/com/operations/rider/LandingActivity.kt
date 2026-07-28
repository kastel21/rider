package com.operations.rider

import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.StringRes
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

    private enum class SyncStep {
        SIGN_IN,
        DOWNLOAD,
        SAVE_LOCAL,
        DOWNLOAD_USERS,
        SAVE_USERS,
    }

    private lateinit var status: TextView
    private lateinit var syncBtn: Button
    private lateinit var continueBtn: Button
    private lateinit var progress: ProgressBar
    private lateinit var err: TextView
    private lateinit var errScroll: ScrollView
    private lateinit var prefs: SharedPreferences

    private var syncInProgress = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_landing)

        status = findViewById(R.id.landing_status)
        syncBtn = findViewById(R.id.sync_button)
        continueBtn = findViewById(R.id.continue_button)
        progress = findViewById(R.id.landing_progress)
        err = findViewById(R.id.sync_error)
        errScroll = findViewById(R.id.sync_error_scroll)
        prefs = getSharedPreferences(OpsPrefs.NAME, MODE_PRIVATE)

        refreshContinueState()
        beginStartup()

        Thread {
            try {
                OpsEmbeddedServer.ensureStarted(applicationContext)
                runOnUiThread { endStartup(success = true) }
            } catch (_: Exception) {
                runOnUiThread {
                    endStartup(success = false)
                    status.setText(R.string.landing_server_failed)
                    Toast.makeText(this, R.string.landing_server_failed_toast, Toast.LENGTH_LONG).show()
                }
            }
        }.start()

        syncBtn.setOnClickListener {
            if (syncInProgress) return@setOnClickListener
            hideSyncError()
            val base = BuildConfig.OPS_REMOTE_API_BASE.trim().trimEnd('/')
            val user = BuildConfig.OPS_SYNC_USERNAME.trim()
            val pass = BuildConfig.OPS_SYNC_PASSWORD
            val emb = BuildConfig.OPS_EMBEDDED_IMPORT_SECRET.trim()
            if (base.isEmpty() || user.isEmpty() || pass.isEmpty() || emb.isEmpty()) {
                err.text = getString(R.string.landing_config_error)
                errScroll.visibility = View.VISIBLE
                return@setOnClickListener
            }
            beginSync()
            Thread {
                try {
                    postStepStatus(R.string.landing_status_sign_in)
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
                            runOnUiThread {
                                showSyncError(SyncStep.SIGN_IN, body, lr.code)
                            }
                            return@Thread
                        }
                        val access = try {
                            JSONObject(body).getString("access")
                        } catch (_: Exception) {
                            runOnUiThread {
                                showSyncError(SyncStep.SIGN_IN, body, lr.code)
                            }
                            return@Thread
                        }

                        postStepStatus(R.string.landing_status_download)
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
                                    showSyncError(SyncStep.DOWNLOAD, bootBody, br.code)
                                }
                                return@Thread
                            }
                            val bootObj = JSONObject(bootBody)

                            client.newCall(profReq).execute().use { pr ->
                                val profBody = pr.body?.string().orEmpty()
                                if (!pr.isSuccessful) {
                                    runOnUiThread {
                                        showSyncError(SyncStep.DOWNLOAD, profBody, pr.code)
                                    }
                                    return@Thread
                                }
                                val profObj = JSONObject(profBody)

                                postStepStatus(R.string.landing_status_save_local)
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
                                            showSyncError(SyncStep.SAVE_LOCAL, ib, ir.code)
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
                                            showSyncError(
                                                SyncStep.SAVE_LOCAL,
                                                ib,
                                                ir.code,
                                                fallbackRes = R.string.landing_import_failed,
                                            )
                                        }
                                        return@Thread
                                    }

                                    val districtId = resolveDistrictId(bootObj, profObj)
                                    if (districtId == null) {
                                        runOnUiThread { finishSyncSuccess() }
                                        reportUserAppsInBackground(base, access)
                                        return@Thread
                                    }

                                    postStepStatus(R.string.landing_status_download_users)
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
                                                showSyncError(
                                                    SyncStep.DOWNLOAD_USERS,
                                                    ub,
                                                    ur.code,
                                                    fallbackRes = R.string.landing_user_import_failed,
                                                )
                                            }
                                            return@Thread
                                        }
                                        postStepStatus(R.string.landing_status_save_users)
                                        val userImportReq = Request.Builder()
                                            .url("http://127.0.0.1:${OpsEmbeddedServer.PORT}/api/embedded/import-users/")
                                            .header("X-Ops-Embedded-Secret", emb)
                                            .post(ub.toRequestBody(JSON))
                                            .build()
                                        client.newCall(userImportReq).execute().use { uir ->
                                            val uib = uir.body?.string().orEmpty()
                                            runOnUiThread {
                                                if (!uir.isSuccessful) {
                                                    showSyncError(
                                                        SyncStep.SAVE_USERS,
                                                        uib,
                                                        uir.code,
                                                        fallbackRes = R.string.landing_user_import_failed,
                                                    )
                                                    return@runOnUiThread
                                                }
                                                val uOk = try {
                                                    JSONObject(uib).optBoolean("ok", false)
                                                } catch (_: Exception) {
                                                    false
                                                }
                                                if (!uOk) {
                                                    showSyncError(
                                                        SyncStep.SAVE_USERS,
                                                        uib,
                                                        uir.code,
                                                        fallbackRes = R.string.landing_user_import_failed,
                                                    )
                                                    return@runOnUiThread
                                                }
                                                finishSyncSuccess()
                                            }
                                        }
                                    }
                                    reportUserAppsInBackground(base, access)
                                }
                            }
                        }
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        showSyncError(SyncStep.DOWNLOAD, e.message.orEmpty(), 0)
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

    private fun beginStartup() {
        progress.visibility = View.VISIBLE
        syncBtn.isEnabled = false
        continueBtn.isEnabled = false
        status.setText(R.string.landing_status_starting)
    }

    private fun endStartup(success: Boolean) {
        progress.visibility = View.GONE
        if (success) {
            status.setText(R.string.landing_status_ready)
            syncBtn.isEnabled = true
            refreshContinueState()
        }
    }

    private fun beginSync() {
        syncInProgress = true
        progress.visibility = View.VISIBLE
        syncBtn.isEnabled = false
        syncBtn.text = getString(R.string.landing_sync_in_progress)
        continueBtn.isEnabled = false
        status.setText(R.string.landing_status_syncing)
    }

    private fun endSync() {
        syncInProgress = false
        progress.visibility = View.GONE
        syncBtn.isEnabled = true
        syncBtn.text = getString(R.string.landing_sync)
        refreshContinueState()
    }

    private fun postStepStatus(@StringRes messageRes: Int) {
        runOnUiThread { status.setText(messageRes) }
    }

    private fun hideSyncError() {
        err.text = ""
        errScroll.visibility = View.GONE
    }

    private fun showSyncError(
        step: SyncStep,
        body: String,
        httpCode: Int,
        withRetryHint: Boolean = true,
        fallbackRes: Int? = null,
    ) {
        endSync()
        status.setText(R.string.landing_status_ready)
        val detail = friendlyDetail(extractErrorMessage(body), httpCode, fallbackRes)
        val prefix = when (step) {
            SyncStep.SIGN_IN -> getString(R.string.landing_error_sign_in, detail)
            SyncStep.DOWNLOAD -> getString(R.string.landing_error_download, detail)
            SyncStep.SAVE_LOCAL -> getString(R.string.landing_error_save_local, detail)
            SyncStep.DOWNLOAD_USERS -> getString(R.string.landing_error_download_users, detail)
            SyncStep.SAVE_USERS -> getString(R.string.landing_error_save_users, detail)
        }
        err.text = if (withRetryHint) {
            "$prefix\n\n${getString(R.string.landing_error_retry_hint)}"
        } else {
            prefix
        }
        errScroll.visibility = View.VISIBLE
    }

    private fun extractErrorMessage(body: String): String {
        val trimmed = body.trim()
        if (trimmed.isEmpty()) return ""
        if (trimmed.startsWith("<") || trimmed.contains("<html", ignoreCase = true)) {
            return ""
        }
        return try {
            val obj = JSONObject(trimmed)
            obj.optString("error").trim()
                .ifEmpty { obj.optString("detail").trim() }
                .ifEmpty { obj.optString("message").trim() }
        } catch (_: Exception) {
            if (trimmed.startsWith("{")) "" else trimmed
        }
    }

    private fun friendlyDetail(raw: String, httpCode: Int, fallbackRes: Int?): String {
        val msg = raw.trim().lowercase()
        when {
            httpCode == 401 || msg.contains("invalid credentials") ->
                return getString(R.string.landing_err_invalid_credentials)
            msg.contains("not a rider") ->
                return getString(R.string.landing_err_not_rider)
            msg.contains("rider profile not found") ->
                return getString(R.string.landing_err_no_profile)
            httpCode == 403 || msg == "forbidden" || msg.contains("permission") ->
                return getString(R.string.landing_err_forbidden)
            httpCode == 404 || msg.contains("not found") ->
                return getString(R.string.landing_err_not_found)
            httpCode in 500..599 ->
                return getString(R.string.landing_err_server)
            msg.contains("unable to resolve host") ||
                msg.contains("failed to connect") ||
                msg.contains("connection refused") ||
                msg.contains("timeout") ||
                msg.contains("network") ->
                return getString(R.string.landing_err_network)
            fallbackRes != null ->
                return getString(fallbackRes)
            raw.isNotBlank() && raw.length <= 120 ->
                return raw.replaceFirstChar { if (it.isLowerCase()) it.titlecase() else it.toString() }
            else ->
                return getString(R.string.landing_err_generic)
        }
    }

    private fun finishSyncSuccess() {
        prefs.edit()
            .putBoolean(OpsPrefs.KEY_LAST_SYNC_OK, true)
            .putLong(OpsPrefs.KEY_LAST_SYNC_AT, System.currentTimeMillis())
            .apply()
        endSync()
        status.setText(R.string.landing_status_synced)
        refreshContinueState()
    }

    private fun refreshContinueState() {
        continueBtn.isEnabled = !syncInProgress && prefs.getBoolean(OpsPrefs.KEY_LAST_SYNC_OK, false)
    }

    private fun reportUserAppsInBackground(apiBase: String, accessToken: String) {
        Thread {
            UserAppsReporter.reportToRemote(applicationContext, apiBase, accessToken)
        }.start()
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
