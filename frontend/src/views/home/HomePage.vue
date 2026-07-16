<template>
  <div class="home-page">
    <HeroSection />
    <QuoteBand />
    <FeelingsSection :feelings="feelings" />
    <PillarsSection />
    <CycleSection :cycle="cycle" />
    <FounderSection :bullets="founderBullets" />
    <TestCtaSection />
    <TestimonialsSection :testimonials="testimonials" />
    <FinalCtaSection />
  </div>
</template>

<script setup>
import HeroSection from './HeroSection.vue'
import QuoteBand from './QuoteBand.vue'
import FeelingsSection from './FeelingsSection.vue'
import PillarsSection from './PillarsSection.vue'
import CycleSection from './CycleSection.vue'
import FounderSection from './FounderSection.vue'
import TestCtaSection from './TestCtaSection.vue'
import TestimonialsSection from './TestimonialsSection.vue'
import FinalCtaSection from './FinalCtaSection.vue'

import { useHomeData } from '../../data/homeData.js'

const { feelings, cycle, founderBullets, testimonials } = useHomeData()
</script>

<style scoped>
.home-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}
</style>