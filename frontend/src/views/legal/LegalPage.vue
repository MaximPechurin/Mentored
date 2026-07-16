<template>
  <div class="legal-page">
    <LegalHero />
    <LegalTabs v-model="activeTab" />
    <LegalContent :tab="activeTab" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LegalHero from './LegalHero.vue'
import LegalTabs from './LegalTabs.vue'
import LegalContent from './LegalContent.vue'

const activeTab = ref('info')
</script>

<style scoped>
.legal-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}
</style>