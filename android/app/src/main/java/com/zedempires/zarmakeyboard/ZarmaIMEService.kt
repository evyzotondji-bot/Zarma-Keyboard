package com.zedempires.zarmakeyboard
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.inputmethodservice.InputMethodService
import android.util.TypedValue
import android.view.*
import android.widget.*

class ZarmaIMEService : InputMethodService() {
    private lateinit var zarmaFont: Typeface
    private lateinit var rootLayout: LinearLayout
    private var isShift = false
    private var isSymbols = false

    private val row1Lower = listOf(Pair("\uE000","\uE034"), Pair("\uE024","\uE035"), Pair("\uE003","\uE036"), Pair("\uE01F","\uE037"), Pair("\uE021","\uE038"), Pair("\uE023","\uE039"), Pair("\uE004","\uE03A"), Pair("\uE001","\uE03B"), Pair("\uE002","\uE03C"), Pair("\uE01E","\uE033"))
    private val row2Lower = listOf("\uE005","\uE020","\uE015","\uE016","\uE017","\uE018","\uE019","\uE01A","\uE01B","\uE01C")
    private val row3Lower = listOf("\uE022","\uE006","\uE007","\uE008","\uE009","\uE014","\uE01D")
    private val row1Upper = listOf(Pair("\uE00A","\uE034"), Pair("\uE02A","\uE035"), Pair("\uE00D","\uE036"), Pair("\uE025","\uE037"), Pair("\uE027","\uE038"), Pair("\uE026","\uE039"), Pair("\uE00E","\uE03A"), Pair("\uE00B","\uE03B"), Pair("\uE00C","\uE03C"), Pair("\uE028","\uE033"))
    private val row2Upper = listOf("\uE00F","\uE029","\uE015","\uE016","\uE017","\uE018","\uE019","\uE01A","\uE01B","\uE01C")
    private val row3Upper = listOf("\uE022","\uE010","\uE011","\uE012","\uE013","\uE014","\uE01D")
    private val symRow1 = listOf("\uE034","\uE035","\uE036","\uE037","\uE038","\uE039","\uE03A","\uE03B","\uE03C","\uE033")
    private val symRow2 = listOf("\uE03D","\uE03E","\uE03F","\uE040","\uE041","\uE042","\uE043","\uE044","\uE045")
    private val symRow3 = listOf("\uE02B","\uE02C","\uE02D","\uE02E","\uE02F","\uE030","\uE031","\uE032")

    override fun onCreate() { super.onCreate(); zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf") }
    override fun onCreateInputView(): View {
        rootLayout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(8, 8, 8, 16) }
        renderKeyboard()
        return rootLayout
    }
    private fun dp(v: Int): Int = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()
    private fun makeKeyBg(color: Int, radiusDp: Int = 10) = GradientDrawable().apply { setColor(color); cornerRadius = dp(radiusDp).toFloat() }

    private fun renderKeyboard() {
        val theme = ThemeManager.getCurrentTheme(this)
        rootLayout.removeAllViews(); rootLayout.setBackgroundColor(theme.bgColor)
        val topBar = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(12, 4, 12, 10) }
        val titleView = TextView(this).apply { text = "ZARMA • ${theme.name}"; setTextColor(theme.hintColor); textSize = 13f; layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f) }
        val paletteBtn = TextView(this).apply {
            text = "🎨 Couleur"; setTextColor(theme.textColor); textSize = 13f; setPadding(dp(12), dp(6), dp(12), dp(6)); background = makeKeyBg(theme.actionKeyColor, 16)
            setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); ThemeManager.nextTheme(this@ZarmaIMEService); renderKeyboard() }
        }
        topBar.addView(titleView); topBar.addView(paletteBtn); rootLayout.addView(topBar)
        if (isSymbols) {
            rootLayout.addView(buildSimpleRow(symRow1, theme)); rootLayout.addView(buildSimpleRow(symRow2, theme)); rootLayout.addView(buildRow3(symRow3, theme, false))
        } else {
            rootLayout.addView(buildRow1(if (isShift) row1Upper else row1Lower, theme))
            rootLayout.addView(buildSimpleRow(if (isShift) row2Upper else row2Lower, theme))
            rootLayout.addView(buildRow3(if (isShift) row3Upper else row3Lower, theme, true))
        }
        rootLayout.addView(buildBottomRow(theme))
    }

    private fun buildRow1(keys: List<Pair<String, String>>, theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for ((mainChar, numHint) in keys) {
            val cell = FrameLayout(this).apply {
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }; background = makeKeyBg(theme.keyColor)
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(mainChar, 1) }
                setOnLongClickListener { it.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS); currentInputConnection?.commitText(numHint, 1); true }
            }
            cell.addView(TextView(this).apply { text = mainChar; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER })
            cell.addView(TextView(this).apply { text = numHint; typeface = zarmaFont; setTextColor(theme.hintColor); textSize = 11f; gravity = Gravity.TOP or Gravity.END; setPadding(0, dp(2), dp(5), 0) })
            row.addView(cell)
        }
        return row
    }

    private fun buildSimpleRow(keys: List<String>, theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for (ch in keys) {
            row.addView(TextView(this).apply {
                text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER; background = makeKeyBg(theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(ch, 1) }
            })
        }
        return row
    }

    private fun buildRow3(keys: List<String>, theme: KeyboardTheme, showShift: Boolean): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        if (showShift) {
            row.addView(TextView(this).apply {
                text = if (isShift) "⬆" else "⇧"; setTextColor(theme.textColor); textSize = 20f; gravity = Gravity.CENTER
                background = makeKeyBg(if (isShift) theme.actionKeyColor else theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1.3f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { isShift = !isShift; renderKeyboard() }
            })
        }
        for (ch in keys) {
            row.addView(TextView(this).apply {
                text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER; background = makeKeyBg(theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(ch, 1) }
            })
        }
        row.addView(TextView(this).apply {
            text = "⌫"; setTextColor(theme.textColor); textSize = 20f; gravity = Gravity.CENTER; background = makeKeyBg(theme.actionKeyColor)
            layoutParams = LinearLayout.LayoutParams(0, dp(50), 1.4f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
            setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.deleteSurroundingText(1, 0) }
        })
        return row
    }

    private fun buildBottomRow(theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        val addKey = { txt: String, zFont: Boolean, w: Float, bg: Int, rad: Int, onClick: () -> Unit ->
            row.addView(TextView(this).apply {
                text = txt; if (zFont) typeface = zarmaFont; setTextColor(theme.textColor); textSize = if (zFont) 20f else 17f; gravity = Gravity.CENTER; background = makeKeyBg(bg, rad)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), w).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { onClick() }
            })
        }
        addKey(if (isSymbols) "\uE000\uE014" else "\uE034\uE035\uE036", true, 1.5f, theme.actionKeyColor, 18) { isSymbols = !isSymbols; renderKeyboard() }
        addKey("\uE02C", true, 1f, theme.keyColor, 10) { currentInputConnection?.commitText("\uE02C", 1) }
        addKey("Zarma", false, 3.8f, theme.keyColor, 14) { currentInputConnection?.commitText(" ", 1) }
        addKey("\uE02D", true, 1f, theme.keyColor, 10) { currentInputConnection?.commitText("\uE02D", 1) }
        addKey("↵", false, 1.5f, theme.actionKeyColor, 24) { currentInputConnection?.commitText("\n", 1) }
        return row
    }
}
