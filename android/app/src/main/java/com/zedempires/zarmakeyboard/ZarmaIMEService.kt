package com.zedempires.zarmakeyboard
import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.inputmethodservice.InputMethodService
import android.media.AudioManager
import android.os.Handler
import android.os.Looper
import android.util.TypedValue
import android.view.*
import android.widget.*

class ZarmaIMEService : InputMethodService() {
    private lateinit var zarmaFont: Typeface
    private lateinit var rootLayout: LinearLayout
    private lateinit var suggestionRow: LinearLayout
    private var previewPopup: PopupWindow? = null
    private lateinit var previewTv: TextView
    private var isShift = false
    private var mode = 0
    private val repeatHandler = Handler(Looper.getMainLooper())

    private val row1Lower = listOf(Pair("\uE000","\uE034"), Pair("\uE024","\uE035"), Pair("\uE003","\uE036"), Pair("\uE01F","\uE037"), Pair("\uE021","\uE038"), Pair("\uE023","\uE039"), Pair("\uE004","\uE03A"), Pair("\uE001","\uE03B"), Pair("\uE002","\uE03C"), Pair("\uE01E","\uE033"))
    private val row2Lower = listOf("\uE005","\uE020","\uE015","\uE016","\uE017","\uE018","\uE019","\uE01A","\uE01B","\uE01C")
    private val row3Lower = listOf("\uE022","\uE006","\uE007","\uE008","\uE009","\uE014","\uE01D")
    private val row1Upper = listOf(Pair("\uE00A","\uE034"), Pair("\uE02A","\uE035"), Pair("\uE00D","\uE036"), Pair("\uE025","\uE037"), Pair("\uE027","\uE038"), Pair("\uE026","\uE039"), Pair("\uE00E","\uE03A"), Pair("\uE00B","\uE03B"), Pair("\uE00C","\uE03C"), Pair("\uE028","\uE033"))
    private val row2Upper = listOf("\uE00F","\uE029","\uE015","\uE016","\uE017","\uE018","\uE019","\uE01A","\uE01B","\uE01C")
    private val row3Upper = listOf("\uE022","\uE010","\uE011","\uE012","\uE013","\uE014","\uE01D")
    private val symRow1 = listOf("\uE034","\uE035","\uE036","\uE037","\uE038","\uE039","\uE03A","\uE03B","\uE03C","\uE033")
    private val symRow2 = listOf("\uE03D","\uE03E","\uE03F","\uE040","\uE02B","\uE02C","\uE02D","\uE02E","\uE02F")
    private val symRow3 = listOf("\uE030","\uE031","\uE032","\uE041","\uE042","\uE043","\uE044","\uE045")
    private val abbrRow1 = listOf("\uE041","\uE046","\uE047","\uE048","\uE045","\uE044","\uE049")
    private val abbrRow2 = listOf("\uE04A","\uE042","\uE04B","\uE04C","\uE043","\uE04D","\uE04E","\uE04F")

