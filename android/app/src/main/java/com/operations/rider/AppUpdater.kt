package com.operations.rider

import android.content.Context
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.content.pm.Signature
import android.os.Build
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.security.MessageDigest
import java.util.concurrent.TimeUnit

fun Request.Builder.withAppIdentity(): Request.Builder = apply {
    header("X-App-Version-Code", BuildConfig.VERSION_CODE.toString())
    header("X-App-Id", BuildConfig.APPLICATION_ID)
}

/**
 * Asks the cloud whether this APK is still allowed, and downloads the replacement file.
 */
object AppUpdater {
    data class Status(
        val updateRequired: Boolean,
        val updateAvailable: Boolean,
        val latestAppVersion: String,
        val downloadPath: String,
    )

    enum class ApkCheck {
        OK,
        DIFFERENT_KEY,
        DIFFERENT_APP,
        NOT_NEWER,
        UNREADABLE,
    }

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.MINUTES)
        .callTimeout(15, TimeUnit.MINUTES)
        .build()

    fun check(apiBase: String): Status? {
        val base = apiBase.trim().trimEnd('/')
        if (base.isEmpty()) return null
        val url = "$base/api/rider/app-update/" +
            "?version_code=${BuildConfig.VERSION_CODE}" +
            "&application_id=${BuildConfig.APPLICATION_ID}"
        val request = Request.Builder().url(url).get().withAppIdentity().build()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) return null
            val obj = JSONObject(response.body?.string().orEmpty())
            val downloadPath = obj.optString("download_path")
            return Status(
                updateRequired = obj.optBoolean("update_required", false),
                updateAvailable = obj.optBoolean("update_available", downloadPath.isNotBlank()),
                latestAppVersion = obj.optString("latest_app_version"),
                downloadPath = downloadPath,
            )
        }
    }

    fun resolveDownloadUrl(apiBase: String, downloadPath: String): String {
        val path = downloadPath.trim()
        if (path.startsWith("https://") || path.startsWith("http://")) return path
        val suffix = if (path.startsWith("/")) path else "/$path"
        return apiBase.trim().trimEnd('/') + suffix
    }

    fun download(url: String, dest: File, onProgress: (percent: Int) -> Unit) {
        val parent = dest.parentFile ?: throw IOException("no download folder")
        parent.mkdirs()
        val partial = File(parent, dest.name + ".part")
        val ready = File(parent, dest.name + ".ready")
        partial.delete()
        ready.delete()
        try {
            val request = Request.Builder().url(url).get().withAppIdentity().build()
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    throw IOException("download failed (${response.code})")
                }
                val body = response.body ?: throw IOException("empty download")
                val total = body.contentLength()
                body.byteStream().use { input ->
                    partial.outputStream().use { output ->
                        val buffer = ByteArray(64 * 1024)
                        var readTotal = 0L
                        var lastPercent = -1
                        while (true) {
                            val count = input.read(buffer)
                            if (count < 0) break
                            output.write(buffer, 0, count)
                            readTotal += count
                            if (total > 0L) {
                                val percent = ((100 * readTotal) / total).toInt().coerceIn(0, 99)
                                if (percent != lastPercent) {
                                    lastPercent = percent
                                    onProgress(percent)
                                }
                            }
                        }
                        output.flush()
                        if (total >= 0L && readTotal != total) {
                            throw IOException("download ended early")
                        }
                    }
                }
            }
            if (!isIntactApk(partial)) {
                throw IOException("download is not a complete apk")
            }
            if (!partial.renameTo(ready) && !copyFile(partial, ready)) {
                throw IOException("could not finish download")
            }
            partial.delete()
            if (!isIntactApk(ready)) {
                throw IOException("download is not a complete apk")
            }
            if (dest.exists() && !dest.delete()) {
                throw IOException("could not replace previous download")
            }
            if (!ready.renameTo(dest) && !copyFile(ready, dest)) {
                throw IOException("could not finish download")
            }
            ready.delete()
            if (!isIntactApk(dest)) {
                dest.delete()
                throw IOException("download is not a complete apk")
            }
        } catch (error: Exception) {
            partial.delete()
            ready.delete()
            throw error
        }
    }

    fun discardDownload(file: File) {
        file.delete()
        File(file.parentFile, file.name + ".part").delete()
        File(file.parentFile, file.name + ".ready").delete()
    }

    /** A complete ZIP/APK starts with a local header and ends with the central-directory marker. */
    fun isIntactApk(file: File): Boolean {
        if (!file.isFile || file.length() < 22L) return false
        file.inputStream().use { input ->
            val magic = ByteArray(4)
            if (input.read(magic) != 4) return false
            if (magic[0] != 0x50.toByte() || magic[1] != 0x4B.toByte() ||
                magic[2] != 0x03.toByte() || magic[3] != 0x04.toByte()
            ) {
                return false
            }
        }
        val window = minOf(file.length(), 22L + 65535L).toInt()
        val tail = ByteArray(window)
        file.inputStream().use { input ->
            val skip = file.length() - window
            var left = skip
            while (left > 0L) {
                val skipped = input.skip(left)
                if (skipped <= 0L) return false
                left -= skipped
            }
            var filled = 0
            while (filled < window) {
                val count = input.read(tail, filled, window - filled)
                if (count < 0) return false
                filled += count
            }
        }
        for (index in tail.size - 22 downTo 0) {
            if (tail[index] == 0x50.toByte() &&
                tail[index + 1] == 0x4B.toByte() &&
                tail[index + 2] == 0x05.toByte() &&
                tail[index + 3] == 0x06.toByte()
            ) {
                return true
            }
        }
        return false
    }

    private fun copyFile(from: File, to: File): Boolean {
        return try {
            from.copyTo(to, overwrite = true)
            true
        } catch (_: Exception) {
            to.delete()
            false
        }
    }

    /**
     * An update can replace this install only when it is the same app, signed with the
     * same certificate, and not an older versionCode.
     */
    fun checkApk(context: Context, apk: File): ApkCheck {
        val pm = context.packageManager
        val installed = packageInfo(pm, context.packageName, apkPath = null) ?: return ApkCheck.UNREADABLE
        val incoming = packageInfo(pm, context.packageName, apkPath = apk.absolutePath) ?: return ApkCheck.UNREADABLE
        if (incoming.packageName != context.packageName) return ApkCheck.DIFFERENT_APP
        val installedCerts = certSha256(installed)
        val incomingCerts = certSha256(incoming)
        if (installedCerts.isEmpty() || incomingCerts.isEmpty()) return ApkCheck.UNREADABLE
        if (installedCerts != incomingCerts) return ApkCheck.DIFFERENT_KEY
        if (versionCodeOf(incoming) < versionCodeOf(installed)) return ApkCheck.NOT_NEWER
        return ApkCheck.OK
    }

    private fun packageInfo(pm: PackageManager, packageName: String, apkPath: String?): PackageInfo? {
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            PackageManager.GET_SIGNING_CERTIFICATES
        } else {
            @Suppress("DEPRECATION")
            PackageManager.GET_SIGNATURES
        }
        return try {
            val info = if (apkPath == null) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    pm.getPackageInfo(packageName, PackageManager.PackageInfoFlags.of(flags.toLong()))
                } else {
                    @Suppress("DEPRECATION")
                    pm.getPackageInfo(packageName, flags)
                }
            } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                pm.getPackageArchiveInfo(apkPath, PackageManager.PackageInfoFlags.of(flags.toLong()))
            } else {
                @Suppress("DEPRECATION")
                pm.getPackageArchiveInfo(apkPath, flags)
            }
            if (info != null && apkPath != null) {
                info.applicationInfo?.sourceDir = apkPath
                info.applicationInfo?.publicSourceDir = apkPath
            }
            info
        } catch (_: Exception) {
            null
        }
    }

    @Suppress("DEPRECATION")
    private fun certSha256(info: PackageInfo): Set<String> {
        val signatures: Array<out Signature>? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val signing = info.signingInfo ?: return emptySet()
            if (signing.hasMultipleSigners()) {
                signing.apkContentsSigners
            } else {
                signing.signingCertificateHistory
            }
        } else {
            info.signatures
        }
        if (signatures.isNullOrEmpty()) return emptySet()
        return signatures.map { signature ->
            MessageDigest.getInstance("SHA-256")
                .digest(signature.toByteArray())
                .joinToString("") { "%02x".format(it) }
        }.toSet()
    }

    private fun versionCodeOf(info: PackageInfo): Long {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            info.longVersionCode
        } else {
            @Suppress("DEPRECATION")
            info.versionCode.toLong()
        }
    }
}
