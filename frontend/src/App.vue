<template>
  <div id="app">
    <Header />
    <main>
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { provide } from 'vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useLanguage } from './composables/useLanguage'

// Инициализируем язык
const { currentLang, setLanguage, t } = useLanguage()

// Провайдим глобально для всех компонентов
provide('currentLang', currentLang)
provide('setLanguage', setLanguage)
provide('t', t)
</script>

<style>
/* --- ГЛОБАЛЬНЫЙ СБРОС --- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

main {
  flex: 1;
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}
</style>