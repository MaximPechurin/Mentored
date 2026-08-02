<template>
  <div v-if="checking || loading" class="esc-checking">Cargando...</div>
  <div v-else-if="forbidden" class="esc-checking">
    <p>No tienes acceso a este curso.</p>
  </div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <router-link to="/escuela/estudiante" class="esc-back">&larr; Mis cursos</router-link>
          <h1 class="esc-hero-title">{{ course.title }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <p v-if="course.description" class="esc-course-description">{{ course.description }}</p>

      <div v-for="module in course.modules" :key="module.id" class="esc-module">
        <h2 class="esc-module-title">{{ module.title }}</h2>

        <div class="esc-lessons">
          <div v-for="lesson in module.lessons" :key="lesson.id" class="esc-lesson">
            <button class="esc-lesson-row" @click="toggleLesson(lesson.id)">
              <span class="esc-lesson-check" :class="{ done: lesson.is_completed }">
                {{ lesson.is_completed ? '✓' : '' }}
              </span>
              <span class="esc-lesson-title">{{ lesson.title }}</span>
              <span v-if="lesson.duration_minutes" class="esc-lesson-duration">{{ lesson.duration_minutes }} min</span>
            </button>

            <div v-if="activeLessonId === lesson.id" class="esc-lesson-body">
              <div v-if="embedUrl(lesson.video_url)" class="esc-video-wrapper">
                <iframe
                  :src="embedUrl(lesson.video_url)"
                  frameborder="0"
                  allow="autoplay; fullscreen; picture-in-picture"
                  allowfullscreen
                ></iframe>
              </div>
              <a v-else-if="lesson.video_url" :href="lesson.video_url" target="_blank" rel="noopener" class="esc-video-link">
                Ver video
              </a>

              <p v-if="lesson.content" class="esc-lesson-content">{{ lesson.content }}</p>

              <ul v-if="lesson.materials.length" class="esc-materials">
                <li v-for="material in lesson.materials" :key="material.id">
                  <a :href="material.file" target="_blank" rel="noopener">{{ material.title }}</a>
                </li>
              </ul>

              <button
                class="esc-complete-btn"
                :disabled="savingLessonId === lesson.id"
                @click="toggleComplete(lesson)"
              >
                {{ lesson.is_completed ? 'Marcar como no visto' : 'Marcar como completado' }}
              </button>
            </div>
          </div>
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

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ title: '', description: '', modules: [] })
const activeLessonId = ref(null)
const savingLessonId = ref(null)

const toggleLesson = (lessonId) => {
  activeLessonId.value = activeLessonId.value === lessonId ? null : lessonId
}

// Конвертация обычной ссылки на YouTube/Vimeo в embed-плеер. Если формат
// не распознан - просто отдаём ссылку "Ver video" (см. шаблон выше).
const embedUrl = (url) => {
  if (!url) return null
  const youtubeWatch = url.match(/youtube\.com\/watch\?v=([\w-]+)/)
  if (youtubeWatch) return `https://www.youtube.com/embed/${youtubeWatch[1]}`
  const youtubeShort = url.match(/youtu\.be\/([\w-]+)/)
  if (youtubeShort) return `https://www.youtube.com/embed/${youtubeShort[1]}`
  if (url.includes('youtube.com/embed/')) return url
  const vimeo = url.match(/vimeo\.com\/(\d+)/)
  if (vimeo) return `https://player.vimeo.com/video/${vimeo[1]}`
  return null
}

const toggleComplete = async (lesson) => {
  savingLessonId.value = lesson.id
  try {
    const response = await schoolApi.updateLessonProgress(lesson.id, {
      is_completed: !lesson.is_completed,
    })
    lesson.is_completed = response.data.is_completed
  } catch (error) {
    console.error('Error al guardar el progreso:', error)
    alert('No se pudo guardar el progreso. Intenta de nuevo.')
  } finally {
    savingLessonId.value = null
  }
}

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  const fresh = await refreshUser()
  const roles = fresh?.roles ?? user.value?.roles ?? []

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

.esc-lesson + .esc-lesson {
  border-top: 1px solid #ece7e1;
}

.esc-lesson-row {
  width: 100%;
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
}

.esc-lesson-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid #d8d1c8;
  font-size: 13px;
  color: #fff;
  flex-shrink: 0;
}

.esc-lesson-check.done {
  background: #8e1519;
  border-color: #8e1519;
}

.esc-lesson-title {
  flex: 1;
  font-weight: 500;
}

.esc-lesson-duration {
  font-size: 13.5px;
  color: #8a8079;
}

.esc-lesson-body {
  padding: 0 22px 22px;
}

.esc-video-wrapper {
  position: relative;
  padding-top: 56.25%;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;
}

.esc-video-wrapper iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.esc-video-link {
  display: inline-block;
  margin-bottom: 16px;
  color: #8e1519;
  font-weight: 600;
  text-decoration: none;
}

.esc-lesson-content {
  font-size: 15px;
  line-height: 1.6;
  color: #3f3a35;
  margin: 0 0 16px;
  white-space: pre-line;
}

.esc-materials {
  margin: 0 0 16px;
  padding-left: 20px;
}

.esc-materials a {
  color: #8e1519;
  text-decoration: none;
  font-weight: 500;
}

.esc-materials a:hover {
  text-decoration: underline;
}

.esc-complete-btn {
  background: #0e0c0c;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-weight: 600;
  font-size: 14.5px;
  padding: 11px 22px;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.3s;
}

.esc-complete-btn:hover:not(:disabled) {
  background: #2a2525;
}

.esc-complete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
