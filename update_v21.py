import os, glob

# 1. Basculer tous les codes Kotlin & PowerShell de \uE0xx vers \uE8xx (évite les emojis WhatsApp)
for path in glob.glob("android/**/*.kt", recursive=True) + glob.glob("windows/*.ps1"):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    s = s.replace("\\uE0", "\\uE8").replace("0xE0", "0xE8").replace("v2.0", "v2.1").replace("versionCode = 2", "versionCode = 3").replace('versionName = "2.0.0"', 'versionName = "2.1.0"')
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)

# 2. Ajouter la Barre d'Aperçu Zarma Curviligne en direct dans ZarmaIMEService.kt
ime_path = "android/app/src/main/java/com/zedempires/zarmakeyboard/ZarmaIMEService.kt"
with open(ime_path, "r", encoding="utf-8") as f:
    ime = f.read()

old_field = "    private lateinit var suggestionRow: LinearLayout"
new_field = "    private lateinit var suggestionRow: LinearLayout\n    private lateinit var livePreviewTv: TextView"
ime = ime.replace(old_field, new_field)

old_commit = "    private fun commitZarma(txt: String) { currentInputConnection?.commitText(txt, 1); updateSuggestions() }"
new_commit = """    private fun refreshLivePreview() {
        if (!::livePreviewTv.isInitialized) return
        val cur = currentInputConnection?.getTextBeforeCursor(120, 0)?.toString().orEmpty()
        livePreviewTv.text = if (cur.isEmpty()) "\\uE814\\uE802\\uE81F\\uE802 \\uE82C" else cur
        livePreviewTv.alpha = if (cur.isEmpty()) 0.55f else 1.0f
    }
    private fun commitZarma(txt: String) { currentInputConnection?.commitText(txt, 1); updateSuggestions(); refreshLivePreview() }"""
ime = ime.replace(old_commit, new_commit)

old_sug = "        rootLayout.addView(suggestionRow); updateSuggestions()"
new_sug = """        val previewBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL
            background = makeBg(theme.keyColor, 10); setPadding(dp(10), dp(4), dp(6), dp(4))
            layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT).apply { setMargins(dp(4), 0, dp(4), dp(5)) }
        }
        livePreviewTv = TextView(this).apply {
            typeface = zarmaFont; setTextColor(theme.textColor); textSize = 22f; maxLines = 1
            layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
        }
        val sendImgBtn = TextView(this).apply {
            text = "Envoyer"; setTextColor(theme.textColor); textSize = 12f
            background = makeBg(theme.actionKeyColor, 12); setPadding(dp(10), dp(5), dp(10), dp(5))
            setOnClickListener {
                feedback(it)
                val txt = currentInputConnection?.getTextBeforeCursor(200, 0)?.toString().orEmpty()
                if (txt.isNotEmpty()) currentInputConnection?.deleteSurroundingText(txt.length, 0)
                refreshLivePreview()
                ZarmaImageRenderer.shareTextAsImage(this@ZarmaIMEService, txt, zarmaFont, theme)
            }
        }
        previewBar.addView(livePreviewTv); previewBar.addView(sendImgBtn)
        rootLayout.addView(previewBar)
        rootLayout.addView(suggestionRow); updateSuggestions(); refreshLivePreview()"""
ime = ime.replace(old_sug, new_sug)
ime = ime.replace("currentInputConnection?.deleteSurroundingText(1, 0); updateSuggestions()", "currentInputConnection?.deleteSurroundingText(1, 0); updateSuggestions(); refreshLivePreview()")

with open(ime_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(ime)
print("[OK] Code Android & Windows migré vers v2.1 (U+E800 + Aperçu Zarma en direct).")
