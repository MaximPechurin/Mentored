<template>
  <div v-if="checking || loading" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else-if="forbidden" class="esc-checking">
    <p>{{ st('course.sinAcceso') }}</p>
  </div>
  <div v-else-if="!lesson" class="esc-checking">
    <p>{{ st('course.sinAcceso') }}</p>
  </div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <router-link :to="`/escuela/curso/${course.slug}`" class="esc-back">← {{ course.title }}</router-link>
          <h1 class="esc-hero-title">{{ lesson.title }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <!-- Шапка материала: N из M, статус, пред/след -->
      <div class="esc-lesson-header">
        <router-link
          v-if="prevLesson"
          :to="`/escuela/curso/${course.slug}/leccion/${prevLesson.id}`"
          class="esc-nav-link"
        >
          {{ st('leccion.anterior') }}
          <span class="esc-nav-title">{{ prevLesson.title }}</span>
        </router-link>
        <span v-else class="esc-nav-spacer"></span>

        <div class="esc-lesson-meta">
          <span class="esc-lesson-counter">{{ lessonIndex + 1 }} {{ st('leccion.deMateriales') }} {{ flatLessons.length }} {{ st('leccion.materiales') }}</span>
          <span class="esc-lesson-state" :class="{ done: lesson.is_completed }">
            {{ lesson.is_completed ? st('leccion.tareaHecha') : st('leccion.tareaPendiente') }}
          </span>
        </div>

        <router-link
          v-if="nextLesson"
          :to="`/escuela/curso/${course.slug}/leccion/${nextLesson.id}`"
          class="esc-nav-link esc-nav-link--next"
        >
          {{ st('leccion.siguiente') }}
          <span class="esc-nav-title">{{ nextLesson.title }}</span>
        </router-link>
        <span v-else class="esc-nav-spacer"></span>
      </div>

      <!-- Тело материала: видео, текст, вложения -->
      <div class="esc-lesson-content-card">
        <div v-if="embedUrl(lesson.video_url)" class="esc-video-wrapper">
          <iframe
            :src="embedUrl(lesson.video_url)"
            frameborder="0"
            allow="autoplay; fullscreen; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
        <a v-else-if="lesson.video_url" :href="lesson.video_url" target="_blank" rel="noopener" class="esc-video-link">
          {{ st('course.verVideo') }}
        </a>

        <p v-if="lesson.content" class="esc-lesson-content">{{ lesson.content }}</p>

        <ul v-if="lesson.materials && lesson.materials.length" class="esc-materials">
          <li v-for="material in lesson.materials" :key="material.id">
            📎 <a :href="material.file" target="_blank" rel="noopener">{{ material.title }}</a>
          </li>
        </ul>

        <button
          class="esc-complete-btn"
          :disabled="savingProgress"
          @click="toggleComplete"
        >
          {{ lesson.is_completed ? st('course.descompletar') : st('course.completar') }}
        </button>
      </div>

      <!-- Задание(я) -->
      <section v-for="a in lesson.assignments" :key="a.id" class="esc-task-block">
        <h2 class="esc-section-title">{{ st('leccion.tarea') }}: {{ a.title }}</h2>

        <div class="esc-task-card">
          <p v-if="detailFor(a.id).description" class="esc-assignment-desc">{{ detailFor(a.id).description }}</p>

          <!-- мой ответ -->
          <div v-if="mySubFor(a.id)" class="esc-answer esc-answer--mine">
            <div class="esc-answer-head">
              <div class="esc-answer-who">
                <span class="esc-answer-avatar">{{ userInitials }}</span>
                <div>
                  <span class="esc-answer-name">{{ st('leccion.tú') }}</span>
                  <span class="esc-answer-date">{{ fmtDate(mySubFor(a.id).submitted_at) }}</span>
                </div>
              </div>
              <span class="esc-sub-status" :class="mySubFor(a.id).status">
                {{ st('statusFull.' + mySubFor(a.id).status) }}
                <template v-if="mySubFor(a.id).score !== null && mySubFor(a.id).score !== undefined">
                  — {{ mySubFor(a.id).score }}/{{ a.max_score }}
                </template>
              </span>
            </div>

            <p v-if="mySubFor(a.id).text" class="esc-answer-text">{{ mySubFor(a.id).text }}</p>
            <p v-if="mySubFor(a.id).file" class="esc-file-name">
              📎 <a :href="mySubFor(a.id).file" target="_blank" rel="noopener">{{ st('teacher.verArchivo') }}</a>
            </p>
            <p v-if="mySubFor(a.id).mentor_comment" class="esc-mentor-comment">
              <strong>{{ st('course.comentarioMentor') }}</strong> {{ mySubFor(a.id).mentor_comment }}
            </p>

            <!-- видимость ответа -->
            <div class="esc-visibility">
              <span class="esc-visibility-state">
                {{ mySubFor(a.id).is_public ? '👁 ' + st('leccion.visibleTodos') : '🔒 ' + st('leccion.soloYo') }}
              </span>
              <button class="esc-visibility-btn" :disabled="savingVisibility" @click="toggleVisibility(a.id)">
                {{ mySubFor(a.id).is_public ? st('leccion.hacerPrivada') : st('leccion.hacerVisible') }}
              </button>
            </div>

            <!-- комментарии к моему ответу -->
            <div v-if="mySubFor(a.id).comments && mySubFor(a.id).comments.length" class="esc-comments">
              <div v-for="c in mySubFor(a.id).comments" :key="c.id" class="esc-comment">
                <span class="esc-comment-author" :class="{ teacher: c.is_teacher }">
                  {{ c.author }}<template v-if="c.is_teacher"> · {{ st('foro.teacher') }}</template>
                </span>
                <span class="esc-comment-date">{{ fmtDate(c.created_at) }}</span>
                <p class="esc-comment-text">{{ c.text }}</p>
              </div>
            </div>
            <div class="esc-comment-form">
              <input
                v-model="commentDrafts['my-' + a.id]"
                type="text"
                :placeholder="st('leccion.comentar')"
                class="esc-comment-input"
                @keyup.enter="sendComment(mySubFor(a.id).id, 'my-' + a.id, a.id)"
              />
              <button class="esc-comment-send" @click="sendComment(mySubFor(a.id).id, 'my-' + a.id, a.id)">
                {{ st('leccion.enviarComentario') }}
              </button>
            </div>
          </div>

          <!-- форма сдачи/пересдачи -->
          <div class="esc-submit-form">
            <div v-if="!mySubFor(a.id)" class="esc-review-label">{{ st('leccion.tuRespuestaTitulo') }}</div>
            <textarea
              v-model="submitDrafts[a.id]"
              rows="4"
              :placeholder="st('course.tuRespuesta')"
              class="esc-textarea"
            ></textarea>
            <input type="file" class="esc-file" @change="onFileChange($event, a.id)" />
            <p v-if="submitFiles[a.id]" class="esc-file-name">📎 {{ submitFiles[a.id].name }}</p>
            <button class="esc-complete-btn" :disabled="submitting" @click="submitAssignment(a)">
              {{ submitting ? st('course.enviando') : (mySubFor(a.id) ? st('course.reenviar') : st('course.enviar')) }}
            </button>
          </div>
        </div>

        <!-- Лента: ответы и комментарии других учеников -->
        <div class="esc-feed">
          <div class="esc-feed-head">
            <h3 class="esc-feed-title">{{ st('leccion.respuestas') }}</h3>
            <button class="esc-feed-sort" @click="toggleSort(a.id)">
              {{ answerSort[a.id] === 'new' ? st('leccion.nuevasPrimero') : st('leccion.viejasPrimero') }} ↕
            </button>
          </div>

          <p v-if="!answersFor(a.id).length" class="esc-muted">{{ st('leccion.sinRespuestas') }}</p>

          <div v-for="ans in answersFor(a.id)" :key="ans.id" class="esc-answer">
            <div class="esc-answer-head">
              <div class="esc-answer-who">
                <span class="esc-answer-avatar">{{ (ans.student || '?').charAt(0).toUpperCase() }}</span>
                <div>
                  <span class="esc-answer-name">{{ ans.is_mine ? st('leccion.tú') : ans.student }}</span>
                  <span class="esc-answer-date">{{ fmtDate(ans.submitted_at) }}</span>
                </div>
              </div>
              <span class="esc-sub-status" :class="ans.status">{{ st('status.' + ans.status) }}</span>
            </div>
            <p v-if="ans.text" class="esc-answer-text">{{ ans.text }}</p>
            <p v-if="ans.file" class="esc-file-name">
              📎 <a :href="ans.file" target="_blank" rel="noopener">{{ st('teacher.verArchivo') }}</a>
            </p>

            <div v-if="ans.comments && ans.comments.length" class="esc-comments">
              <div v-for="c in ans.comments" :key="c.id" class="esc-comment">
                <span class="esc-comment-author" :class="{ teacher: c.is_teacher }">
                  {{ c.author }}<template v-if="c.is_teacher"> · {{ st('foro.teacher') }}</template>
                </span>
                <span class="esc-comment-date">{{ fmtDate(c.created_at) }}</span>
                <p class="esc-comment-text">{{ c.text }}</p>
              </div>
            </div>
            <div class="esc-comment-form">
              <input
                v-model="commentDrafts['ans-' + ans.id]"
                type="text"
                :placeholder="st('leccion.comentar')"
                class="esc-comment-input"
                @keyup.enter="sendFeedComment(ans, a.id)"
              />
              <button class="esc-comment-send" @click="sendFeedComment(ans, a.id)">
                {{ st('leccion.enviarComentario') }}
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st, schoolLang } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ title: '', slug: '', modules: [] })

