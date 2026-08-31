<template>
  <div v-if="checking || loading" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else-if="forbidden" class="esc-checking">
    <p>{{ st('course.sinAcceso') }}</p>
  </div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <router-link to="/escuela/profesor" class="esc-back">{{ st('common.volver') }}</router-link>
          <span class="esc-hero-tag">{{ st('teacher.progresoAlumno') }}</span>
          <h1 class="esc-hero-title">{{ course.title }}</h1>
          <p v-if="course.student" class="esc-hero-student">{{ course.student.name }} · {{ course.student.email }}</p>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <div v-for="module in course.modules" :key="module.id" class="esc-module">
        <h2 class="esc-module-title">{{ module.title }}</h2>

        <div class="esc-lessons">
          <div v-for="lesson in module.lessons" :key="lesson.id" class="esc-lesson">
            <button class="esc-lesson-row" @click="toggleLesson(lesson.id)">
              <span class="esc-lesson-check" :class="{ done: lesson.is_completed }">
                {{ lesson.is_completed ? '✓' : '' }}
              </span>
              <span class="esc-lesson-title">{{ lesson.title }}</span>
              <span v-if="lesson.duration_minutes" class="esc-lesson-duration">{{ lesson.duration_minutes }} {{ st('course.min') }}</span>
            </button>

            <div v-if="activeLessonId === lesson.id" class="esc-lesson-body">
              <p v-if="lesson.content" class="esc-lesson-content">{{ lesson.content }}</p>

              <ul v-if="lesson.materials.length" class="esc-materials">
                <li v-for="material in lesson.materials" :key="material.id">
                  <a :href="material.file" target="_blank" rel="noopener">{{ material.title }}</a>
                </li>
              </ul>

              <div v-if="lesson.assignments && lesson.assignments.length" class="esc-assignments">
                <div v-for="a in lesson.assignments" :key="a.id" class="esc-assignment-static">
                  📝 {{ a.title }} <span class="esc-assignment-max">— {{ a.max_score }} {{ st('course.pts') }}</span>
                </div>
              </div>
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
import { useSchoolLang } from '../../composables/useSchoolLang'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ title: '', modules: [], student: null })
const activeLessonId = ref(null)

const toggleLesson = (lessonId) => {
  activeLessonId.value = activeLessonId.value === lessonId ? null : lessonId
}

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  const fresh = await refreshUser()
  const isDev = fresh?.is_dev ?? user.value?.is_dev ?? false
  const roles = fresh?.roles ?? user.value?.roles ?? []

  if (!isDev) {
    router.replace('/')
    return
  }

  if (!roles.includes('teacher')) {
    router.replace('/cuenta')
    return
  }

  checking.value = false

  try {
    const response = await schoolApi.teacherStudentCourse(route.params.courseId, route.params.userId)
    course.value = response.data
  } catch (error) {
    if (error.response?.status === 403 || error.response?.status === 404) {
      forbidden.value = true
    } else {
      console.error('Error al cargar el progreso del alumno:', error)
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

.esc-hero-tag {
  display: block;
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

.esc-hero-student {
  color: #b8afa8;
  font-size: 14.5px;
  margin: 8px 0 0;
}

.esc-shell {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 32px 88px;
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

.esc-assignments {
  margin: 4px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.esc-assignment-static {
  font-size: 14.5px;
  color: #3f3a35;
}

.esc-assignment-max {
  color: #8a8079;
}

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
