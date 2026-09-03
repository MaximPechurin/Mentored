<template>
  <div v-if="checking || loading" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else-if="forbidden" class="esc-checking">
    <p>{{ st('course.sinAcceso') }}</p>
  </div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <router-link to="/escuela/estudiante" class="esc-back">{{ st('course.volverCursos') }}</router-link>
          <h1 class="esc-hero-title">{{ course.title }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <p v-if="course.description" class="esc-course-description">{{ course.description }}</p>

      <div v-for="module in course.modules" :key="module.id" class="esc-module">
        <h2 class="esc-module-title">{{ module.title }}</h2>

        <div class="esc-lessons">
          <router-link
            v-for="lesson in module.lessons"
            :key="lesson.id"
            :to="`/escuela/curso/${course.slug}/leccion/${lesson.id}`"
            class="esc-lesson-row"
          >
            <span class="esc-lesson-check" :class="{ done: lesson.is_completed }">
              {{ lesson.is_completed ? '✓' : '' }}
            </span>
            <span class="esc-lesson-main">
              <span class="esc-lesson-title">{{ lesson.title }}</span>
              <span v-if="lesson.content" class="esc-lesson-snippet">{{ snippet(lesson.content) }}</span>
            </span>
            <span class="esc-lesson-side">
              <span v-if="lesson.assignments && lesson.assignments.length" class="esc-lesson-task">📝</span>
              <span v-if="lesson.duration_minutes" class="esc-lesson-duration">{{ lesson.duration_minutes }} {{ st('course.min') }}</span>
            </span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ title: '', description: '', modules: [] })

// короткий анонс под названием урока в списке (как в референсе)
const snippet = (text) => {
  const t = (text || '').replace(/\s+/g, ' ').trim()
  return t.length > 110 ? t.slice(0, 110) + '…' : t
}

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  const fresh = await refreshUser()
  const isDev = fresh?.is_dev ?? user.value?.is_dev ?? false
  const roles = fresh?.roles ?? user.value?.roles ?? []

  // Раздел «Школа» пока закрыт для всех, кроме dev-аккаунтов (тот же
  // гейт, что и в API - permission IsDev).
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
    const response = await schoolApi.getCourse(route.params.slug)
    course.value = response.data
  } catch (error) {
    if (error.response?.status === 403 || error.response?.status === 404) {
      forbidden.value = true
    } else {
      console.error('Error al cargar el curso:', error)
    }
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

.esc-back {
  display: inline-block;
  color: #c49a3f;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
}

.esc-back:hover {
  text-decoration: underline;
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

.esc-course-description {
  font-size: 16px;
  color: #6b6259;
  margin: 0 0 32px;
}

.esc-module {
  margin-bottom: 28px;
}

.esc-module-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 14px;
}

.esc-lessons {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  overflow: hidden;
}

.esc-lesson-row + .esc-lesson-row {
  border-top: 1px solid #ece7e1;
}

.esc-lesson-row {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 22px;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 16px;
  text-align: left;
  color: #1c1c1c;
  text-decoration: none;
  transition: background 0.2s;
}

.esc-lesson-row:hover { background: #faf8f5; }

.esc-lesson-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 8px;
  border: 1.5px solid #d8d1c8;
  font-size: 14px;
  color: #fff;
  flex-shrink: 0;
}

.esc-lesson-check.done {
  background: #8e1519;
  border-color: #8e1519;
}

.esc-lesson-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.esc-lesson-title {
  font-weight: 500;
}

.esc-lesson-snippet {
  font-size: 13px;
  color: #8a8079;
  line-height: 1.4;
}

.esc-lesson-side {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.esc-lesson-task { font-size: 15px; }

.esc-lesson-duration {
  font-size: 13.5px;
  color: #8a8079;
  white-space: nowrap;
}


@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
