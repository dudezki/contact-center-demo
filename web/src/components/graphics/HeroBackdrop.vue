<script setup lang="ts">
// Cinematic night-office backdrop drawn in SVG (soft window bokeh, a light shaft, film grain).
// Drop a licensed photograph at /public/images/hero.jpg and it is layered on top automatically.
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { gsap } from '@/composables/useMotion'
const root = ref<HTMLElement>()
let mm: gsap.MatchMedia | undefined
const hasPhoto = ref(true)
const photo = "/images/hero.jpg" // optional, resolved at runtime
const bokeh = Array.from({ length: 26 }, (_, i) => {
  const r = (n: number) => { const x = Math.sin(i * 91.7 + n * 13.3) * 10000; return x - Math.floor(x) }
  return { x: 8 + r(1) * 92, y: 10 + r(2) * 58, r: 14 + r(3) * 46, o: 0.12 + r(4) * 0.34, warm: r(5) > 0.35 }
})

onMounted(() => {
  mm = gsap.matchMedia()
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    const el = root.value!
    // Bokeh: each light drifts on its own path and tempo and breathes in brightness.
    el.querySelectorAll<SVGElement>('[data-bokeh]').forEach((c, i) => {
      const r = (n: number) => { const x = Math.sin(i * 57.3 + n * 9.1) * 10000; return x - Math.floor(x) }
      gsap.to(c, { x: (r(1) - 0.5) * 22, y: (r(2) - 0.5) * 14, duration: 8 + r(3) * 8, ease: 'sine.inOut', repeat: -1, yoyo: true, delay: -r(4) * 8 })
      gsap.to(c, { opacity: Number(c.dataset.bokeh) * (0.35 + r(5) * 0.4), duration: 3 + r(6) * 4, ease: 'sine.inOut', repeat: -1, yoyo: true, delay: -r(7) * 5 })
    })
    gsap.to('[data-glow]', { opacity: 0.65, scale: 1.08, transformOrigin: '68% 38%', duration: 6, ease: 'sine.inOut', repeat: -1, yoyo: true })
    gsap.to('[data-shaft]', { x: 4, rotation: 1.5, transformOrigin: '50% 0%', opacity: 0.6, duration: 9, ease: 'sine.inOut', repeat: -1, yoyo: true })
    // Pointer parallax: far layer and photo move at different depths.
    const far = gsap.quickTo('[data-hero-layer="far"]', 'x', { duration: 1.2, ease: 'power3.out' })
    const farY = gsap.quickTo('[data-hero-layer="far"]', 'y', { duration: 1.2, ease: 'power3.out' })
    const move = (e: PointerEvent) => {
      far((e.clientX / innerWidth - 0.5) * -18); farY((e.clientY / innerHeight - 0.5) * -12)
    }
    window.addEventListener('pointermove', move, { passive: true })
    return () => window.removeEventListener('pointermove', move)
  })
})
onBeforeUnmount(() => mm?.revert())
</script>

<template>
  <div ref="root" class="absolute inset-0 overflow-hidden bg-ink" aria-hidden="true">
    <svg class="absolute -inset-[3%] size-[106%] max-w-none" viewBox="0 0 100 60" preserveAspectRatio="xMidYMid slice" data-hero-layer="far">
      <defs>
        <radialGradient id="glow" cx="68%" cy="38%" r="55%">
          <stop offset="0" stop-color="#e8a24a" stop-opacity="0.38" /><stop offset="1" stop-color="#e8a24a" stop-opacity="0" />
        </radialGradient>
        <linearGradient id="shaft" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#f1ece3" stop-opacity="0.16" /><stop offset="1" stop-color="#f1ece3" stop-opacity="0" />
        </linearGradient>
        <radialGradient id="bk-warm"><stop offset="0" stop-color="#e8a24a" stop-opacity="0.9" /><stop offset="0.55" stop-color="#e8a24a" stop-opacity="0.5" /><stop offset="1" stop-color="#e8a24a" stop-opacity="0" /></radialGradient>
        <radialGradient id="bk-cool"><stop offset="0" stop-color="#9fb4c7" stop-opacity="0.9" /><stop offset="0.55" stop-color="#9fb4c7" stop-opacity="0.5" /><stop offset="1" stop-color="#9fb4c7" stop-opacity="0" /></radialGradient>
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" /><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.5 0" /></filter>
      </defs>
      <rect data-glow width="100" height="60" fill="url(#glow)" />
      <circle v-for="(b, i) in bokeh" :key="i" :data-bokeh="b.o" :cx="b.x" :cy="b.y" :r="b.r / 7" :fill="b.warm ? 'url(#bk-warm)' : 'url(#bk-cool)'" :opacity="b.o" />
      <polygon data-shaft points="58,0 82,0 46,60 12,60" fill="url(#shaft)" />
    </svg>
    <img
      v-if="hasPhoto" :src="photo" alt="" class="absolute inset-0 size-full object-cover opacity-70"
      data-hero-layer="photo" @error="hasPhoto = false"
    />
    <!-- Legibility: left-weighted scrim + floor fade. -->
    <div class="absolute inset-0 bg-gradient-to-r from-ink/55 via-ink/15 to-transparent" />
    <div class="absolute inset-x-0 bottom-0 h-1/5 bg-gradient-to-t from-ink/70 to-transparent" />
    <svg class="absolute inset-0 size-full opacity-[0.07] mix-blend-screen"><rect width="100%" height="100%" filter="url(#grain)" /></svg>
  </div>
</template>
