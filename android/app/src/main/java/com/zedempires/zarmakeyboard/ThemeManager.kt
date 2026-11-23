package com.zedempires.zarmakeyboard
import android.content.Context
import android.graphics.Color

data class KeyboardTheme(val id: String, val name: String, val bgColor: Int, val keyColor: Int, val actionKeyColor: Int, val textColor: Int, val hintColor: Int)

object ThemeManager {
    val THEMES = listOf(
        KeyboardTheme("green", "Vert Zarma", Color.parseColor("#388E3C"), Color.parseColor("#57A05A"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#C8E6C9")),
        KeyboardTheme("eldas_blue", "Bleu ELDAS", Color.parseColor("#154360"), Color.parseColor("#1F618D"), Color.parseColor("#0E2F44"), Color.WHITE, Color.parseColor("#AED6F1")),
        KeyboardTheme("turquoise", "Turquoise", Color.parseColor("#00796B"), Color.parseColor("#26A69A"), Color.parseColor("#004D40"), Color.WHITE, Color.parseColor("#B2DFDB")),
        KeyboardTheme("amoled", "Noir AMOLED", Color.parseColor("#000000"), Color.parseColor("#1E1E1E"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#A5D6A7")),
        KeyboardTheme("gold", "Or & Ardoise", Color.parseColor("#212121"), Color.parseColor("#37474F"), Color.parseColor("#F9A825"), Color.WHITE, Color.parseColor("#FFF59D"))
    )
    fun getCurrentTheme(context: Context): KeyboardTheme {
        val id = context.getSharedPreferences("zarma_kbd_prefs", Context.MODE_PRIVATE).getString("theme_id", "green")
        return THEMES.find { it.id == id } ?: THEMES.first()
    }
    fun nextTheme(context: Context): KeyboardTheme {
        val current = getCurrentTheme(context)
        val next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.size]
        context.getSharedPreferences("zarma_kbd_prefs", Context.MODE_PRIVATE).edit().putString("theme_id", next.id).apply()
        return next
    }
}
