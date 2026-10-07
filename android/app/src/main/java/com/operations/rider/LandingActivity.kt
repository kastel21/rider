package com.operations.rider

import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.SharedPreferences
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.StringRes
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import java.io.File
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/**
 * Landing: online sync (service account) into local SQLite via POST /api/embedded/import-bootstrap/,
 * then user may continue to local WebView login. Cloud bootstrap for OPS_SYNC_USERNAME includes
 * all facilities when that username is in OPS_MOBILE_SYNC_USERNAMES.
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
    private lateinit var updateBtn: Button
    private lateinit var continueBtn: Button
    private lateinit var progress: ProgressBar
    private lateinit var err: TextView
    private lateinit var errScroll: ScrollView
    private lateinit var prefs: SharedPreferences

    private var syncInProgress = false
    private var updateDownloadPath: String = ""
    private var pendingInstall: File? = null
    private var updateDialog: AlertDialog? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_landing)

        status = findViewById(R.id.landing_status)
        syncBtn = findViewById(R.id.sync_button)
        updateBtn = findViewById(R.id.update_button)
        continueBtn = findViewById(R.id.continue_button)
        progress = findViewById(R.id.landing_progress)
        err = findViewById(R.id.sync_error)
        errScroll = findViewById(R.id.sync_error_scroll)
        prefs = getSharedPreferences(OpsPrefs.NAME, MODE_PRIVATE)

        refreshContinueState()
        beginStartup()
        checkForRequiredUpdate()

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

        updateBtn.setOnClickListener {
            if (updateDownloadPath.isBlank()) return@setOnClickListener
            downloadAndInstallUpdate()
        }

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
                        .withAppIdentity()
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
                            .withAppIdentity()
                            .build()
                        val profReq = Request.Builder()
                            .url("$base/api/rider/profile/")
                            .header("Authorization", "Bearer $access")
                            .get()
                            .withAppIdentity()
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
                                        .withAppIdentity()
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

    override fun onResume() {
        super.onResume()
        val file = pendingInstall ?: return
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !packageManager.canRequestPackageInstalls()) {
            return
        }
        pendingInstall = null
        if (!file.isFile || !AppUpdater.isIntactApk(file) || AppUpdater.checkApk(this, file) != AppUpdater.ApkCheck.OK) {
            AppUpdater.discardDownload(file)
            showUpdateProblem(R.string.landing_update_discarded)
            return
        }
        installDownloadedApk(file)
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
        if (httpCode == 426 || updateRequiredCode(body)) {
            val path = try {
                JSONObject(body).optString("download_path")
            } catch (_: Exception) {
                ""
            }
            val name = try {
                JSONObject(body).optString("latest_app_version")
            } catch (_: Exception) {
                ""
            }
            endSync()
            status.setText(R.string.landing_status_ready)
            showUpdateOffer(name, path)
            return
        }
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

    private fun updateRequiredCode(body: String): Boolean {
        return try {
            JSONObject(body).optString("code") == "update_required"
        } catch (_: Exception) {
            false
        }
    }

    private fun checkForRequiredUpdate() {
        val base = BuildConfig.OPS_REMOTE_API_BASE.trim()
        if (base.isEmpty()) return
        Thread {
            val statusInfo = try {
                AppUpdater.check(base)
            } catch (_: Exception) {
                null
            } ?: return@Thread
            if (statusInfo.downloadPath.isBlank()) return@Thread
            if (!statusInfo.updateRequired && !statusInfo.updateAvailable) return@Thread
            runOnUiThread {
                showUpdateOffer(statusInfo.latestAppVersion, statusInfo.downloadPath)
            }
        }.start()
    }

    private fun showUpdateOffer(versionName: String, downloadPath: String) {
        val path = downloadPath.trim()
        if (path.isBlank() || isFinishing) return
        updateDownloadPath = path
        if (updateDialog?.isShowing == true) return
        val label = versionName.trim().ifEmpty { getString(R.string.landing_update_version_fallback) }
        updateDialog = AlertDialog.Builder(this)
            .setTitle(R.string.landing_update_title)
            .setMessage(getString(R.string.landing_update_message, label))
            .setPositiveButton(R.string.landing_update_accept) { _, _ ->
                downloadAndInstallUpdate()
            }
            .setNegativeButton(R.string.landing_update_reject) { _, _ ->
                updateBtn.visibility = View.VISIBLE
                updateBtn.isEnabled = true
            }
            .setCancelable(true)
            .create()
        updateDialog?.show()
    }

    private fun downloadAndInstallUpdate() {
        val base = BuildConfig.OPS_REMOTE_API_BASE.trim()
        val path = updateDownloadPath
        if (base.isEmpty() || path.isBlank()) return
        updateBtn.isEnabled = false
        progress.visibility = View.VISIBLE
        status.text = getString(R.string.landing_update_downloading, 0)
        val dest = File(cacheDir, "updates/rider-update.apk")
        Thread {
            try {
                AppUpdater.download(AppUpdater.resolveDownloadUrl(base, path), dest) { percent ->
                    runOnUiThread {
                        status.text = getString(R.string.landing_update_downloading, percent)
                    }
                }
                val intact = AppUpdater.isIntactApk(dest)
                val verdict = if (intact) AppUpdater.checkApk(this, dest) else AppUpdater.ApkCheck.UNREADABLE
                if (verdict != AppUpdater.ApkCheck.OK) {
                    AppUpdater.discardDownload(dest)
                }
                runOnUiThread {
                    progress.visibility = View.GONE
                    updateBtn.isEnabled = true
                    when (verdict) {
                        AppUpdater.ApkCheck.OK -> installDownloadedApk(dest)
                        AppUpdater.ApkCheck.DIFFERENT_KEY ->
                            showUpdateProblem(R.string.landing_update_key_mismatch)
                        AppUpdater.ApkCheck.DIFFERENT_APP ->
                            showUpdateProblem(R.string.landing_update_wrong_app)
                        AppUpdater.ApkCheck.NOT_NEWER ->
                            showUpdateProblem(R.string.landing_update_not_newer)
                        AppUpdater.ApkCheck.UNREADABLE ->
                            showUpdateProblem(R.string.landing_update_discarded)
                    }
                }
            } catch (_: Exception) {
                AppUpdater.discardDownload(dest)
                runOnUiThread {
                    progress.visibility = View.GONE
                    updateBtn.isEnabled = true
                    showUpdateProblem(R.string.landing_update_discarded)
                }
            }
        }.start()
    }

    private fun showUpdateProblem(@StringRes messageRes: Int) {
        if (isFinishing) return
        AlertDialog.Builder(this)
            .setTitle(R.string.landing_update_title)
            .setMessage(messageRes)
            .setPositiveButton(android.R.string.ok, null)
            .show()
    }

    private fun installDownloadedApk(file: File) {
        if (!file.isFile || !AppUpdater.isIntactApk(file) || AppUpdater.checkApk(this, file) != AppUpdater.ApkCheck.OK) {
            pendingInstall = null
            AppUpdater.discardDownload(file)
            showUpdateProblem(R.string.landing_update_discarded)
            return
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !packageManager.canRequestPackageInstalls()) {
            pendingInstall = file
            status.setText(R.string.landing_update_permission)
            startActivity(
                Intent(
                    Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                    Uri.parse("package:$packageName"),
                ),
            )
            return
        }
        val uri = FileProvider.getUriForFile(this, "$packageName.fileprovider", file)
        val intent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, "application/vnd.android.package-archive")
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        try {
            startActivity(intent)
            status.setText(R.string.landing_update_install)
        } catch (_: ActivityNotFoundException) {
            AppUpdater.discardDownload(file)
            showUpdateProblem(R.string.landing_update_discarded)
        }
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
