<template>
  <div v-if="checking" class="esc-checking">Cargando...</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <span class="esc-hero-avatar">{{ userInitials }}</span>
        <div>
          <span class="esc-hero-tag">Panel de profesor</span>
          <h1 class="esc-hero-title">Hola, {{ userDisplayName }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <section class="esc-block">
        <h2 class="esc-section-title">Mis cursos</h2>

        <div v-if="loadingCourses" class="esc-empty">
          <p class="esc-empty-text">Cargando...</p>
        </div>
        <div v-else-if="courses.length === 0" class="esc-empty">
          <p class="esc-empty-text">Todavía no tienes cursos asignados.</p>
        </div>

        <div v-else class="esc-course-list">
          <div v-for="course in courses" :key="course.id" class="esc-course-card">
            <button class="esc-course-head" @click="toggleCourse(course.id)">
              <span class="esc-course-title">{{ course.title }}</span>
              <span class="esc-course-meta">
                {{ course.students_count }} alumnos
                <span v-if="course.pending_submissions_count" class="esc-badge">
                  {{ course.pending_submissions_count }} por revisar
                </span>
              </span>
            </button>

            <div v-if="activeCourseId === course.id" class="esc-roster">
              <p v-if="rosterLoading" class="esc-muted">Cargando alumnos...</p>
              <template v-else>
                <p v-if="roster.length === 0" class="esc-muted">Nadie ha comprado este curso todavía.</p>
                <div v-for="st in roster" :key="st.id" class="esc-student">
                  <div class="esc-student-info">
                    <span class="esc-student-name">{{ st.student }}</span>
                    <span class="esc-student-email">{{ st.email }}</span>
                  </div>
                  <div class="esc-student-progress">
                    <div class="esc-progress-bar">
                      <div class="esc-progress-fill" :style="{ width: st.progress_percent + '%' }"></div>
                    </div>
                    <span class="esc-progress-val">{{ st.progress_percent }}% ({{ st.lessons_completed }}/{{ st.lessons_total }})</span>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </section>

      <section class="esc-block">
        <h2 class="esc-section-title">Tareas por revisar</h2>

        <div v-if="submissions.length === 0" class="esc-empty">
          <p class="esc-empty-text">No hay tareas pendientes de revisión.</p>
        </div>

        <div v-else class="esc-course-list">
          <div v-for="s in submissions" :key="s.id" class="esc-sub-card">
            <div class="esc-sub-main">
              <strong>{{ s.student }}</strong> — {{ s.assignment_title }}
              <div class="esc-sub-sub">{{ s.course_title }} · {{ s.lesson_title }}</div>
            </div>
            <span class="esc-badge">{{ statusLabel(s.status) }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'

const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()

const checking = ref(true)
const loadingCourses = ref(true)
const courses = ref([])
const submissions = ref([])

// раскрытый курс + его ростер студентов
const activeCourseId = ref(null)
const rosterLoading = ref(false)
const roster = ref([])

const statusLabel = (s) => ({
  submitted: 'En revisión',
  reviewed: 'Revisado',
  needs_revision: 'Devuelto',
}[s] || s)

const toggleCourse = async (courseId) => {
  if (activeCourseId.value === courseId) {
    activeCourseId.value = null
    return
  }
  activeCourseId.value = courseId
  rosterLoading.value = true
  roster.value = []
  try {
    const { data } = await schoolApi.teacherCourseStudents(courseId)
    roster.value = data.students
  } catch (error) {
    console.error('Error al cargar alumnos:', error)
  } finally {
    rosterLoading.value = false
  }
}

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
  // гейт, что и в API - permission IsDev).
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
    const [cr, sr] = await Promise.all([
      schoolApi.teacherCourses(),
      schoolApi.teacherSubmissions(),
    ])
    courses.value = cr.data
    submissions.value = sr.data
  } catch (error) {
    console.error('Error al cargar el panel del profesor:', error)
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

.esc-block + .esc-block {
  margin-top: 40px;
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
  margin: 0;
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
}

.esc-course-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
}

/* --- Список курсов препода с раскрытием ростера --- */
.esc-course-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.esc-course-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  overflow: hidden;
}

.esc-course-head {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  padding: 20px 24px;
}

.esc-course-meta {
  font-size: 14px;
  color: #8a8079;
  display: flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
}

.esc-badge {
  display: inline-block;
  background: #fff4e0;
  color: #9a6a00;
  font-size: 12.5px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
}

.esc-roster {
  border-top: 1px solid #ece7e1;
  padding: 12px 24px 20px;
}

.esc-muted {
  color: #8a8079;
  margin: 8px 0;
}

.esc-student {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #f0ebe5;
}

.esc-student:last-child { border-bottom: none; }

.esc-student-info { display: flex; flex-direction: column; min-width: 0; }
.esc-student-name { font-weight: 600; color: #15110f; }
.esc-student-email { font-size: 13px; color: #8a8079; }

.esc-student-progress {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  width: 260px;
  max-width: 45%;
}

.esc-progress-bar {
  flex: 1;
  height: 7px;
  border-radius: 4px;
  background: #f0ebe5;
  overflow: hidden;
}

.esc-progress-fill {
  height: 100%;
  border-radius: 4px;
  background: #8e1519;
}

.esc-progress-val {
  font-size: 13px;
  color: #6b6259;
  white-space: nowrap;
}

.esc-sub-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.esc-sub-main { min-width: 0; }
.esc-sub-sub { font-size: 13px; color: #8a8079; margin-top: 2px; }

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
