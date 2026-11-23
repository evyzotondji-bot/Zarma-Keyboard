package com.zedempires.zarmakeyboard
import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.provider.Settings
import android.view.inputmethod.InputMethodManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.SwitchCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf")
        val scroll = ScrollView(this); val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(40, 48, 40, 48) }
        root.addView(TextView(this).apply { text = "Clavier Zarma Pro v2.0 (ELDAS)"; textSize = 22f; setTypeface(null, Typeface.BOLD) })
        root.addView(Button(this).apply { text = "1. Activer dans Paramètres Android"; setOnClickListener { startActivity(Intent(Settings.ACTION_INPUT_METHOD_SETTINGS)) } })
        root.addView(Button(this).apply { text = "2. Sélectionner Clavier Zarma Pro"; setOnClickListener { (getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager).showInputMethodPicker() } })
        val testBox = EditText(this).apply { hint = "Tapez ici en Zarma..."; typeface = zarmaFont; textSize = 26f; minLines = 2 }
        root.addView(testBox)
        root.addView(Button(this).apply { text = "Partager en Image HD (WhatsApp / TikTok)"; setOnClickListener { ZarmaImageRenderer.shareTextAsImage(this@MainActivity, testBox.text.toString(), zarmaFont, ThemeManager.getCurrentTheme(this@MainActivity)) } })
        root.addView(TextView(this).apply { text = "\nThèmes Couleurs :"; textSize = 17f; setTypeface(null, Typeface.BOLD) })
        for (t in ThemeManager.PRESETS) {
            root.addView(Button(this).apply { text = "Appliquer : ${t.name}"; setBackgroundColor(t.bgColor); setTextColor(t.textColor); setOnClickListener { ThemeManager.setThemeId(this@MainActivity, t.id); Toast.makeText(this@MainActivity, "Thème ${t.name}", Toast.LENGTH_SHORT).show() } })
        }
        root.addView(TextView(this).apply { text = "\nCouleurs Personnalisées (#RRGGBB) :"; textSize = 17f; setTypeface(null, Typeface.BOLD) })
        val edBg = EditText(this).apply { setText("#1B5E20") }; val edKey = EditText(this).apply { setText("#2E7D32") }
        val edAct = EditText(this).apply { setText("#F9A825") }; val edTxt = EditText(this).apply { setText("#FFFFFF") }
        root.addView(edBg); root.addView(edKey); root.addView(edAct); root.addView(edTxt)
        root.addView(Button(this).apply { text = "Enregistrer couleurs personnalisées"; setOnClickListener { val ok = ThemeManager.saveCustomColors(this@MainActivity, edBg.text.toString(), edKey.text.toString(), edAct.text.toString(), edTxt.text.toString()); Toast.makeText(this@MainActivity, if (ok) "Enregistré !" else "Format #RRGGBB invalide", Toast.LENGTH_SHORT).show() } })
        root.addView(TextView(this).apply { text = "\nConfort :"; textSize = 17f; setTypeface(null, Typeface.BOLD) })
        root.addView(SwitchCompat(this).apply { text = "Vibration"; isChecked = ThemeManager.isHapticEnabled(this@MainActivity); setOnCheckedChangeListener { _, v -> ThemeManager.setHapticEnabled(this@MainActivity, v) } })
        root.addView(SwitchCompat(this).apply { text = "Bulles d'aperçu Gboard"; isChecked = ThemeManager.isPopupEnabled(this@MainActivity); setOnCheckedChangeListener { _, v -> ThemeManager.setPopupEnabled(this@MainActivity, v) } })
        root.addView(SwitchCompat(this).apply { text = "Son des touches"; isChecked = ThemeManager.isSoundEnabled(this@MainActivity); setOnCheckedChangeListener { _, v -> ThemeManager.setSoundEnabled(this@MainActivity, v) } })
        val hRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        for ((lbl, hVal) in listOf("Compact" to 44, "Normal" to 50, "Grand" to 58)) { hRow.addView(Button(this).apply { text = lbl; setOnClickListener { ThemeManager.setKeyHeightDp(this@MainActivity, hVal); Toast.makeText(this@MainActivity, "Hauteur : $lbl", Toast.LENGTH_SHORT).show() } }) }
        root.addView(hRow); scroll.addView(root); setContentView(scroll)
    }
}
