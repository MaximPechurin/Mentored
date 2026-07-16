<template>
  <div class="contacto-page">
    <ContactoHero />
    <ContactoForm />
    <ContactoFaq />
  </div>
</template>

<script setup>
import ContactoHero from './ContactoHero.vue'
import ContactoForm from './ContactoForm.vue'
import ContactoFaq from './ContactoFaq.vue'
</script>

<style scoped>
.contacto-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f5eee3;
}
</style>