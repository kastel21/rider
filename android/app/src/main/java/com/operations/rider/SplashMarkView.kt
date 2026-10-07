package com.operations.rider

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View

/** Hexagon and specimen vial used on the startup splash. [fillLevel] is 0..1. */
class SplashMarkView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
) : View(context, attrs) {

    var fillLevel: Float = 0.3f
        set(value) {
            field = value.coerceIn(0f, 1f)
            invalidate()
        }

    private val hexPath = Path()
    private val vialRect = RectF()
    private val fillRect = RectF()
    private var laidOutW = -1
    private var laidOutH = -1
    private var unit = 1f

    private val hexPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        color = Color.WHITE
        strokeJoin = Paint.Join.ROUND
    }
    private val vialPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        color = Color.parseColor("#38BDF8")
    }
    private val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
        color = Color.parseColor("#38BDF8")
    }
    private val capPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        color = Color.WHITE
        strokeCap = Paint.Cap.ROUND
    }

    override fun onDraw(canvas: Canvas) {
        val w = width
        val h = height
        if (w <= 0 || h <= 0) return
        ensureGeometry(w, h)

        canvas.drawPath(hexPath, hexPaint)

        val radius = 5f * unit
        canvas.save()
        canvas.clipPath(Path().apply { addRoundRect(vialRect, radius, radius, Path.Direction.CW) })
        canvas.drawRoundRect(fillRect, 1.5f * unit, 1.5f * unit, fillPaint)
        canvas.restore()

        canvas.drawRoundRect(vialRect, radius, radius, vialPaint)
        canvas.drawLine(31f * unit, 22f * unit, 41f * unit, 22f * unit, capPaint)
    }

    private fun ensureGeometry(w: Int, h: Int) {
        if (w == laidOutW && h == laidOutH) {
            updateFill()
            return
        }
        laidOutW = w
        laidOutH = h
        unit = w / 72f
        hexPaint.strokeWidth = 1.6f * unit
        vialPaint.strokeWidth = 1.8f * unit
        capPaint.strokeWidth = 1.8f * unit

        hexPath.reset()
        hexPath.moveTo(36f * unit, 6f * unit)
        hexPath.lineTo(62f * unit, 20f * unit)
        hexPath.lineTo(62f * unit, 50f * unit)
        hexPath.lineTo(36f * unit, 66f * unit)
        hexPath.lineTo(10f * unit, 50f * unit)
        hexPath.lineTo(10f * unit, 20f * unit)
        hexPath.close()

        vialRect.set(31f * unit, 24f * unit, 41f * unit, 50f * unit)
        updateFill()
    }

    private fun updateFill() {
        val left = 33.2f * unit
        val right = 38.8f * unit
        val top = 28f * unit
        val bottom = 48f * unit
        val fillTop = bottom - (bottom - top) * fillLevel
        fillRect.set(left, fillTop, right, bottom)
    }
}
