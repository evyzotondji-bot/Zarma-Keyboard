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
