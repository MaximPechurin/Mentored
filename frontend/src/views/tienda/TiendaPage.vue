<template>
  <div class="tienda-page">
    <TiendaHero />
    <TiendaFilters v-model="activeFilter" />
    <TiendaGrid :filter="activeFilter" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TiendaHero from './TiendaHero.vue'
import TiendaFilters from './TiendaFilters.vue'
import TiendaGrid from './TiendaGrid.vue'

const activeFilter = ref('todos')
</script>

<style scoped>
.tienda-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f5eee3;
}
</style>