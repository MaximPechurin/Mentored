<template>
  <div class="compras-page">
    <ComprasHero />
    <ComprasSteps />
    <ComprasContent />
  </div>
</template>

<script setup>
import ComprasHero from './ComprasHero.vue'
import ComprasSteps from './ComprasSteps.vue'
import ComprasContent from './ComprasContent.vue'
</script>

<style scoped>
.compras-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}
</style>