// задания: детали, мой ответ, лента, черновики
const assignmentDetails = reactive({})   // assignmentId -> {description, ...}
const mySubs = reactive({})              // assignmentId -> submission | null
const answers = reactive({})             // assignmentId -> [ответы ленты]
const answerSort = reactive({})          // assignmentId -> 'old' | 'new'
const submitDrafts = reactive({})
const submitFiles = reactive({})
const commentDrafts = reactive({})

const savingProgress = ref(false)
const savingVisibility = ref(false)
const submitting = ref(false)

// плоский список уроков курса (модули по порядку) - для «N из M» и пред/след
const flatLessons = computed(() =>
  (course.value.modules || []).flatMap((m) => m.lessons || [])
)
const lessonIndex = computed(() =>
  flatLessons.value.findIndex((l) => l.id === Number(route.params.lessonId))
)
const lesson = computed(() =>
  lessonIndex.value >= 0 ? flatLessons.value[lessonIndex.value] : null
)
const prevLesson = computed(() =>
  lessonIndex.value > 0 ? flatLessons.value[lessonIndex.value - 1] : null
)
const nextLesson = computed(() =>
  lessonIndex.value >= 0 && lessonIndex.value < flatLessons.value.length - 1
    ? flatLessons.value[lessonIndex.value + 1]
    : null
)

