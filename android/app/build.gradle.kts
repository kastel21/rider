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

android {
    namespace = "com.operations.rider"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.operations.rider"
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

        // Python 3.12+ (incl. 3.13) supports only 64-bit ABIs in Chaquopy
        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
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
        // Must match a Python interpreter on the build machine (major.minor).
        version = "3.13"
        buildPython(System.getenv("CHAQUOPY_BUILD_PYTHON") ?: "python")
        pip {
            // app/ -> android/ -> repo root (requirements-android.txt)
            install("-r", "../../requirements-android.txt")
        }
        // tzdata ships zone files; extract so importlib.resources can load them from disk on Android.
        extractPackages("tzdata")
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

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
}
