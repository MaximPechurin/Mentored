<template>
  <div v-if="checking" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <span class="esc-hero-avatar">{{ userInitials }}</span>
        <div>
          <span class="esc-hero-tag">{{ st('teacher.panel') }}</span>
          <h1 class="esc-hero-title">{{ st('teacher.hola') }}, {{ userDisplayName }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <!-- Обзор платформы (только суперюзер) -->
      <section v-if="platform" class="esc-block">
        <h2 class="esc-section-title">{{ st('stats.platform') }}</h2>
        <div class="stats-grid">
          <div class="stat-card"><span class="stat-num">{{ platform.courses_active }}</span><span class="stat-lbl">{{ st('stats.activeCourses') }}</span></div>
          <div class="stat-card"><span class="stat-num">{{ platform.students_active }}</span><span class="stat-lbl">{{ st('stats.activeStudents') }}</span></div>
          <div class="stat-card"><span class="stat-num">{{ platform.teachers_total }}</span><span class="stat-lbl">{{ st('stats.teachers') }}</span></div>
          <div class="stat-card"><span class="stat-num">{{ platform.enrollments_active }}</span><span class="stat-lbl">{{ st('stats.enrollments') }}</span></div>
          <div class="stat-card"><span class="stat-num">{{ platform.avg_completion }}%</span><span class="stat-lbl">{{ st('stats.avgCompletion') }}</span></div>
          <div class="stat-card"><span class="stat-num">{{ platform.forum_threads }}</span><span class="stat-lbl">{{ st('stats.forumThreads') }}</span></div>
        </div>
      </section>

      <section class="esc-block">
        <h2 class="esc-section-title">{{ st('teacher.misCursos') }}</h2>

        <div v-if="loadingCourses" class="esc-empty">
          <p class="esc-empty-text">{{ st('common.cargando') }}</p>
        </div>
        <div v-else-if="courses.length === 0" class="esc-empty">
          <p class="esc-empty-text">{{ st('teacher.sinCursos') }}</p>
        </div>

        <div v-else class="esc-course-list">
          <div v-for="course in courses" :key="course.id" class="esc-course-card">
            <button class="esc-course-head" @click="toggleCourse(course.id)">
              <span class="esc-course-title">{{ course.title }}</span>
              <span class="esc-course-meta">
                {{ course.students_count }} {{ st('teacher.alumnos') }}
                <span v-if="course.pending_submissions_count" class="esc-badge">
                  {{ course.pending_submissions_count }} {{ st('teacher.porRevisar') }}
                </span>
              </span>
            </button>

            <div v-if="activeCourseId === course.id" class="esc-roster">
              <router-link :to="`/escuela/foro/${course.id}`" class="esc-foro-link">💬 {{ st('foro.open') }}</router-link>

              <!-- аналитика курса -->
              <div v-if="analytics" class="stats-grid stats-grid--course">
                <div class="stat-card"><span class="stat-num">{{ analytics.avg_progress }}%</span><span class="stat-lbl">{{ st('stats.avgProgress') }}</span></div>
                <div class="stat-card"><span class="stat-num">{{ analytics.distribution.completed }}</span><span class="stat-lbl">{{ st('stats.completed') }}</span></div>
                <div class="stat-card"><span class="stat-num">{{ analytics.distribution.in_progress }}</span><span class="stat-lbl">{{ st('stats.inProgress') }}</span></div>
                <div class="stat-card"><span class="stat-num">{{ analytics.distribution.not_started }}</span><span class="stat-lbl">{{ st('stats.notStarted') }}</span></div>
                <div class="stat-card"><span class="stat-num">{{ analytics.submissions.submitted }}</span><span class="stat-lbl">{{ st('stats.pending') }}</span></div>
                <div class="stat-card"><span class="stat-num">{{ analytics.submissions.reviewed }}</span><span class="stat-lbl">{{ st('stats.reviewed') }}</span></div>
              </div>

              <p v-if="rosterLoading" class="esc-muted">{{ st('teacher.cargandoAlumnos') }}</p>
              <template v-else>
                <p v-if="roster.length === 0" class="esc-muted">{{ st('teacher.nadieCompro') }}</p>
                <router-link
                  v-for="row in roster"
                  :key="row.id"
                  :to="`/escuela/profesor/curso/${course.id}/alumno/${row.user_id}`"
                  class="esc-student"
                >
                  <div class="esc-student-info">
                    <span class="esc-student-name">{{ row.student }}</span>
                    <span class="esc-student-email">{{ row.email }}</span>
                  </div>
                  <div class="esc-student-progress">
                    <div class="esc-progress-bar">
                      <div class="esc-progress-fill" :style="{ width: row.progress_percent + '%' }"></div>
                    </div>
                    <span class="esc-progress-val">{{ row.progress_percent }}% ({{ row.lessons_completed }}/{{ row.lessons_total }})</span>
                  </div>
                </router-link>
              </template>
            </div>
          </div>
        </div>
      </section>

      <section class="esc-block">
        <h2 class="esc-section-title">{{ st('teacher.tareasPorRevisar') }}</h2>

        <div v-if="submissions.length === 0" class="esc-empty">
          <p class="esc-empty-text">{{ st('teacher.sinTareas') }}</p>
        </div>

        <div v-else class="esc-course-list">
          <div v-for="s in submissions" :key="s.id" class="esc-sub-card">
            <button class="esc-sub-head" @click="toggleSubmission(s.id)">
              <div class="esc-sub-main">
                <strong>{{ s.student }}</strong> — {{ s.assignment_title }}
                <div class="esc-sub-sub">{{ s.course_title }} · {{ s.lesson_title }}</div>
              </div>
              <span class="esc-badge">{{ statusLabel(s.status) }}</span>
            </button>

            <div v-if="activeSubmissionId === s.id" class="esc-review">
              <!-- ответ студента -->
              <div class="esc-review-label">{{ st('teacher.respuestaAlumno') }}</div>
              <p class="esc-review-text">{{ s.text || st('teacher.sinTexto') }}</p>
              <p v-if="s.file" class="esc-review-file">
                {{ st('teacher.archivoAdjunto') }}:
                <a :href="s.file" target="_blank" rel="noopener">{{ st('teacher.verArchivo') }}</a>
              </p>

              <!-- форма проверки -->
              <div class="esc-review-form">
                <label class="esc-review-field">
                  <span>{{ st('teacher.calificacion') }} (0–{{ s.max_score }})</span>
                  <input type="number" min="0" :max="s.max_score" v-model.number="reviewScore" class="esc-score-input" />
                </label>
                <textarea v-model="reviewComment" rows="3" :placeholder="st('teacher.comentario')" class="esc-textarea"></textarea>
                <div class="esc-review-actions">
                  <button class="esc-btn-approve" :disabled="reviewing" @click="doReview(s, 'reviewed')">
                    {{ reviewing ? st('teacher.guardando') : st('teacher.marcarRevisado') }}
                  </button>
                  <button class="esc-btn-return" :disabled="reviewing" @click="doReview(s, 'needs_revision')">
                    {{ st('teacher.devolver') }}
                  </button>
                </div>
              </div>
            </div>
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
import { useSchoolLang } from '../../composables/useSchoolLang'

const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loadingCourses = ref(true)
const courses = ref([])
const submissions = ref([])

// раскрытый курс + его ростер студентов
const activeCourseId = ref(null)
const rosterLoading = ref(false)
const roster = ref([])

// проверка сдачи ДЗ
const activeSubmissionId = ref(null)
const reviewScore = ref(null)
const reviewComment = ref('')
const reviewing = ref(false)

// аналитика
const analytics = ref(null)          // по раскрытому курсу
const platform = ref(null)           // обзор платформы (суперюзер)
const isSuperuser = computed(() => !!user.value?.is_superuser)

const statusLabel = (s) => st('status.' + s)

const toggleSubmission = (id) => {
  if (activeSubmissionId.value === id) {
    activeSubmissionId.value = null
    return
  }
  activeSubmissionId.value = id
  const s = submissions.value.find((x) => x.id === id)
  // подставляем текущие значения (если уже оценивали)
  reviewScore.value = s?.score ?? null
  reviewComment.value = s?.mentor_comment ?? ''
}

const doReview = async (s, newStatus) => {
  reviewing.value = true
  try {
    await schoolApi.reviewSubmission(s.id, {
      status: newStatus,
      score: reviewScore.value,
      mentor_comment: reviewComment.value,
    })
    // сдача проверена - убираем из очереди "на проверку" и снижаем счётчик у курса
    submissions.value = submissions.value.filter((x) => x.id !== s.id)
    activeSubmissionId.value = null
    const course = courses.value.find((c) => c.title === s.course_title)
    if (course && course.pending_submissions_count > 0) course.pending_submissions_count -= 1
  } catch (error) {
    console.error('Error al revisar la tarea:', error)
    const msg = error.response?.data?.error || 'Error'
    alert(msg)
  } finally {
    reviewing.value = false
  }
}

const toggleCourse = async (courseId) => {
  if (activeCourseId.value === courseId) {
    activeCourseId.value = null
    return
  }
  activeCourseId.value = courseId
  rosterLoading.value = true
  roster.value = []
  analytics.value = null
  try {
    const [r, a] = await Promise.all([
      schoolApi.teacherCourseStudents(courseId),
      schoolApi.courseAnalytics(courseId),
    ])
    roster.value = r.data.students
    analytics.value = a.data
  } catch (error) {
    console.error('Error al cargar alumnos/analítica:', error)
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

  // обзор платформы - только суперюзеру
  if (isSuperuser.value) {
    try {
      const { data } = await schoolApi.platformAnalytics()
      platform.value = data
    } catch (e) { /* не критично */ }
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

.esc-foro-link {
  display: inline-block;
  margin-bottom: 12px;
  background: #faf8f5;
  border: 1px solid #ece7e1;
  border-radius: 999px;
  padding: 7px 16px;
  color: #8e1519;
  font-weight: 600;
  font-size: 13.5px;
  text-decoration: none;
}
.esc-foro-link:hover { border-color: #8e1519; }

/* --- карточки аналитики --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}
.stats-grid--course { margin: 0 0 18px; }
.stat-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 14px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.stats-grid--course .stat-card { background: #faf8f5; }
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #8e1519;
  line-height: 1;
}
.stat-lbl { font-size: 13px; color: #8a8079; }

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
  text-decoration: none;
  cursor: pointer;
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
  overflow: hidden;
}

.esc-sub-head {
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.esc-sub-main { min-width: 0; color: #1c1c1c; }
.esc-sub-sub { font-size: 13px; color: #8a8079; margin-top: 2px; }

/* --- панель проверки ДЗ --- */
.esc-review {
  border-top: 1px solid #ece7e1;
  padding: 16px 20px 20px;
}

.esc-review-label {
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #8a8079;
  margin-bottom: 6px;
}

.esc-review-text {
  font-size: 15px;
  line-height: 1.6;
  color: #3f3a35;
  white-space: pre-line;
  margin: 0 0 12px;
}

.esc-review-file { font-size: 14px; margin: 0 0 14px; }
.esc-review-file a { color: #8e1519; font-weight: 600; text-decoration: none; }
.esc-review-file a:hover { text-decoration: underline; }

.esc-review-form { border-top: 1px dashed #ece7e1; padding-top: 14px; }

.esc-review-field {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #3f3a35;
  margin-bottom: 10px;
}

.esc-score-input {
  width: 80px;
  border: 1px solid #e4ddd2;
  border-radius: 8px;
  padding: 8px 10px;
  font-family: inherit;
  font-size: 15px;
  background: #fbf9f6;
  outline: none;
}

.esc-score-input:focus { border-color: #8e1519; }

.esc-review-form .esc-textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e4ddd2;
  border-radius: 10px;
  padding: 10px 12px;
  font-family: inherit;
  font-size: 14.5px;
  background: #fbf9f6;
  outline: none;
  resize: vertical;
  margin-bottom: 12px;
}

.esc-review-form .esc-textarea:focus { border-color: #8e1519; }

.esc-review-actions { display: flex; gap: 10px; flex-wrap: wrap; }

.esc-btn-approve, .esc-btn-return {
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 20px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.esc-btn-approve { background: #2f7a3a; color: #fff; }
.esc-btn-return { background: #fff; color: #a52a2a; border: 1px solid #e2b8b8; }
.esc-btn-approve:disabled, .esc-btn-return:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
