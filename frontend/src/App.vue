<template>
  <div id="app" :class="{ 'app--escuela': isEscuela }">
    <!-- Раздел /escuela/* - отдельная "учебная платформа" со своей
         тёмной шапкой и без маркетингового Header/Footer, чтобы визуально
         отличаться от витрины магазина. -->
    <EscuelaNav v-if="isEscuela" />
    <Header v-else />
    <main>
      <router-view />
    </main>
    <Footer v-if="!isEscuela" />
    <!-- Чат преподаватель↔ученик - только внутри учебной платформы -->
    <ChatWidget v-if="isEscuela && isAuthenticated" />
  </div>
</template>

<script setup>
import { provide, computed } from 'vue'
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import EscuelaNav from './components/EscuelaNav.vue'
import ChatWidget from './components/ChatWidget.vue'
import { useLanguage } from './composables/useLanguage'
import { useAuth } from './composables/useAuth'

const route = useRoute()
const isEscuela = computed(() => route.path.startsWith('/escuela'))
const { isAuthenticated } = useAuth()

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