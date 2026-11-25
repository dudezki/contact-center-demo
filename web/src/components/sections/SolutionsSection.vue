<script setup lang="ts">
import { ref } from 'vue'
import { AudioLines, BarChart3, GitBranch, Languages, ShieldCheck, UsersRound } from 'lucide-vue-next'
import { useSectionMotion } from '@/composables/useMotion'

const root = ref<HTMLElement>()
useSectionMotion(() => root.value)

// Capabilities describe the product direction; only live voice is wired in this MVP.
const items = [
  { icon: AudioLines, t: 'Voice, in the browser', d: 'Natural two-way conversation over WebRTC. No dial-in, no app, no hold music.' },
  { icon: GitBranch, t: 'Intelligent routing', d: 'Understand intent in the first sentence and send each caller to the right outcome.' },
  { icon: Languages, t: 'Multilingual by design', d: 'Speech and language models that can follow callers across languages.' },
  { icon: UsersRound, t: 'Human handoff', d: 'Escalate to a person with the full context, so nobody repeats themselves.' },
  { icon: BarChart3, t: 'Conversation insight', d: 'Transcripts and trends that show what customers actually ask for.' },
  { icon: ShieldCheck, t: 'Private by default', d: 'Short-lived sessions, server-side secrets, and isolated rooms per call.' },
]
</script>

<template>
  <section id="solutions" ref="root" class="container-x py-28 sm:py-40">
    <div class="grid gap-14 lg:grid-cols-[1fr_1.5fr] lg:gap-24">
      <div class="lg:sticky lg:top-32 lg:self-start">
        <p class="eyebrow" data-reveal>Capabilities</p>
        <h2 class="display mt-5 text-5xl sm:text-7xl" data-reveal="0.1">A contact center that actually listens.</h2>
      </div>
      <ol class="divide-y divide-line border-y border-line">
        <li v-for="(it, i) in items" :key="it.t" class="group grid grid-cols-[3rem_1fr] gap-4 py-8 sm:grid-cols-[4rem_1fr_auto]" data-reveal>
          <span class="font-mono text-sm text-mute">{{ String(i + 1).padStart(2, '0') }}</span>
          <div>
            <h3 class="display text-3xl transition-colors group-hover:text-signal sm:text-4xl">{{ it.t }}</h3>
            <p class="mt-2 max-w-md text-paper-dim">{{ it.d }}</p>
          </div>
          <component :is="it.icon" :size="26" class="hidden text-mute transition-colors group-hover:text-signal sm:block" aria-hidden="true" />
        </li>
      </ol>
    </div>
  </section>
</template>