const userInitials = computed(() => {
  const name = user.value?.full_name || user.value?.username || user.value?.email || '?'
  return name.charAt(0).toUpperCase()
})

const detailFor = (aId) => assignmentDetails[aId] || {}
const mySubFor = (aId) => mySubs[aId] || null
const answersFor = (aId) => answers[aId] || []

const fmtDate = (iso) => {
  if (!iso) return ''
  const locales = { es: 'es-PE', ru: 'ru-RU', en: 'en-US' }
  return new Date(iso).toLocaleDateString(locales[schoolLang.value] || 'es-PE', {
    day: 'numeric', month: 'short', year: 'numeric',
  })
}

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

const toggleComplete = async () => {
  savingProgress.value = true
  try {
    const { data } = await schoolApi.updateLessonProgress(lesson.value.id, {
      is_completed: !lesson.value.is_completed,
    })
    lesson.value.is_completed = data.is_completed
  } catch (error) {
    console.error('Error al guardar el progreso:', error)
  } finally {
    savingProgress.value = false
  }
}

const loadAssignment = async (aId) => {
  try {
    const { data } = await schoolApi.getAssignment(aId)
    assignmentDetails[aId] = data
    mySubs[aId] = data.my_submission
    submitDrafts[aId] = data.my_submission?.text || ''
  } catch (error) {
    console.error('Error al cargar la tarea:', error)
  }
}

const loadAnswers = async (aId) => {
  try {
    const { data } = await schoolApi.assignmentAnswers(aId, answerSort[aId] || 'old')
    answers[aId] = data
  } catch (error) {
    console.error('Error al cargar respuestas:', error)
  }
}

const toggleSort = async (aId) => {
  answerSort[aId] = answerSort[aId] === 'new' ? 'old' : 'new'
  await loadAnswers(aId)
}

const onFileChange = (e, aId) => {
  submitFiles[aId] = e.target.files[0] || null
}

