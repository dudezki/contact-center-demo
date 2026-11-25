<script setup lang="ts">
import { ref } from 'vue'
import { useSectionMotion } from '@/composables/useMotion'
const root = ref<HTMLElement>()
useSectionMotion(() => root.value)
</script>

<template>
  <section id="about" ref="root" class="relative overflow-hidden border-y border-line bg-ink-2 py-28 sm:py-40">
    <!-- Concentric signal rings: a quiet echo of a sound wave leaving a speaker. -->
    <svg class="pointer-events-none absolute -right-40 top-1/2 size-[56rem] -translate-y-1/2 text-signal/25" viewBox="0 0 400 400" fill="none" stroke="currentColor" aria-hidden="true" data-parallax="0.12">
      <circle v-for="r in 8" :key="r" cx="200" cy="200" :r="r * 24" :stroke-width="r % 3 === 0 ? 1 : 0.5" :stroke-dasharray="r % 2 ? '2 6' : 'none'" />
    </svg>
    <div class="container-x relative">
      <p class="eyebrow" data-reveal>AI-powered customer experience</p>
      <p class="display mt-6 max-w-[20ch] text-4xl sm:text-6xl lg:text-7xl" data-reveal="0.1">
        Speed matters. <span class="text-paper-dim">So does being</span> <span class="italic text-signal">understood.</span>
      </p>
      <div class="mt-16 grid max-w-3xl gap-10 text-paper-dim sm:grid-cols-2">
        <p data-reveal>The agent responds in a natural voice, handles interruptions the way a person would, and keeps answers short enough to be useful.</p>
        <p data-reveal="0.1">It is tuned to sound like a trained representative: professional, friendly and concise — and it says plainly when it needs to hand you to a human.</p>
      </div>
    </div>
  </section>
</template>
