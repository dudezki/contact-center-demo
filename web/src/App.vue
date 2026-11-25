<script setup lang="ts">
import { useSmoothScroll } from '@/composables/useMotion'
import SiteNav from '@/components/layout/SiteNav.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'
import HeroSection from '@/components/sections/HeroSection.vue'
import SolutionsSection from '@/components/sections/SolutionsSection.vue'
import ExperienceSection from '@/components/sections/ExperienceSection.vue'
import HowItWorksSection from '@/components/sections/HowItWorksSection.vue'
import AvailabilitySection from '@/components/sections/AvailabilitySection.vue'
import ContactSection from '@/components/sections/ContactSection.vue'
import CallDock from '@/components/voice/CallDock.vue'

useSmoothScroll()
</script>

<template>
  <SiteNav />
  <main id="main" tabindex="-1" class="outline-none">
    <HeroSection /><SolutionsSection /><ExperienceSection /><HowItWorksSection /><AvailabilitySection /><ContactSection />
  </main>
  <SiteFooter />
  <CallDock />
</template>
