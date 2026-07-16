<template>
  <div class="consultas-page">
    <ConsultasHero />
    <ConsultasCategories />
    <ConsultasFeatured />
    <ConsultasHowItWorks />
    <ConsultasResults />
    <ConsultasCta />
  </div>
</template>

<script setup>
import ConsultasHero from './ConsultasHero.vue'
import ConsultasCategories from './ConsultasCategories.vue'
import ConsultasFeatured from './ConsultasFeatured.vue'
import ConsultasHowItWorks from './ConsultasHowItWorks.vue'
import ConsultasResults from './ConsultasResults.vue'
import ConsultasCta from './ConsultasCta.vue'
</script>

<style scoped>
.consultas-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}
</style>