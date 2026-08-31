<template>
  <div v-if="checking" class="esc-checking">Cargando...</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <span class="esc-hero-avatar">{{ userInitials }}</span>
        <div>
          <span class="esc-hero-tag">{{ st('student.panel') }}</span>
          <h1 class="esc-hero-title">{{ st('student.hola') }}, {{ userDisplayName }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <h2 class="esc-section-title">{{ st('student.misCursos') }}</h2>

      <div v-if="loadingCourses" class="esc-empty">
        <p class="esc-empty-text">{{ st('student.cargandoCursos') }}</p>
      </div>

      <div v-else-if="courses.length === 0" class="esc-empty">
        <p class="esc-empty-text">{{ st('student.sinCursos') }}</p>
        <router-link to="/tienda" class="esc-empty-btn">{{ st('student.verCursos') }}</router-link>
      </div>

      <div v-else class="esc-courses">
        <template v-for="course in courses" :key="course.id">
          <router-link
            :to="`/escuela/curso/${course.slug}`"
            class="esc-course"
          >
            <h3 class="esc-course-title">{{ course.title }}</h3>
            <p v-if="course.teachers.length" class="esc-course-teacher">{{ course.teachers.join(', ') }}</p>
            <div class="esc-progress">
              <span>{{ st('common.progreso') }}</span>
              <span class="esc-progress-value">{{ course.progress_percent }}%</span>
            </div>
            <div class="esc-progress-bar">
              <div class="esc-progress-fill" :style="{ width: course.progress_percent + '%' }"></div>
            </div>
          </router-link>

          <router-link :to="`/escuela/foro/${course.id}`" class="esc-foro-card">
            <span class="esc-foro-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </span>
            <div>
              <h3 class="esc-foro-title">{{ st('foro.title') }}</h3>
              <p class="esc-foro-sub">{{ course.title }}</p>
              <p class="esc-foro-desc">{{ st('foro.subtitulo') }}</p>
            </div>
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'

const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loadingCourses = ref(true)
const courses = ref([])

const userDisplayName = computed(() => {
  if (!user.value) return 'Invitado'
  return user.value.full_name || user.value.username || user.value.email || 'Invitado'
})

const userInitials = computed(() => {
  const name = userDisplayName.value
  return name ? name.charAt(0).toUpperCase() : '?'
})

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  // Роли/флаги могут быть устаревшими в localStorage (например, только
  // что назначены из админки) - подтягиваем свежий профиль перед проверкой.
  const fresh = await refreshUser()
  const isDev = fresh?.is_dev ?? user.value?.is_dev ?? false
  const roles = fresh?.roles ?? user.value?.roles ?? []

  // Раздел «Школа» пока закрыт для всех, кроме dev-аккаунтов (тот же
  // гейт, что и в API - permission IsDev). Обычному пользователю
  // отдаём как будто раздела нет - редирект на главную.
  if (!isDev) {
    router.replace('/')
    return
  }

  if (!roles.includes('student')) {
    router.replace('/cuenta')
    return
  }

  checking.value = false

  try {
    const response = await schoolApi.myCourses()
    courses.value = response.data
  } catch (error) {
    console.error('Error al cargar mis cursos:', error)
  } finally {
    loadingCourses.value = false
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
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 22px;
}

.esc-hero-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  flex-shrink: 0;
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
  font-size: 34px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.3px;
}

.esc-shell {
  max-width: 1180px;
  margin: 0 auto;
  padding: 48px 32px 88px;
}

.esc-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
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
  margin: 0 0 20px;
}

.esc-empty-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  background: #0e0c0c;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  padding: 12px 28px;
  border-radius: 999px;
  transition: background 0.3s;
}

.esc-empty-btn:hover {
  background: #2a2525;
}

.esc-courses {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.esc-course {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 22px;
  text-decoration: none;
  color: inherit;
  display: block;
  transition: border-color 0.3s;
}

.esc-course:hover {
  border-color: #8e1519;
}

.esc-course-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 6px;
}

.esc-course-teacher {
  font-size: 13.5px;
  color: #8a8079;
  margin: 0 0 16px;
}

.esc-progress {
  display: flex;
  justify-content: space-between;
  font-size: 13.5px;
  color: #8a8079;
  margin-bottom: 8px;
}

.esc-progress-value {
  font-weight: 600;
  color: #8e1519;
}

.esc-progress-bar {
  height: 7px;
  border-radius: 4px;
  background: #f0ebe5;
  overflow: hidden;
}

.esc-progress-fill {
  height: 100%;
  border-radius: 4px;
  background: #8e1519;
  transition: width 0.3s;
}

/* --- Panel del foro (junto a las tarjetas de curso) --- */
.esc-foro-card {
  grid-column: span 2;
  display: flex;
  align-items: center;
  gap: 18px;
  background: #0e0c0c;
  border: 1.5px solid #c49a3f;
  border-radius: 18px;
  padding: 26px 28px;
  text-decoration: none;
  transition: background 0.3s, border-color 0.3s;
}

.esc-foro-card:hover {
  background: #1a1614;
  border-color: #d9ac4b;
}

.esc-foro-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(196, 154, 63, 0.15);
  color: #c49a3f;
  flex-shrink: 0;
}

.esc-foro-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 4px;
}

.esc-foro-sub {
  font-size: 14px;
  font-weight: 600;
  color: #c49a3f;
  margin: 0 0 4px;
}

.esc-foro-desc {
  font-size: 13.5px;
  color: #b8afa8;
  margin: 0;
}

@media (max-width: 920px) {
  .esc-foro-card { grid-column: span 1; padding: 20px; }
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