    override fun onCreate() {
        super.onCreate()
        zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf")
        previewTv = TextView(this).apply { typeface = zarmaFont; textSize = 36f; gravity = Gravity.CENTER }
        previewPopup = PopupWindow(previewTv, dp(58), dp(68), false).apply { isTouchable = false; elevation = dp(6).toFloat() }
    }
    override fun onFinishInputView(finishingInput: Boolean) { super.onFinishInputView(finishingInput); previewPopup?.dismiss(); repeatHandler.removeCallbacksAndMessages(null) }
    override fun onCreateInputView(): View {
        rootLayout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(6, 6, 6, 14) }
        renderKeyboard(); return rootLayout
    }
    private fun dp(v: Int): Int = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()
    private fun makeBg(color: Int, radDp: Int = 10) = GradientDrawable().apply { setColor(color); cornerRadius = dp(radDp).toFloat() }
    private fun feedback(v: View) {
        if (ThemeManager.isHapticEnabled(this)) v.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP)
        if (ThemeManager.isSoundEnabled(this)) (getSystemService(Context.AUDIO_SERVICE) as AudioManager).playSoundEffect(AudioManager.FX_KEY_CLICK, 0.5f)
    }
    private fun showPopup(anchor: View, ch: String, theme: KeyboardTheme) {
        if (!ThemeManager.isPopupEnabled(this)) return
        previewTv.text = ch; previewTv.setTextColor(theme.textColor); previewTv.background = makeBg(theme.actionKeyColor, 14)
        val loc = IntArray(2); anchor.getLocationInWindow(loc)
        previewPopup?.dismiss()
        previewPopup?.showAtLocation(rootLayout, Gravity.NO_GRAVITY, loc[0] + (anchor.width - dp(58)) / 2, (loc[1] - dp(72)).coerceAtLeast(8))
    }
    private fun commitZarma(txt: String) { currentInputConnection?.commitText(txt, 1); updateSuggestions() }
    private fun getCurrentWordPrefix(): String {
        val before = currentInputConnection?.getTextBeforeCursor(24, 0)?.toString() ?: return ""
        return before.takeLastWhile { it != ' ' && it != '\n' && it != '\uE02C' && it != '\uE02D' }
    }
    private fun updateSuggestions() {
        if (!::suggestionRow.isInitialized) return
        val theme = ThemeManager.getCurrentTheme(this); val prefix = getCurrentWordPrefix()
        suggestionRow.removeAllViews()
        for (word in ZarmaDictionary.suggest(prefix)) {
            suggestionRow.addView(TextView(this).apply {
                text = word; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 20f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor, 8)
                layoutParams = LinearLayout.LayoutParams(0, dp(36), 1f).apply { setMargins(dp(3), 0, dp(3), 0) }
                setOnClickListener { feedback(it); if (prefix.isNotEmpty()) currentInputConnection?.deleteSurroundingText(prefix.length, 0); commitZarma(word + " ") }
            })
        }
    }
    private fun renderKeyboard() {
        val theme = ThemeManager.getCurrentTheme(this); val kh = dp(ThemeManager.getKeyHeightDp(this))
        rootLayout.removeAllViews(); rootLayout.setBackgroundColor(theme.bgColor)
        val topBar = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(6, 2, 6, 6) }
        val addToolBtn = { label: String, iconType: String?, onClick: () -> Unit ->
            val btn = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER; setPadding(dp(10), dp(5), dp(10), dp(5)); background = makeBg(theme.actionKeyColor, 14)
                layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, dp(34)).apply { setMargins(dp(3), 0, dp(3), 0) }
                setOnClickListener { feedback(it); onClick() }
            }
            if (iconType != null) btn.addView(ImageView(this).apply { setImageDrawable(VectorIcons.draw(this@ZarmaIMEService, iconType, theme.textColor, 18)) })
            if (label.isNotEmpty()) btn.addView(TextView(this).apply { text = label; setTextColor(theme.textColor); textSize = 12f; if (label.startsWith("\uE041")) typeface = zarmaFont; setPadding(if (iconType != null) dp(5) else 0, 0, 0, 0) })
            topBar.addView(btn)
        }
        addToolBtn(if (mode == 2) "ABC" else "\uE041\uE042", null) { mode = if (mode == 2) 0 else 2; renderKeyboard() }
        addToolBtn("Image", "share_img") { ZarmaImageRenderer.shareTextAsImage(this, currentInputConnection?.getTextBeforeCursor(200, 0)?.toString().orEmpty(), zarmaFont, theme) }
        addToolBtn("Thème", "palette") { ThemeManager.nextTheme(this); renderKeyboard() }
        addToolBtn("", "settings") { startActivity(Intent(this, MainActivity::class.java).apply { addFlags(Intent.FLAG_ACTIVITY_NEW_TASK) }) }
        rootLayout.addView(topBar)
        suggestionRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setPadding(4, 0, 4, 6) }
        rootLayout.addView(suggestionRow); updateSuggestions()
        when (mode) {
            1 -> { rootLayout.addView(buildRow(symRow1, theme, kh)); rootLayout.addView(buildRow(symRow2, theme, kh)); rootLayout.addView(buildRow3(symRow3, theme, kh, false)) }
            2 -> { rootLayout.addView(buildRow(abbrRow1, theme, kh)); rootLayout.addView(buildRow3(abbrRow2, theme, kh, false)) }
            else -> { rootLayout.addView(buildRow1Hints(if (isShift) row1Upper else row1Lower, theme, kh)); rootLayout.addView(buildRow(if (isShift) row2Upper else row2Lower, theme, kh)); rootLayout.addView(buildRow3(if (isShift) row3Upper else row3Lower, theme, kh, true)) }
        }
        rootLayout.addView(buildBottomRow(theme, kh))
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun attachKeyTouch(view: View, ch: String, theme: KeyboardTheme, onCommit: () -> Unit) {
        view.setOnTouchListener { v, ev ->
            when (ev.action) {
                MotionEvent.ACTION_DOWN -> { feedback(v); v.alpha = 0.75f; showPopup(v, ch, theme) }
                MotionEvent.ACTION_UP -> { v.alpha = 1f; previewPopup?.dismiss(); onCommit() }
                MotionEvent.ACTION_CANCEL -> { v.alpha = 1f; previewPopup?.dismiss() }
            }; true
        }
    }

    private fun buildRow1Hints(keys: List<Pair<String, String>>, theme: KeyboardTheme, kh: Int): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for ((mainChar, hintChar) in keys) {
            val cell = FrameLayout(this).apply { layoutParams = LinearLayout.LayoutParams(0, kh, 1f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }; background = makeBg(theme.keyColor) }
            cell.addView(TextView(this).apply { text = mainChar; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 23f; gravity = Gravity.CENTER })
            cell.addView(TextView(this).apply { text = hintChar; typeface = zarmaFont; setTextColor(theme.hintColor); textSize = 10f; gravity = Gravity.TOP or Gravity.END; setPadding(0, dp(2), dp(4), 0) })
            var longTriggered = false
            cell.setOnLongClickListener { longTriggered = true; showPopup(it, hintChar, theme); commitZarma(hintChar); true }
            cell.setOnClickListener { if (!longTriggered) commitZarma(mainChar); longTriggered = false; previewPopup?.dismiss() }
            row.addView(cell)
        }
        return row
    }

    private fun buildRow(keys: List<String>, theme: KeyboardTheme, kh: Int): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for (ch in keys) {
            val tv = TextView(this).apply { text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 23f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) } }
            attachKeyTouch(tv, ch, theme) { commitZarma(ch) }; row.addView(tv)
        }
        return row
    }
    @SuppressLint("ClickableViewAccessibility")
    private fun buildRow3(keys: List<String>, theme: KeyboardTheme, kh: Int, showShift: Boolean): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        if (showShift) {
            row.addView(ImageView(this).apply {
                setImageDrawable(VectorIcons.draw(this@ZarmaIMEService, if (isShift) "shift_on" else "shift", theme.textColor, 22)); scaleType = ImageView.ScaleType.CENTER
                background = makeBg(if (isShift) theme.actionKeyColor else theme.keyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1.3f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }
                setOnClickListener { feedback(it); isShift = !isShift; renderKeyboard() }
            })
        }
        for (ch in keys) {
            val tv = TextView(this).apply { text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 23f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) } }
            attachKeyTouch(tv, ch, theme) { commitZarma(ch) }; row.addView(tv)
        }
        val delBtn = ImageView(this).apply { setImageDrawable(VectorIcons.draw(this@ZarmaIMEService, "backspace", theme.textColor, 22)); scaleType = ImageView.ScaleType.CENTER; background = makeBg(theme.actionKeyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1.4f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) } }
        var downX = 0f; var swiped = false
        val repeatRun = object : Runnable { override fun run() { currentInputConnection?.deleteSurroundingText(1, 0); updateSuggestions(); repeatHandler.postDelayed(this, 55) } }
        delBtn.setOnTouchListener { v, ev ->
            when (ev.action) {
                MotionEvent.ACTION_DOWN -> { downX = ev.x; swiped = false; feedback(v); v.alpha = 0.75f; currentInputConnection?.deleteSurroundingText(1, 0); updateSuggestions(); repeatHandler.postDelayed(repeatRun, 420) }
                MotionEvent.ACTION_MOVE -> { if (downX - ev.x > dp(42)) swiped = true }
                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    v.alpha = 1f; repeatHandler.removeCallbacks(repeatRun)
                    if (swiped) {
                        val before = currentInputConnection?.getTextBeforeCursor(32, 0)?.toString().orEmpty()
                        val trimLen = before.length - before.trimEnd().dropLastWhile { it != ' ' }.length
                        if (trimLen > 0) currentInputConnection?.deleteSurroundingText(trimLen, 0); updateSuggestions()
                    }
                }
            }; true
        }
        row.addView(delBtn); return row
    }

    private fun buildBottomRow(theme: KeyboardTheme, kh: Int): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        row.addView(TextView(this).apply { text = if (mode == 1) "\uE000\uE014" else "\uE034\uE035\uE036"; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 18f; gravity = Gravity.CENTER; background = makeBg(theme.actionKeyColor, 18); layoutParams = LinearLayout.LayoutParams(0, kh, 1.5f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }; setOnClickListener { feedback(it); mode = if (mode == 1) 0 else 1; renderKeyboard() } })
        row.addView(TextView(this).apply { text = "\uE02C"; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 21f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }; setOnClickListener { feedback(it); commitZarma("\uE02C") } })
        row.addView(TextView(this).apply { text = "Zarma"; setTextColor(theme.textColor); textSize = 15f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor, 14); layoutParams = LinearLayout.LayoutParams(0, kh, 3.8f).apply { setMargins(dp(3), dp(3), dp(3), dp(3)) }; setOnClickListener { feedback(it); commitZarma(" ") } })
        row.addView(TextView(this).apply { text = "\uE02D"; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 21f; gravity = Gravity.CENTER; background = makeBg(theme.keyColor); layoutParams = LinearLayout.LayoutParams(0, kh, 1f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }; setOnClickListener { feedback(it); commitZarma("\uE02D") } })
        row.addView(ImageView(this).apply { setImageDrawable(VectorIcons.draw(this@ZarmaIMEService, "enter", theme.textColor, 22)); scaleType = ImageView.ScaleType.CENTER; background = makeBg(theme.actionKeyColor, 24); layoutParams = LinearLayout.LayoutParams(0, kh, 1.5f).apply { setMargins(dp(2), dp(3), dp(2), dp(3)) }; setOnClickListener { feedback(it); commitZarma("\n") } })
        return row
    }
}
