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

    <!-- WhatsApp group -->
    <section v-if="course.whatsapp_group" class="esc-whatsapp">
      <div class="esc-whatsapp-inner">
        <div class="esc-whatsapp-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
          </svg>
        </div>
        <div class="esc-whatsapp-body">
          <h3 class="esc-whatsapp-title">
            {{ course.whatsapp_group.name || st('course.whatsappGroupDefault') || 'Grupo de WhatsApp' }}
          </h3>
          <p v-if="course.whatsapp_group.description" class="esc-whatsapp-desc">
            {{ course.whatsapp_group.description }}
          </p>
          <p v-else class="esc-whatsapp-desc">
            {{ st('course.whatsappGroupHint') || 'Únete al grupo del curso para resolver dudas y compartir con otros alumnos.' }}
          </p>
        </div>
        <a
          :href="course.whatsapp_group.url"
          target="_blank"
          rel="noopener"
          class="esc-whatsapp-btn"
        >
          {{ st('course.joinWhatsapp') || 'Unirme al grupo' }}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </a>
      </div>
    </section>

    <div v-if="course.access_expires_at" class="esc-access-banner" :class="bannerClass">
      <template v-if="course.access_status === 'active'">
        <span class="esc-access-icon">⏳</span>
        <span>
          {{ st('course.accessHasta') || 'Tu acceso está disponible hasta' }}
          <strong>{{ fmtDate(course.access_expires_at) }}</strong>
          ({{ daysLeftLabel }})
        </span>
      </template>
      <template v-else-if="course.access_status === 'expired'">
        <span class="esc-access-icon">🔒</span>
        <span>
          {{ st('course.accessExpirado') || 'Tu acceso ha expirado. Contáctanos para renovarlo.' }}
        </span>
      </template>
      <template v-else-if="course.access_status === 'not_started'">
        <span class="esc-access-icon">🕐</span>
        <span>
          {{ st('course.accessProximo') || 'El acceso se abrirá próximamente.' }}
        </span>
      </template>
    </div>

    <div class="esc-shell">
      <p v-if="course.description" class="esc-course-description">{{ course.description }}</p>

      <button v-if="course.has_certificate" class="esc-certificate-btn" @click="downloadCertificate">
        🎓 {{ st('student.descargarCertificado') }}
      </button>

      <div v-for="module in course.modules" :key="module.id" class="esc-module">
        <h2 class="esc-module-title">{{ module.title }}</h2>

        <div class="esc-lessons">
          <router-link
            v-for="lesson in module.lessons"
            :key="lesson.id"
            :to="`/escuela/curso/${course.slug}/leccion/${lesson.id}`"
            class="esc-lesson-row"
            :class="{ locked: isLessonLocked(lesson.id) }"
            :title="isLessonLocked(lesson.id) ? st('leccion.leccionBloqueada') : ''"
            @click="onLessonClick($event, lesson)"
          >
            <span class="esc-lesson-check" :class="{ done: lesson.is_completed }">
              {{ lesson.is_completed ? '✓' : (isLessonLocked(lesson.id) ? '🔒' : '') }}
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'
import { stripHtml } from '../../composables/useLessonContent'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ title: '', description: '', modules: [] })

// короткий анонс под названием урока в списке (как в референсе).
// stripHtml - на случай, если контент урока сделан визуальным редактором
// (HTML): в превью показываем чистый текст без тегов.
const snippet = (text) => {
  const t = stripHtml(text).replace(/\s+/g, ' ').trim()
  return t.length > 110 ? t.slice(0, 110) + '…' : t
}

const downloadCertificate = async () => {
  try {
    const response = await schoolApi.downloadCertificate(course.value.slug)
    const url = URL.createObjectURL(response.data)
    const a = document.createElement('a')
    a.href = url
    a.download = `certificado-${course.value.slug}.png`
    a.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error al descargar el certificado:', error)
    alert('No se pudo descargar el certificado.')
  }
}

