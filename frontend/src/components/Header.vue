<template>
  <header class="header">
    <div class="header-inner">
      <!-- Логотип -->
      <router-link to="/" class="logo">
        <img src="/images/logo.png" alt="Mentored">
      </router-link>

      <!-- Навигация -->
      <nav class="nav">
        <!-- <router-link to="/cursos">Cursos</router-link> -->
        <router-link to="/consultas">Consultas</router-link>
        <!-- <router-link to="/expertos">Expertos</router-link> -->
        <router-link to="/tienda">Tienda</router-link>
        <!-- <router-link to="/comunidad">Comunidad</router-link> -->
        <!-- <router-link to="/gratis">Gratis</router-link> -->
        <router-link to="/blog">Blog</router-link>
        <router-link to="/contacto">Contacto</router-link>
      </nav>

      <!-- Действия -->
      <div class="actions">
        <!-- Заметная кнопка входа в учебную платформу. Видна только тем,
             у кого есть доступ к школе (is_dev + роль student/teacher).
             Ведёт в панель препода, если он преподаватель, иначе - в
             кабинет студента. -->
        <router-link v-if="hasSchool" :to="schoolHome" class="btn-escuela">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m2 7 10-5 10 5-10 5z"/><path d="M6 9.5V15c0 1.5 2.7 3 6 3s6-1.5 6-3V9.5"/>
          </svg>
          Ir a la Escuela
        </router-link>

        <div class="cta-buttons">
          <!--<a href="#" class="btn-test">{{ t('nav.test') }}</a> МБ ВЕРНУТЬ В ДАЛЬНЕЙШЕМ -->
          <a href="https://wa.me/51940304595" class="btn-whatsapp">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
            WhatsApp
          </a>
        </div>

        <!-- ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА -->
        <div class="language-switcher">
          <button
            class="lang-btn"
            :class="{ active: currentLang === 'es' }"
            @click="setLanguage('es')"
            aria-label="Español"
          >ES</button>
          <span class="lang-divider">|</span>
        </div>

        <router-link to="/carrito" class="icon-btn" aria-label="Carrito">
          <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="9" cy="21" r="1"/>
            <circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
          </svg>
        </router-link>
        <router-link to="/cuenta" class="icon-btn" aria-label="Cuenta">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </router-link>
        <button class="burger" aria-label="Menú">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguage } from '../composables/useLanguage.js'
import { useAuth } from '../composables/useAuth.js'

const { currentLang, setLanguage, t } = useLanguage()

// user - это снэпшот из localStorage (см. useAuth.loadUser) - может быть
// устаревшим, если роль назначили после последнего логина/refreshUser().
// Для хедера это ок (просто пункт меню появится чуть позже, после
// обновления профиля на любой другой странице) - здесь сознательно не
// дёргаем API при каждой отрисовке хедера.
const { user } = useAuth()
const isDev = computed(() => !!user.value?.is_dev)
const isStudent = computed(() => !!user.value?.roles?.includes('student'))
const isTeacher = computed(() => !!user.value?.roles?.includes('teacher'))
// Доступ к школе: dev-аккаунт с ролью студента или преподавателя
const hasSchool = computed(() => isDev.value && (isStudent.value || isTeacher.value))
const schoolHome = computed(() => (isTeacher.value ? '/escuela/profesor' : '/escuela/estudiante'))
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #ffffff;
  border-bottom: 1px solid #ececec;
  width: 100%;
}

.header-inner {
  max-width: 1480px;
  margin: 0 auto;
  height: 84px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 11px;
  text-decoration: none;
  flex-shrink: 0;
  color: #fc0100;
}

.logo img {
  display: block;
  flex-shrink: 0;
  height: 38px;
  width: auto;
}

.nav {
  display: flex;
  align-items: center;
  gap: 30px;
  flex: 1;
  justify-content: center;
}

.nav a {
  text-decoration: none;
  font-size: 16.5px;
  font-weight: 400;
  color: #1c1c1c;
  white-space: nowrap;
  letter-spacing: -0.1px;
  transition: color 0.3s;
}

/* БЛОК ДЛЯ ПОДСВЕТКИ АКТИВНОЙ СТРАНИЦЫ */
.nav a:hover {
  color: #8e1519;
}

/* Активная страница — красный цвет */
.nav a.router-link-active {
  color: #8e1519;
  font-weight: 600;
}

.nav a.router-link-exact-active {
  color: #8e1519;
  font-weight: 600;
}

.actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.cta-buttons {
  display: flex;
  align-items: center;
  gap: 14px;
}

.btn-test {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  border: 1.5px solid #8e1519;
  color: #8e1519;
  font-weight: 600;
  font-size: 15.5px;
  padding: 11px 22px;
  border-radius: 999px;
  white-space: nowrap;
  transition: all 0.3s;
}

.btn-test:hover {
  background: #8e1519;
  color: #fff;
}

.btn-escuela {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  background: #0e0c0c;
  color: #fff;
  font-weight: 600;
  font-size: 15.5px;
  padding: 12px 20px;
  border-radius: 999px;
  white-space: nowrap;
  border: 1.5px solid #c49a3f;
  transition: all 0.3s;
}

.btn-escuela svg { color: #c49a3f; }

.btn-escuela:hover {
  background: #c49a3f;
  border-color: #c49a3f;
}

.btn-escuela:hover svg { color: #0e0c0c; }

.btn-whatsapp {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 15.5px;
  padding: 12px 22px;
  border-radius: 999px;
  white-space: nowrap;
  transition: background 0.3s;
}

.btn-whatsapp:hover {
  background: #a01a1f;
}

/* --- ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА --- */
.language-switcher {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #1c1c1c;
  padding: 0 8px;
  border-left: 1px solid #ececec;
  padding-left: 14px;
}

.lang-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #999;
  padding: 4px 6px;
  transition: color 0.3s, font-weight 0.3s;
  font-family: inherit;
  text-transform: uppercase;
}

.lang-btn:hover {
  color: #666;
}

.lang-btn.active {
  color: #8e1519;
  font-weight: 700;
}

.lang-divider {
  color: #ddd;
  font-weight: 300;
}

.icon-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  color: #1a1a1a;
  text-decoration: none;
  transition: color 0.3s;
}

.icon-btn:hover {
  color: #8e1519;
}

.burger {
  display: none;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border: none;
  background: none;
  cursor: pointer;
  color: #1a1a1a;
  padding: 0;
}

@media (max-width: 980px) {
  .nav { display: none !important; }
  .cta-buttons { display: none !important; }
  .burger { display: inline-flex !important; }
  .header-inner { height: 64px !important; padding: 0 16px !important; gap: 12px !important; }
  .logo img { height: 30px !important; }
  .actions { gap: 4px !important; }
  .language-switcher {
    border-left: none;
    padding-left: 0;
    gap: 4px;
  }
  .lang-btn { font-size: 12px; padding: 2px 4px; }
}
</style>