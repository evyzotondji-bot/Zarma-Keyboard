package com.zedempires.zarmakeyboard
import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.provider.Settings
import android.view.inputmethod.InputMethodManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf")
        val layout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(48, 64, 48, 48) }
        layout.addView(TextView(this).apply { text = "Clavier Zarma Officiel (ELDAS)"; textSize = 22f })
        layout.addView(Button(this).apply { text = "1. Activer le Clavier Zarma"; setOnClickListener { startActivity(Intent(Settings.ACTION_INPUT_METHOD_SETTINGS)) } })
        layout.addView(Button(this).apply { text = "2. Choisir Clavier Zarma"; setOnClickListener { (getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager).showInputMethodPicker() } })
        layout.addView(Button(this).apply {
            text = "3. Couleur : ${ThemeManager.getCurrentTheme(this@MainActivity).name}"
            setOnClickListener { text = "3. Couleur : ${ThemeManager.nextTheme(this@MainActivity).name}" }
        })
        layout.addView(EditText(this).apply { hint = "Testez l'écriture Zarma ici..."; typeface = zarmaFont; textSize = 26f; minLines = 3 })
        setContentView(layout)
    }
}
