<template>
  <div v-if="checking" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <span class="esc-hero-tag">{{ st('foro.listaSub') }}</span>
          <h1 class="esc-hero-title">{{ st('foro.listaTitle') }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <div v-if="loading" class="esc-empty">
        <p class="esc-empty-text">{{ st('common.cargando') }}</p>
      </div>
      <div v-else-if="forums.length === 0" class="esc-empty">
        <p class="esc-empty-text">{{ st('foro.sinForos') }}</p>
      </div>

      <div v-else class="esc-foros-list">
        <router-link
          v-for="f in forums"
          :key="f.id"
          :to="`/escuela/foro/${f.id}`"
          class="esc-foro-card"
        >
          <span class="esc-foro-icon">💬</span>
          <span class="esc-foro-main">
            <span class="esc-foro-title">{{ f.title }}</span>
            <span class="esc-foro-meta">
              {{ f.threads_count }} {{ st('foro.temas') }}
              <span v-if="f.is_teacher" class="esc-foro-badge">{{ st('foro.profe') }}</span>
            </span>
          </span>
          <span class="esc-foro-arrow">→</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'

const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forums = ref([])

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  const fresh = await refreshUser()
  const isDev = fresh?.is_dev ?? user.value?.is_dev ?? false

  // Раздел «Школа» пока закрыт для всех, кроме dev-аккаунтов (тот же
  // гейт, что и в API - permission IsDev).
  if (!isDev) {
    router.replace('/')
    return
  }

  checking.value = false

  try {
    const { data } = await schoolApi.forumsList()
    forums.value = data
  } catch (error) {
    console.error('Error al cargar los foros:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.esc-checking {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  color: #6b6259;
}

.esc-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f6f3ef;
  min-height: 100vh;
}

.esc-hero {
  background: #0e0c0c;
  padding: 52px 32px;
}

.esc-hero-container {
  max-width: 900px;
  margin: 0 auto;
}

.esc-hero-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 8px;
}

.esc-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  line-height: 1.15;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.3px;
}

.esc-shell {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 32px 88px;
}

.esc-empty {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 48px 32px;
  text-align: center;
}

.esc-empty-text {
  font-size: 16px;
  color: #6b6259;
  margin: 0;
}

.esc-foros-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.esc-foro-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 20px 24px;
  text-decoration: none;
  color: #1c1c1c;
  transition: border-color 0.2s, background 0.2s;
}

.esc-foro-card:hover {
  border-color: #8e1519;
  background: #faf8f5;
}

.esc-foro-icon { font-size: 24px; flex-shrink: 0; }

.esc-foro-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.esc-foro-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
}

.esc-foro-meta {
  font-size: 13.5px;
  color: #8a8079;
  display: flex;
  align-items: center;
  gap: 8px;
}

.esc-foro-badge {
  display: inline-block;
  background: #f6ecd9;
  color: #9a6a00;
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding: 2px 9px;
  border-radius: 999px;
}

.esc-foro-arrow {
  font-size: 18px;
  color: #8e1519;
  flex-shrink: 0;
}

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
