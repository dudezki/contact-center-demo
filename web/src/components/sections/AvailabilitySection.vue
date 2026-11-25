<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useSectionMotion } from '@/composables/useMotion'
const root = ref<HTMLElement>()
useSectionMotion(() => root.value)
const hour = ref(0)
onMounted(() => { hour.value = new Date().getHours() + new Date().getMinutes() / 60 })
const pos = computed(() => `${(hour.value / 24) * 100}%`)
</script>

<template>
  <section ref="root" class="border-t border-line py-28 sm:py-36">
    <div class="container-x grid gap-12 lg:grid-cols-2 lg:items-end">
      <div>
        <p class="eyebrow" data-reveal>Service availability</p>
        <h2 class="display mt-5 text-5xl sm:text-7xl" data-reveal="0.1">Open every hour.<br /><span class="italic text-signal">Including this one.</span></h2>
      </div>
      <div data-reveal>
        <p class="mb-6 max-w-sm text-paper-dim">The voice agent answers around the clock. Human specialists join for complex cases during staffed hours.</p>
        <div class="relative h-14" role="img" aria-label="24-hour availability: the AI agent is available all day; your local time is marked">
          <div class="absolute inset-x-0 top-6 h-px bg-line" />
          <div class="absolute inset-x-0 top-5 flex justify-between" aria-hidden="true">
            <span v-for="h in 25" :key="h" class="w-px bg-paper/25" :class="(h - 1) % 6 === 0 ? 'h-4' : 'h-2'" />
          </div>
          <div class="absolute inset-x-0 top-1 h-2 rounded-full bg-signal/80" aria-hidden="true" />
          <span class="absolute top-0 -ml-px h-14 w-0.5 bg-paper" :style="{ left: pos }" aria-hidden="true" />
        </div>
        <div class="mt-1 flex justify-between font-mono text-xs text-mute" aria-hidden="true"><span>00</span><span>06</span><span>12</span><span>18</span><span>24</span></div>
      </div>
    </div>
  </section>
</template>
