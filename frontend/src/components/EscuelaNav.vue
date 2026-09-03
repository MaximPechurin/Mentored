<template>
  <header class="esc-nav">
    <div class="esc-nav-inner">
      <router-link :to="schoolHome" class="esc-brand">
        <span class="esc-brand-name">Mentored</span>
        <span class="esc-brand-sep">·</span>
        <span class="esc-brand-tag">Escuela</span>
      </router-link>

      <nav class="esc-nav-links">
        <router-link v-if="isStudent" to="/escuela/estudiante">{{ st('nav.misCursos') }}</router-link>
        <router-link v-if="isTeacher" to="/escuela/profesor">{{ st('nav.panelProfesor') }}</router-link>
        <router-link to="/escuela/foros">{{ st('nav.foros') }}</router-link>
      </nav>

      <div class="esc-nav-actions">
        <div v-if="isSuperuser" class="esc-lang">
          <button
            v-for="lang in supported"
            :key="lang"
            class="esc-lang-btn"
            :class="{ active: schoolLang === lang }"
            @click="setSchoolLang(lang)"
          >{{ lang.toUpperCase() }}</button>
        </div>
        <router-link to="/" class="esc-back-site">{{ st('nav.volverSitio') }}</router-link>
        <button class="esc-logout" @click="handleLogout">{{ st('nav.salir') }}</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { useSchoolLang } from '../composables/useSchoolLang'

const router = useRouter()
const { user, logout } = useAuth()
const { st, schoolLang, supported, setSchoolLang } = useSchoolLang()

const isStudent = computed(() => !!user.value?.roles?.includes('student'))
const isTeacher = computed(() => !!user.value?.roles?.includes('teacher'))
const isSuperuser = computed(() => !!user.value?.is_superuser)
// Куда ведёт логотип: у препода - его панель, иначе - кабинет студента
const schoolHome = computed(() => (isTeacher.value ? '/escuela/profesor' : '/escuela/estudiante'))

// Переключатель языка - только для суперюзеров (тестирование локализации).
// Обычные студенты/преподаватели всегда видят испанский, даже если в
// localStorage этого браузера случайно остался другой school_lang.
watch(isSuperuser, (val) => {
  if (!val) setSchoolLang('es')
}, { immediate: true })

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.esc-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #0e0c0c;
  border-bottom: 1px solid #241d1d;
}

.esc-nav-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 64px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 28px;
}

.esc-brand {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  text-decoration: none;
  flex-shrink: 0;
}

.esc-brand-name {
  font-family: 'Playfair Display', serif;
  font-size: 21px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 0.2px;
}

.esc-brand-sep { color: #6b625c; }

.esc-brand-tag {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #c49a3f;
}

.esc-nav-links {
  display: flex;
  align-items: center;
  gap: 22px;
  flex: 1;
}

.esc-nav-links a {
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  color: #b8afa8;
  transition: color 0.2s;
}

.esc-nav-links a:hover { color: #ffffff; }
.esc-nav-links a.router-link-active { color: #c49a3f; }

.esc-nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.esc-lang {
  display: flex;
  align-items: center;
  gap: 2px;
  border: 1px solid #3a3230;
  border-radius: 999px;
  padding: 2px;
}

.esc-lang-btn {
  background: none;
  border: none;
  color: #8a8079;
  font-family: inherit;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  padding: 4px 9px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
}

.esc-lang-btn:hover { color: #ffffff; }

.esc-lang-btn.active {
  background: #c49a3f;
  color: #0e0c0c;
}

.esc-back-site {
  text-decoration: none;
  font-size: 14px;
  color: #8a8079;
  transition: color 0.2s;
}

.esc-back-site:hover { color: #ffffff; }

.esc-logout {
  background: none;
  border: 1px solid #3a3230;
  color: #b8afa8;
  font-family: inherit;
  font-size: 14px;
  padding: 7px 16px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
}

.esc-logout:hover {
  border-color: #8e1519;
  color: #ffffff;
}

@media (max-width: 720px) {
  .esc-nav-inner { height: 56px; padding: 0 14px; gap: 14px; }
  .esc-nav-links { gap: 14px; }
  .esc-nav-links a { font-size: 14px; }
  .esc-back-site { display: none; }
}
</style>