const submitAssignment = async (a) => {
  if (!submitDrafts[a.id] && !submitFiles[a.id]) {
    alert(st('course.adjunta'))
    return
  }
  submitting.value = true
  try {
    const fd = new FormData()
    fd.append('text', submitDrafts[a.id] || '')
    if (submitFiles[a.id]) fd.append('file', submitFiles[a.id])
    await schoolApi.submitAssignment(a.id, fd)
    submitFiles[a.id] = null
    await Promise.all([loadAssignment(a.id), loadAnswers(a.id)])
  } catch (error) {
    console.error('Error al enviar la tarea:', error)
    alert('No se pudo enviar la tarea. Intenta de nuevo.')
  } finally {
    submitting.value = false
  }
}

const toggleVisibility = async (aId) => {
  const sub = mySubs[aId]
  if (!sub) return
  savingVisibility.value = true
  try {
    const { data } = await schoolApi.setSubmissionVisibility(sub.id, !sub.is_public)
    sub.is_public = data.is_public
    await loadAnswers(aId)
  } catch (error) {
    console.error('Error al cambiar visibilidad:', error)
  } finally {
    savingVisibility.value = false
  }
}

const sendComment = async (submissionId, draftKey, aId) => {
  const text = (commentDrafts[draftKey] || '').trim()
  if (!text) return
  try {
    await schoolApi.addSubmissionComment(submissionId, text)
    commentDrafts[draftKey] = ''
    await Promise.all([loadAssignment(aId), loadAnswers(aId)])
  } catch (error) {
    console.error('Error al comentar:', error)
    alert(error.response?.data?.error || 'Error')
  }
}

const sendFeedComment = (ans, aId) => sendComment(ans.id, 'ans-' + ans.id, aId)

const loadLessonData = async () => {
  if (!lesson.value) return
  const ids = (lesson.value.assignments || []).map((a) => a.id)
  await Promise.all(ids.flatMap((id) => [loadAssignment(id), loadAnswers(id)]))
}

// при переходе пред/след меняется только параметр маршрута - курс уже загружен
watch(() => route.params.lessonId, () => { loadLessonData() })

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
    const { data } = await schoolApi.getCourse(route.params.slug)
    course.value = data
    await loadLessonData()
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
.esc-back:hover { text-decoration: underline; }

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

/* --- шапка материала: счётчик, статус, пред/след --- */
.esc-lesson-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 18px 22px;
  margin-bottom: 20px;
}

.esc-nav-link {
  display: flex;
  flex-direction: column;
  gap: 2px;
  color: #8e1519;
  font-weight: 600;
  font-size: 13.5px;
  text-decoration: none;
  max-width: 220px;
}
.esc-nav-link--next { text-align: right; align-items: flex-end; }
.esc-nav-link:hover { text-decoration: underline; }
.esc-nav-title {
  font-weight: 400;
  font-size: 12.5px;
  color: #8a8079;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.esc-nav-spacer { width: 60px; }

.esc-lesson-meta {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-align: center;
}

.esc-lesson-counter { font-size: 13px; color: #8a8079; }

.esc-lesson-state {
  font-size: 13px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  background: #fff4e0;
  color: #9a6a00;
}
.esc-lesson-state.done { background: #e4f3e6; color: #2f7a3a; }

/* --- тело материала --- */
.esc-lesson-content-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 36px;
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
  line-height: 1.7;
  color: #3f3a35;
  margin: 0 0 16px;
  white-space: pre-line;
}

.esc-materials {
  margin: 0 0 18px;
  padding-left: 4px;
  list-style: none;
}
.esc-materials li { margin-bottom: 6px; }
.esc-materials a {
  color: #8e1519;
  text-decoration: none;
  font-weight: 500;
}
.esc-materials a:hover { text-decoration: underline; }

/* --- задание --- */
.esc-task-block { margin-bottom: 40px; }

.esc-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 16px;
  letter-spacing: -0.3px;
}

.esc-task-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 22px 24px;
}

.esc-assignment-desc {
  font-size: 14.5px;
  line-height: 1.6;
  color: #3f3a35;
  margin: 0 0 18px;
  white-space: pre-line;
}

