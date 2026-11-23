import os

def wf(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))

wf("android/gradle.properties", "android.useAndroidX=true\norg.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n")
wf("android/settings.gradle.kts", 'pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }\ndependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }\nrootProject.name = "ZarmaKeyboard"\ninclude(":app")\n')
wf("android/build.gradle.kts", 'plugins { id("com.android.application") version "8.5.2" apply false; id("org.jetbrains.kotlin.android") version "1.9.24" apply false }\n')
wf("android/app/build.gradle.kts", r"""
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.zedempires.zarmakeyboard"
    compileSdk = 34
    defaultConfig { applicationId = "com.zedempires.zarmakeyboard"; minSdk = 24; targetSdk = 34; versionCode = 2; versionName = "2.0.0" }
    buildTypes { release { isMinifyEnabled = false; proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro") } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
}
""")

wf("android/app/src/main/AndroidManifest.xml", r"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:allowBackup="true" android:label="Clavier Zarma Pro" android:supportsRtl="true" android:theme="@style/Theme.Material3.DayNight.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter>
        </activity>
        <service android:name=".ZarmaIMEService" android:exported="true" android:label="Clavier Zarma Pro (ELDAS)" android:permission="android.permission.BIND_INPUT_METHOD">
            <intent-filter><action android:name="android.view.InputMethod" /></intent-filter>
            <meta-data android:name="android.view.im" android:resource="@xml/method" />
        </service>
        <provider android:name="androidx.core.content.FileProvider" android:authorities="${applicationId}.fileprovider" android:exported="false" android:grantUriPermissions="true">
            <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
""")

wf("android/app/src/main/res/xml/method.xml", '<?xml version="1.0" encoding="utf-8"?>\n<input-method xmlns:android="http://schemas.android.com/apk/res/android" android:settingsActivity="com.zedempires.zarmakeyboard.MainActivity"><subtype android:label="Zarma (Niger)" android:imeSubtypeLocale="dje_NE" android:imeSubtypeMode="keyboard" /></input-method>\n')
wf("android/app/src/main/res/xml/file_paths.xml", '<?xml version="1.0" encoding="utf-8"?>\n<paths><cache-path name="shared_images" path="shared_images/" /></paths>\n')

wf("android/app/src/main/java/com/zedempires/zarmakeyboard/ThemeManager.kt", r"""
package com.zedempires.zarmakeyboard
import android.content.Context
import android.graphics.Color

data class KeyboardTheme(val id: String, val name: String, val bgColor: Int, val keyColor: Int, val actionKeyColor: Int, val textColor: Int, val hintColor: Int)

object ThemeManager {
    val PRESETS = listOf(
        KeyboardTheme("green", "Vert Zarma", Color.parseColor("#388E3C"), Color.parseColor("#57A05A"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#C8E6C9")),
        KeyboardTheme("eldas_blue", "Bleu ELDAS", Color.parseColor("#154360"), Color.parseColor("#1F618D"), Color.parseColor("#0E2F44"), Color.WHITE, Color.parseColor("#AED6F1")),
        KeyboardTheme("turquoise", "Turquoise Pro", Color.parseColor("#00796B"), Color.parseColor("#26A69A"), Color.parseColor("#004D40"), Color.WHITE, Color.parseColor("#B2DFDB")),
        KeyboardTheme("amoled", "Noir AMOLED", Color.parseColor("#000000"), Color.parseColor("#1E1E1E"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#A5D6A7")),
        KeyboardTheme("gold", "Or & Ardoise", Color.parseColor("#212121"), Color.parseColor("#37474F"), Color.parseColor("#F9A825"), Color.WHITE, Color.parseColor("#FFF59D")),
        KeyboardTheme("light", "Clair Moderne", Color.parseColor("#ECEFF1"), Color.parseColor("#FFFFFF"), Color.parseColor("#CFD8DC"), Color.parseColor("#212121"), Color.parseColor("#546E7A"))
    )

    private fun prefs(c: Context) = c.getSharedPreferences("zarma_pro_prefs", Context.MODE_PRIVATE)

    fun getCurrentTheme(c: Context): KeyboardTheme {
        val p = prefs(c)
        val id = p.getString("theme_id", "green") ?: "green"
        if (id == "custom") {
            return KeyboardTheme("custom", "Personnalisé", p.getInt("c_bg", Color.parseColor("#1B5E20")), p.getInt("c_key", Color.parseColor("#2E7D32")), p.getInt("c_act", Color.parseColor("#F9A825")), p.getInt("c_txt", Color.WHITE), Color.parseColor("#E0E0E0"))
        }
        return PRESETS.find { it.id == id } ?: PRESETS.first()
    }

    fun setThemeId(c: Context, id: String) { prefs(c).edit().putString("theme_id", id).apply() }

    fun saveCustomColors(c: Context, bgHex: String, keyHex: String, actHex: String, txtHex: String): Boolean {
        return try {
            prefs(c).edit().putString("theme_id", "custom").putInt("c_bg", Color.parseColor(bgHex.trim())).putInt("c_key", Color.parseColor(keyHex.trim())).putInt("c_act", Color.parseColor(actHex.trim())).putInt("c_txt", Color.parseColor(txtHex.trim())).apply()
            true
        } catch (_: Exception) { false }
    }

    fun nextTheme(c: Context): KeyboardTheme {
        val cur = getCurrentTheme(c)
        val idx = PRESETS.indexOfFirst { it.id == cur.id }
        val next = PRESETS[(idx + 1) % PRESETS.size]
        setThemeId(c, next.id); return next
    }

    fun getKeyHeightDp(c: Context): Int = prefs(c).getInt("key_height", 50)
    fun setKeyHeightDp(c: Context, h: Int) = prefs(c).edit().putInt("key_height", h).apply()
    fun isHapticEnabled(c: Context): Boolean = prefs(c).getBoolean("haptic", true)
    fun setHapticEnabled(c: Context, v: Boolean) = prefs(c).edit().putBoolean("haptic", v).apply()
    fun isPopupEnabled(c: Context): Boolean = prefs(c).getBoolean("popup", true)
    fun setPopupEnabled(c: Context, v: Boolean) = prefs(c).edit().putBoolean("popup", v).apply()
    fun isSoundEnabled(c: Context): Boolean = prefs(c).getBoolean("sound", false)
    fun setSoundEnabled(c: Context, v: Boolean) = prefs(c).edit().putBoolean("sound", v).apply()
}
""")

wf("android/app/src/main/java/com/zedempires/zarmakeyboard/VectorIcons.kt", r"""
package com.zedempires.zarmakeyboard
import android.content.Context
import android.graphics.*
import android.graphics.drawable.BitmapDrawable

object VectorIcons {
    fun draw(context: Context, type: String, color: Int, sizeDp: Int = 22): BitmapDrawable {
        val px = (sizeDp * context.resources.displayMetrics.density).toInt().coerceAtLeast(24)
        val bmp = Bitmap.createBitmap(px, px, Bitmap.Config.ARGB_8888)
        val c = Canvas(bmp)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { this.color = color; style = Paint.Style.STROKE; strokeWidth = px * 0.09f; strokeCap = Paint.Cap.ROUND; strokeJoin = Paint.Join.ROUND }
        val w = px.toFloat(); val h = px.toFloat(); val path = Path()
        when (type) {
            "shift", "shift_on" -> {
                path.moveTo(w*0.5f, h*0.18f); path.lineTo(w*0.84f, h*0.54f); path.lineTo(w*0.66f, h*0.54f); path.lineTo(w*0.66f, h*0.82f); path.lineTo(w*0.34f, h*0.82f); path.lineTo(w*0.34f, h*0.54f); path.lineTo(w*0.16f, h*0.54f); path.close()
                if (type == "shift_on") p.style = Paint.Style.FILL_AND_STROKE
                c.drawPath(path, p)
            }
            "backspace" -> {
                path.moveTo(w*0.32f, h*0.24f); path.lineTo(w*0.86f, h*0.24f); path.lineTo(w*0.86f, h*0.76f); path.lineTo(w*0.32f, h*0.76f); path.lineTo(w*0.12f, h*0.50f); path.close()
                c.drawPath(path, p); c.drawLine(w*0.46f, h*0.38f, w*0.70f, h*0.62f, p); c.drawLine(w*0.70f, h*0.38f, w*0.46f, h*0.62f, p)
            }
            "enter" -> {
                path.moveTo(w*0.78f, h*0.26f); path.lineTo(w*0.78f, h*0.56f); path.lineTo(w*0.24f, h*0.56f); c.drawPath(path, p)
                c.drawLine(w*0.40f, h*0.40f, w*0.24f, h*0.56f, p); c.drawLine(w*0.40f, h*0.72f, w*0.24f, h*0.56f, p)
            }
            "palette" -> {
                c.drawCircle(w*0.5f, h*0.5f, w*0.36f, p); p.style = Paint.Style.FILL
                c.drawCircle(w*0.38f, h*0.38f, w*0.06f, p); c.drawCircle(w*0.62f, h*0.38f, w*0.06f, p); c.drawCircle(w*0.36f, h*0.58f, w*0.06f, p)
            }
            "share_img" -> {
                c.drawRoundRect(RectF(w*0.16f, h*0.20f, w*0.84f, h*0.80f), w*0.1f, w*0.1f, p)
                path.moveTo(w*0.24f, h*0.68f); path.lineTo(w*0.44f, h*0.46f); path.lineTo(w*0.58f, h*0.60f); path.lineTo(w*0.68f, h*0.50f); path.lineTo(w*0.78f, h*0.68f); c.drawPath(path, p)
            }
            "settings" -> { c.drawCircle(w*0.5f, h*0.5f, w*0.18f, p); c.drawCircle(w*0.5f, h*0.5f, w*0.34f, p) }
        }
        return BitmapDrawable(context.resources, bmp)
    }
}
""")

wf("android/app/src/main/java/com/zedempires/zarmakeyboard/ZarmaDictionary.kt", r"""
package com.zedempires.zarmakeyboard

object ZarmaDictionary {
    val WORDS = listOf(
        "\uE014\uE002\uE01F\uE002", "\uE016\uE009\uE015\uE002", "\uE017\uE002\uE01F\uE029\uE002",
        "\uE01A\uE000\uE014\uE003", "\uE016\uE007\uE017\uE000\uE022", "\uE01B\uE000\uE02B\uE020\uE000\uE02B\uE014\uE004\uE02E",
        "\uE01D\uE002\uE023\uE000\uE015\uE001\uE02E", "\uE01C\uE000\uE01F\uE017\uE004\uE02E", "\uE01E\uE000\uE021\uE001\uE02E",
        "\uE020\uE000\uE01C\uE014\uE000\uE02E", "\uE021\uE000\uE005\uE016\uE001\uE02E", "\uE028\uE000\uE022",
        "\uE024\uE007\uE01A\uE000", "\uE029\uE000\uE02B\uE01F\uE001", "\uE025\uE000\uE02B",
        "\uE027\uE000\uE014\uE005", "\uE020\uE007\uE015\uE005", "\uE01C\uE001\uE02B\uE01B\uE000\uE02E",
        "\uE023\uE000\uE02B\uE01C\uE002", "\uE000\uE016\uE002", "\uE001\uE018\uE008\uE01A\uE000",
        "\uE001\uE018\uE008\uE024\uE000", "\uE001\uE021\uE000\uE027\uE001", "\uE001\uE017\uE004",
        "\uE001\uE015\uE004", "\uE001\uE023\uE003", "\uE001\uE018\uE000\uE01A\uE004",
        "\uE001\uE023\uE003\uE017\uE000", "\uE024\uE007\uE017\uE004", "\uE024\uE000\uE01C\uE014\uE000\uE01F",
        "\uE018\uE000\uE022\uE000\uE01F\uE001"
    )
    fun suggest(prefix: String): List<String> {
        if (prefix.isEmpty()) return listOf("\uE014\uE002\uE01F\uE002", "\uE024\uE007\uE01A\uE000", "\uE016\uE009\uE015\uE002")
        val matches = WORDS.filter { it.startsWith(prefix) && it != prefix }.take(3).toMutableList()
        if (matches.size < 3) matches.add(prefix + "\uE02C")
        if (matches.size < 3) matches.add(prefix + "\uE02E")
        return matches.take(3)
    }
}
""")

wf("android/app/src/main/java/com/zedempires/zarmakeyboard/ZarmaImageRenderer.kt", r"""
package com.zedempires.zarmakeyboard
import android.content.Context
import android.content.Intent
import android.graphics.*
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import androidx.core.content.FileProvider
import java.io.File
import java.io.FileOutputStream

object ZarmaImageRenderer {
    fun shareTextAsImage(context: Context, rawText: String, font: Typeface, theme: KeyboardTheme) {
        val text = rawText.trim().ifEmpty { "\uE014\uE002\uE01F\uE002 \uE02C" }
        val width = 1080; val pad = 72
        val tp = TextPaint(Paint.ANTI_ALIAS_FLAG).apply { typeface = font; color = theme.textColor; textSize = 76f }
        val layout = StaticLayout.Builder.obtain(text, 0, text.length, tp, width - pad * 2).setAlignment(Layout.Alignment.ALIGN_NORMAL).setLineSpacing(16f, 1.15f).build()
        val height = (layout.height + pad * 2 + 64).coerceAtLeast(360)
        val bmp = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bmp)
        canvas.drawRoundRect(RectF(0f, 0f, width.toFloat(), height.toFloat()), 44f, 44f, Paint(Paint.ANTI_ALIAS_FLAG).apply { color = theme.bgColor })
        canvas.drawRoundRect(RectF(16f, 16f, width - 16f, height - 16f), 36f, 36f, Paint(Paint.ANTI_ALIAS_FLAG).apply { color = theme.keyColor; style = Paint.Style.STROKE; strokeWidth = 10f })
        canvas.save(); canvas.translate(pad.toFloat(), pad.toFloat()); layout.draw(canvas); canvas.restore()
        canvas.drawText("ZARMA • ACADÉMIE ELDAS", pad.toFloat(), (height - 32).toFloat(), Paint(Paint.ANTI_ALIAS_FLAG).apply { color = theme.hintColor; textSize = 28f; typeface = Typeface.DEFAULT_BOLD })
        val dir = File(context.cacheDir, "shared_images").apply { mkdirs() }
        val file = File(dir, "zarma_message.png")
        FileOutputStream(file).use { bmp.compress(Bitmap.CompressFormat.PNG, 100, it) }
        val uri = FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file)
        val shareIntent = Intent(Intent.ACTION_SEND).apply { type = "image/png"; putExtra(Intent.EXTRA_STREAM, uri); addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION) }
        context.startActivity(Intent.createChooser(shareIntent, "Envoyer l'écriture Zarma").apply { addFlags(Intent.FLAG_ACTIVITY_NEW_TASK) })
    }
}
""")
print("[OK] Moteur Android Pro généré.")
