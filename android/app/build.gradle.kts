import java.io.File
import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python")
}

fun escapeForBuildConfigString(value: String): String =
    value.replace("\\", "\\\\").replace("\"", "\\\"")

val localProperties = Properties().apply {
    rootProject.file("local.properties").takeIf { it.exists() }?.inputStream()?.use { load(it) }
}

/** Repo-root .env fallback (same keys as android/local.properties). */
val rootEnvProperties = Properties().apply {
    val envFile = rootProject.file("../.env")
    if (!envFile.isFile) return@apply
    envFile.readLines().forEach { line ->
        val trimmed = line.trim()
        if (trimmed.isEmpty() || trimmed.startsWith("#")) return@forEach
        val eq = trimmed.indexOf('=')
        if (eq > 0) {
            setProperty(trimmed.substring(0, eq).trim(), trimmed.substring(eq + 1).trim())
        }
    }
}

fun buildConfigProp(key: String): String {
    val fromLocal = localProperties.getProperty(key)?.trim().orEmpty()
    if (fromLocal.isNotEmpty()) return fromLocal
    return rootEnvProperties.getProperty(key)?.trim().orEmpty()
}

/** Host Python for Chaquopy. 32-bit APK needs 3.11; 64-bit APK needs 3.13. */
fun chaquopyBuildPythonArgs(bit: String): Array<String> {
    val envName = if (bit == "32") "CHAQUOPY_BUILD_PYTHON_32" else "CHAQUOPY_BUILD_PYTHON_64"
    var fromEnv = System.getenv(envName)?.trim().orEmpty()
    if (fromEnv.isEmpty() && bit == "64") {
        fromEnv = System.getenv("CHAQUOPY_BUILD_PYTHON")?.trim().orEmpty()
    }
    if (fromEnv.isNotEmpty()) {
        return fromEnv.split(Regex("\\s+")).filter { it.isNotEmpty() }.toTypedArray()
    }
    if (bit == "64") {
        return arrayOf("python")
    }
    val localAppData = System.getenv("LOCALAPPDATA").orEmpty()
    val python311Candidates = listOf(
        "${System.getProperty("user.home")}/.conda/envs/chaquopy311/python.exe",
        "C:/Anaconda/envs/chaquopy311/python.exe",
        "$localAppData/Programs/Python/Python311/python.exe",
        "C:/Python311/python.exe",
    )
    val found311 = python311Candidates.firstOrNull { File(it).isFile }
    if (found311 != null) {
        return arrayOf(found311)
    }
    val isWindows = System.getProperty("os.name").orEmpty().lowercase().contains("win")
    return if (isWindows) arrayOf("py", "-3.11") else arrayOf("python3.11")
}

android {
    namespace = "com.operations.rider"
    compileSdk = 34

    defaultConfig {
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        val remoteBase = escapeForBuildConfigString(buildConfigProp("OPS_REMOTE_API_BASE"))
        val jwtSigningKey = escapeForBuildConfigString(buildConfigProp("JWT_SIGNING_KEY"))
        val syncUser = escapeForBuildConfigString(buildConfigProp("OPS_SYNC_USERNAME"))
        val syncPassword = escapeForBuildConfigString(buildConfigProp("OPS_SYNC_PASSWORD"))
        val embeddedSecret = escapeForBuildConfigString(buildConfigProp("OPS_EMBEDDED_IMPORT_SECRET"))
        buildConfigField("String", "OPS_REMOTE_API_BASE", "\"$remoteBase\"")
        buildConfigField("String", "JWT_SIGNING_KEY", "\"$jwtSigningKey\"")
        buildConfigField("String", "OPS_SYNC_USERNAME", "\"$syncUser\"")
        buildConfigField("String", "OPS_SYNC_PASSWORD", "\"$syncPassword\"")
        buildConfigField("String", "OPS_EMBEDDED_IMPORT_SECRET", "\"$embeddedSecret\"")
    }

    flavorDimensions += listOf("brand", "abi")
    productFlavors {
        create("rider") {
            dimension = "brand"
            applicationId = "com.operations.rider"
        }
        create("ecollect") {
            dimension = "brand"
            isDefault = true
            applicationId = "com.ecollect.app"
        }
        create("abi32") {
            dimension = "abi"
            applicationIdSuffix = ".bit32"
            versionNameSuffix = "-32"
            ndk {
                abiFilters += listOf("armeabi-v7a")
            }
        }
        create("abi64") {
            dimension = "abi"
            isDefault = true
            applicationIdSuffix = ".bit64"
            versionNameSuffix = "-64"
            ndk {
                abiFilters += listOf("arm64-v8a", "x86_64")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        buildConfig = true
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
        }
    }
}

chaquopy {
    defaultConfig {
        pip {
            // app/ -> android/ -> repo root (requirements-android.txt)
            install("-r", "../../requirements-android.txt")
        }
        // tzdata ships zone files; extract so importlib.resources can load them from disk on Android.
        extractPackages("tzdata")
    }
    productFlavors {
        getByName("abi32") {
            // Python 3.11 is the newest Chaquopy runtime that still builds armeabi-v7a.
            version = "3.11"
            buildPython(*chaquopyBuildPythonArgs("32"))
        }
        getByName("abi64") {
            // Python 3.13: 64-bit only, including Android 15 16 KB page devices.
            version = "3.13"
            buildPython(*chaquopyBuildPythonArgs("64"))
        }
    }
}

val djangoRoot: java.io.File = rootProject.projectDir.parentFile

tasks.register<Copy>("syncDjangoProject") {
    group = "django"
    description = "Copy Django project into src/main/python for Chaquopy packaging"
    from(djangoRoot) {
        include(
            "config/**/*.py",
            "operations/**/*.py",
            "operations/**/*.html",
            "operations/**/*.json",
            "templates/**",
            "static/**",
            "manage.py",
        )
        exclude("**/new/**")
        exclude("**/__pycache__/**")
        exclude("**/*.pyc")
        exclude("**/.mypy_cache/**")
    }
    into(layout.projectDirectory.dir("src/main/python"))
}

tasks.register<Copy>("bundleSeedDatabase") {
    group = "django"
    description =
        "Copy repository db.sqlite3 into src/main/python/data/db.sqlite3 so the APK ships a pre-populated DB (skipped if db.sqlite3 is missing)"
    val seed = djangoRoot.resolve("db.sqlite3")
    onlyIf { seed.isFile }
    from(seed)
    rename { "db.sqlite3" }
    into(layout.projectDirectory.dir("src/main/python/data"))
}

tasks.named("preBuild") {
    dependsOn("syncDjangoProject", "bundleSeedDatabase")
}

// Gradle 8: Chaquopy merge*PythonSources must run after Django tree (and optional seed DB) are in place
tasks.configureEach {
    if (name.startsWith("merge") && name.endsWith("PythonSources")) {
        dependsOn("syncDjangoProject", "bundleSeedDatabase")
    }
}

android.applicationVariants.configureEach {
    val bit = if (flavorName.contains("abi32", ignoreCase = true)) "32" else "64"
    val brand = if (flavorName.contains("ecollect", ignoreCase = true)) "E-Collect" else "Operations-Rider"
    val typeName = buildType.name
    outputs.configureEach {
        (this as com.android.build.gradle.internal.api.BaseVariantOutputImpl).outputFileName =
            "$brand-$bit-$typeName.apk"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
}
