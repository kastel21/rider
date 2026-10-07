package com.operations.rider

import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.view.View
import android.view.animation.DecelerateInterpolator
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

/**
 * Lab Pulse startup screen. Rings and the vial play while the local server starts,
 * then the landing screen opens.
 */
class SplashActivity : AppCompatActivity() {

    private val ui = Handler(Looper.getMainLooper())
    private val animators = mutableListOf<android.animation.Animator>()
    private var opened = false
    private var startedAt = 0L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        startedAt = SystemClock.uptimeMillis()

        val mark = findViewById<SplashMarkView>(R.id.splash_mark)
        val wordmark = findViewById<TextView>(R.id.splash_wordmark)
        val starting = findViewById<TextView>(R.id.splash_starting)
        val version = findViewById<TextView>(R.id.splash_version)
        version.text = BuildConfig.VERSION_NAME.substringBefore('-')

        pulseRing(findViewById(R.id.splash_ring_1), 0L)
        pulseRing(findViewById(R.id.splash_ring_2), 800L)
        pulseRing(findViewById(R.id.splash_ring_3), 1600L)
        revealMark(mark)
        fillVial(mark)
        revealWordmark(wordmark)
        blinkStarting(starting)
        revealVersion(version)

        Thread {
            try {
                OpsEmbeddedServer.ensureStarted(applicationContext)
            } catch (_: Exception) {
                // LandingActivity surfaces the startup failure.
            }
            val elapsed = SystemClock.uptimeMillis() - startedAt
            val wait = (MIN_SPLASH_MS - elapsed).coerceAtLeast(0L)
            ui.postDelayed({ openLanding() }, wait)
        }.start()
    }

    override fun onDestroy() {
        ui.removeCallbacksAndMessages(null)
        animators.forEach { it.cancel() }
        animators.clear()
        super.onDestroy()
    }

    private fun pulseRing(ring: View, delayMs: Long) {
        ring.scaleX = 0.35f
        ring.scaleY = 0.35f
        val scaleX = ObjectAnimator.ofFloat(ring, View.SCALE_X, 0.35f, 1.18f)
        val scaleY = ObjectAnimator.ofFloat(ring, View.SCALE_Y, 0.35f, 1.18f)
        val alpha = ObjectAnimator.ofFloat(ring, View.ALPHA, 0.9f, 0f)
        listOf(scaleX, scaleY, alpha).forEach { animator ->
            animator.duration = RING_MS
            animator.startDelay = delayMs
            animator.repeatCount = ValueAnimator.INFINITE
            animator.interpolator = DecelerateInterpolator()
            animators += animator
            animator.start()
        }
    }

    private fun revealMark(mark: SplashMarkView) {
        mark.scaleX = 0.8f
        mark.scaleY = 0.8f
        mark.animate().alpha(1f).scaleX(1f).scaleY(1f).setDuration(520L).start()
    }

    private fun fillVial(mark: SplashMarkView) {
        val fill = ValueAnimator.ofFloat(0.28f, 1f, 0.28f).apply {
            duration = RING_MS
            repeatCount = ValueAnimator.INFINITE
            addUpdateListener { mark.fillLevel = it.animatedValue as Float }
        }
        animators += fill
        fill.start()
    }

    private fun revealWordmark(wordmark: TextView) {
        wordmark.translationY = 10f * resources.displayMetrics.density
        wordmark.animate().alpha(1f).translationY(0f).setStartDelay(180L).setDuration(620L).start()
    }

    private fun blinkStarting(starting: TextView) {
        val blink = ObjectAnimator.ofFloat(starting, View.ALPHA, 0.2f, 1f).apply {
            duration = 700L
            startDelay = 420L
            repeatMode = ValueAnimator.REVERSE
            repeatCount = ValueAnimator.INFINITE
        }
        animators += blink
        blink.start()
    }

    private fun revealVersion(version: TextView) {
        version.animate().alpha(1f).setStartDelay(400L).setDuration(500L).start()
    }

    private fun openLanding() {
        if (opened || isFinishing || isDestroyed) return
        opened = true
        startActivity(Intent(this, LandingActivity::class.java))
        finish()
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out)
    }

    companion object {
        private const val MIN_SPLASH_MS = 2600L
        private const val RING_MS = 2400L
    }
}