// последовательная блокировка: урок доступен, только если пройден
// непосредственно предыдущий - тот же критерий, что и в EscuelaLeccionPage
const flatLessons = computed(() =>
  (course.value.modules || []).flatMap((m) => m.lessons || [])
)
const lockedLessonIds = computed(() => {
  const arr = flatLessons.value
  const locked = new Set()
  for (let i = 1; i < arr.length; i++) {
    if (!arr[i - 1].is_completed) locked.add(arr[i].id)
  }
  return locked
})
const isLessonLocked = (lessonId) => lockedLessonIds.value.has(lessonId)
const onLessonClick = (event, lesson) => {
  if (isLessonLocked(lesson.id)) event.preventDefault()
}

const daysLeftLabel = computed(() => {
  const days = course.value?.days_left
  if (days === null || days === undefined) return ''
  if (days === 0) return 'vence hoy'
  if (days === 1) return 'queda 1 día'
  return `quedan ${days} días`
})

const bannerClass = computed(() => ({
  'esc-access-banner--active': course.value?.access_status === 'active',
  'esc-access-banner--warn': course.value?.access_status === 'active' && course.value?.days_left <= 7,
  'esc-access-banner--expired': course.value?.access_status === 'expired',
  'esc-access-banner--pending': course.value?.access_status === 'not_started',
}))

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

.esc-certificate-btn {
  display: inline-block;
  margin: -16px 0 32px;
  background: #0e0c0c;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14.5px;
  padding: 11px 22px;
  cursor: pointer;
  transition: background 0.3s;
}

.esc-certificate-btn:hover { background: #2a2525; }

.esc-whatsapp-btn {
  display: inline-block;
  margin: -16px 0 32px;
  background: #2f7a3a;
  color: #fff;
  text-decoration: none;
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14.5px;
  padding: 11px 22px;
  cursor: pointer;
  transition: background 0.3s;
}

.esc-whatsapp-btn:hover { background: #256030; }

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

.esc-lesson-row.locked {
  color: #b0a99f;
  cursor: not-allowed;
}
.esc-lesson-row.locked:hover { background: none; }

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

.esc-access-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 14px;
  font-size: 14.5px;
  margin-bottom: 20px;
  border: 1px solid transparent;
}

.esc-access-banner--active {
  background: #eaf5ed;
  border-color: #cbe5d2;
  color: #2f7a3a;
}

.esc-access-banner--warn {
  background: #fff5e0;
  border-color: #f3ddb3;
  color: #8c6a10;
}

.esc-access-banner--expired {
  background: #fbeaea;
  border-color: #f0cccc;
  color: #8e1519;
}

.esc-access-banner--pending {
  background: #f0ede8;
  border-color: #d8d1c8;
  color: #6f655c;
}

.esc-access-icon { font-size: 18px; }

/* ===== WhatsApp group ===== */
.esc-whatsapp {
  max-width: 1180px;
  margin: 20px auto 0;
  padding: 0 32px;
}

.esc-whatsapp-inner {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-left: 4px solid #25d366; /* WhatsApp green */
  border-radius: 16px;
  padding: 20px 24px;
  flex-wrap: wrap;
}

.esc-whatsapp-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #e7f9ee;
  color: #1ea952;
  flex-shrink: 0;
}

.esc-whatsapp-body {
  flex: 1;
  min-width: 200px;
}

.esc-whatsapp-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 4px;
}

.esc-whatsapp-desc {
  font-size: 14px;
  color: #6b6259;
  margin: 0;
  line-height: 1.5;
  white-space: pre-line;
}

.esc-whatsapp-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #25d366;
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 14.5px;
  padding: 12px 22px;
  border-radius: 999px;
  transition: background 0.2s, transform 0.15s;
  white-space: nowrap;
}

.esc-whatsapp-btn:hover {
  background: #1ea952;
  transform: translateY(-1px);
}

@media (max-width: 700px) {
  .esc-whatsapp {
    padding: 0 20px;
  }
  .esc-whatsapp-inner {
    flex-direction: column;
    align-items: flex-start;
  }
  .esc-whatsapp-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
