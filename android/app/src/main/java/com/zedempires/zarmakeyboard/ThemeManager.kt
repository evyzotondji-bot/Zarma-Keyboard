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