/* --- карточка ответа --- */
.esc-answer {
  border: 1px solid #ece7e1;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 14px;
  background: #ffffff;
}
.esc-answer--mine { background: #faf8f5; }

.esc-answer-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.esc-answer-who { display: flex; align-items: center; gap: 10px; }

.esc-answer-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.esc-answer-name { display: block; font-weight: 600; color: #15110f; font-size: 14.5px; }
.esc-answer-date { display: block; font-size: 12.5px; color: #8a8079; }

.esc-answer-text {
  font-size: 14.5px;
  line-height: 1.6;
  color: #3f3a35;
  margin: 0 0 10px;
  white-space: pre-line;
}

.esc-sub-status {
  display: inline-block;
  font-size: 12.5px;
  font-weight: 600;
  padding: 4px 11px;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
}
.esc-sub-status.submitted { background: #fff4e0; color: #9a6a00; }
.esc-sub-status.reviewed { background: #e4f3e6; color: #2f7a3a; }
.esc-sub-status.needs_revision { background: #fde6e6; color: #a52a2a; }

.esc-mentor-comment {
  font-size: 14px;
  color: #3f3a35;
  background: #f6f3ef;
  border-radius: 10px;
  padding: 10px 14px;
  margin: 0 0 12px;
}

/* --- видимость ответа --- */
.esc-visibility {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  border-top: 1px dashed #ece7e1;
  padding-top: 12px;
  margin-bottom: 12px;
}
.esc-visibility-state { font-size: 13px; color: #6b6259; }
.esc-visibility-btn {
  background: none;
  border: 1px solid #d8d1c8;
  border-radius: 999px;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  color: #6b6259;
  padding: 6px 14px;
  cursor: pointer;
}
.esc-visibility-btn:hover { border-color: #8e1519; color: #8e1519; }
.esc-visibility-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* --- комментарии --- */
.esc-comments {
  border-top: 1px solid #f0ebe5;
  padding-top: 10px;
  margin-bottom: 10px;
}

.esc-comment { padding: 6px 0; }
.esc-comment-author { font-size: 13px; font-weight: 600; color: #15110f; }
.esc-comment-author.teacher { color: #8e1519; }
.esc-comment-date { font-size: 12px; color: #8a8079; margin-left: 8px; }
.esc-comment-text {
  font-size: 14px;
  line-height: 1.55;
  color: #3f3a35;
  margin: 2px 0 0;
  white-space: pre-line;
}

.esc-comment-form { display: flex; gap: 8px; }

.esc-comment-input {
  flex: 1;
  border: 1px solid #e4ddd2;
  border-radius: 999px;
  padding: 9px 16px;
  font-family: inherit;
  font-size: 14px;
  background: #fbf9f6;
  outline: none;
}
.esc-comment-input:focus { border-color: #8e1519; }

.esc-comment-send {
  background: #0e0c0c;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 13px;
  padding: 8px 18px;
  cursor: pointer;
}
.esc-comment-send:hover { background: #2a2525; }

/* --- форма сдачи --- */
.esc-submit-form { border-top: 1px dashed #ece7e1; padding-top: 16px; }

.esc-review-label {
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #8a8079;
  margin-bottom: 8px;
}

.esc-textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e4ddd2;
  border-radius: 10px;
  padding: 12px;
  font-family: inherit;
  font-size: 14.5px;
  color: #15110f;
  background: #fbf9f6;
  outline: none;
  resize: vertical;
  margin-bottom: 10px;
}
.esc-textarea:focus { border-color: #8e1519; }

.esc-file {
  display: block;
  font-size: 13.5px;
  color: #6b6259;
  margin-bottom: 8px;
}

.esc-file-name { font-size: 13.5px; color: #3f3a35; margin: 0 0 12px; }
.esc-file-name a { color: #8e1519; font-weight: 600; text-decoration: none; }
.esc-file-name a:hover { text-decoration: underline; }

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
.esc-complete-btn:hover:not(:disabled) { background: #2a2525; }
.esc-complete-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* --- лента ответов --- */
.esc-feed { margin-top: 22px; }

.esc-feed-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.esc-feed-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
}

.esc-feed-sort {
  background: none;
  border: 1px solid #d8d1c8;
  border-radius: 999px;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  color: #6b6259;
  padding: 6px 14px;
  cursor: pointer;
}
.esc-feed-sort:hover { border-color: #8e1519; color: #8e1519; }

.esc-muted { color: #8a8079; margin: 8px 0; }

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
  .esc-lesson-header { flex-wrap: wrap; }
  .esc-nav-title { display: none; }
}
</style>
