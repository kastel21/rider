package com.operations.rider

import android.app.AppOpsManager
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.os.Build
import android.util.Log
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/**
 * Enumerates launcher-visible user apps (not system packages) and optionally
 * limits to packages with recent usage when Usage Access is granted.
 */
object UserAppsReporter {

    data class AppEntry(val packageName: String, val label: String)

    private const val TAG = "UserAppsReporter"
    private const val USAGE_LOOKBACK_DAYS = 90
    private val JSON = "application/json; charset=utf-8".toMediaType()
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    fun launcherUserApps(context: Context): List<AppEntry> {
        val pm = context.packageManager
        val launcherIntent = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            PackageManager.MATCH_ALL
        } else {
            @Suppress("DEPRECATION")
            PackageManager.GET_RESOLVED_FILTER
        }
        val activities = pm.queryIntentActivities(launcherIntent, flags)
        val seen = LinkedHashSet<String>()
        val result = mutableListOf<AppEntry>()
        for (resolveInfo in activities) {
            val pkg = resolveInfo.activityInfo?.packageName ?: continue
            if (!seen.add(pkg)) continue
            try {
                val appInfo = pm.getApplicationInfo(pkg, 0)
                if (isSystemPackage(appInfo)) continue
                val label = pm.getApplicationLabel(appInfo).toString().trim()
                if (label.isEmpty()) continue
                result.add(AppEntry(pkg, label))
            } catch (_: PackageManager.NameNotFoundException) {
            }
        }
        val recentlyUsed = recentlyUsedPackages(context)
        return if (recentlyUsed.isNullOrEmpty()) {
            result.sortedBy { it.label.lowercase() }
        } else {
            result.filter { it.packageName in recentlyUsed }
                .sortedBy { it.label.lowercase() }
        }
    }

    private fun isSystemPackage(appInfo: ApplicationInfo): Boolean {
        val flags = appInfo.flags
        val isSystem = (flags and ApplicationInfo.FLAG_SYSTEM) != 0
        val isUpdatedSystem = (flags and ApplicationInfo.FLAG_UPDATED_SYSTEM_APP) != 0
        return isSystem && !isUpdatedSystem
    }

    private fun recentlyUsedPackages(context: Context): Set<String>? {
        if (!hasUsageAccess(context)) return null
        val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
            ?: return null
        val end = System.currentTimeMillis()
        val start = end - USAGE_LOOKBACK_DAYS * 24L * 60L * 60L * 1000L
        val stats = usm.queryUsageStats(UsageStatsManager.INTERVAL_DAILY, start, end) ?: return null
        val used = stats
            .filter { it.totalTimeInForeground > 0 }
            .map { it.packageName }
            .toSet()
        return used.ifEmpty { null }
    }

    private fun hasUsageAccess(context: Context): Boolean {
        val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as? AppOpsManager ?: return false
        val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            appOps.unsafeCheckOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                android.os.Process.myUid(),
                context.packageName,
            )
        } else {
            @Suppress("DEPRECATION")
            appOps.checkOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                android.os.Process.myUid(),
                context.packageName,
            )
        }
        return mode == AppOpsManager.MODE_ALLOWED
    }

    fun reportToRemote(context: Context, apiBase: String, accessToken: String) {
        val base = apiBase.trim().trimEnd('/')
        if (base.isEmpty() || accessToken.isBlank()) return
        val apps = launcherUserApps(context)
        if (apps.isEmpty()) return
        val arr = JSONArray()
        for (app in apps) {
            arr.put(
                JSONObject().apply {
                    put("package", app.packageName)
                    put("label", app.label)
                    put("is_system", false)
                },
            )
        }
        val body = JSONObject().apply { put("apps", arr) }.toString()
        val req = Request.Builder()
            .url("$base/api/rider/report-user-apps/")
            .header("Authorization", "Bearer $accessToken")
            .post(body.toRequestBody(JSON))
            .build()
        try {
            client.newCall(req).execute().use { resp ->
                if (!resp.isSuccessful) {
                    Log.w(TAG, "report-user-apps failed: ${resp.code}")
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "report-user-apps error: ${e.message}")
        }
    }
}
