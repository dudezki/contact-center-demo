<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { ArrowDown, Mic } from 'lucide-vue-next'
import { gsap } from '@/composables/useMotion'
import { useCallStore } from '@/stores/call'
import Button from '@/components/ui/Button.vue'
import HeroBackdrop from '@/components/graphics/HeroBackdrop.vue'
import Waveform from '@/components/voice/Waveform.vue'

const call = useCallStore()
const root = ref<HTMLElement>()
let mm: gsap.MatchMedia | undefined

onMounted(() => {
  mm = gsap.matchMedia()
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    gsap.from('[data-line] > span', { yPercent: 110, duration: 1.3, ease: 'expo.out', stagger: 0.14, delay: 0.15 })
    gsap.from('[data-hero-in]', { opacity: 0, y: 24, duration: 1, ease: 'power3.out', stagger: 0.12, delay: 0.75 })
    // Parallax: backdrop drifts slower than the page, content lifts and fades.
    gsap.to('[data-hero-bg]', { yPercent: 18, scale: 1.08, ease: 'none', scrollTrigger: { trigger: root.value, start: 'top top', end: 'bottom top', scrub: true } })
    gsap.to('[data-hero-copy]', { yPercent: -12, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: root.value, start: 'top top', end: 'bottom 20%', scrub: true } })
  })
})
onBeforeUnmount(() => mm?.revert())
</script>

<template>
  <section id="home" ref="root" class="relative flex min-h-svh items-end overflow-hidden pb-16 pt-32 sm:items-center sm:pb-0">
    <div data-hero-bg class="absolute inset-0 will-change-transform"><HeroBackdrop /></div>
    <div data-hero-copy class="container-x relative">
      <p class="eyebrow mb-8" data-hero-in>AI-powered contact center</p>
      <h1 class="display max-w-[14ch] text-[clamp(3.4rem,10vw,9rem)]">
        <span class="block overflow-hidden pb-[0.08em]" data-line><span class="block">Every conversation.</span></span>
        <span class="block overflow-hidden pb-[0.12em]" data-line><span class="block italic text-signal">A real connection.</span></span>
      </h1>
      <p class="mt-8 max-w-md text-lg text-paper-dim" data-hero-in>
        Intelligent conversations. Instant support. Always here when you need us.
      </p>
      <div class="mt-10 flex flex-wrap items-center gap-6" data-hero-in>
        <Button size="lg" :class="call.active ? 'group' : 'group cta-pulse'" :disabled="call.active" @click="call.start()">
          <Mic :size="20" aria-hidden="true" />Start a conversation
        </Button>
        <div class="flex items-center gap-3 text-sm text-mute">
          <span class="h-8 w-24" aria-hidden="true"><Waveform source="agent" :bars="14" :active="false" /></span>
          <span>
            <span class="flex items-center gap-2 text-paper-dim">
              <span class="relative flex size-2" aria-hidden="true"><span class="absolute inset-0 animate-ping rounded-full bg-ok/70" /><span class="relative size-2 rounded-full bg-ok" /></span>
              Agent online now
            </span>
            <span class="block">Voice call in your browser — no download</span>
          </span>
        </div>
      </div>
    </div>
    <a href="#solutions" class="absolute bottom-6 left-1/2 hidden size-11 -translate-x-1/2 place-items-center text-mute hover:text-paper sm:grid" aria-label="Scroll to solutions">
      <ArrowDown :size="20" />
    </a>
  </section>
</template>
