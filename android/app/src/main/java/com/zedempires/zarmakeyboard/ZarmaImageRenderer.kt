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
