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
          <h1 class="esc-hero-title">{{ course.title }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <!-- Название/описание курса -->
      <section class="esc-block">
        <div class="esc-section-header">
          <h2 class="esc-section-title">{{ st('teacher.datosCurso') }}</h2>
          <button v-if="!editingCourseInfo" class="esc-edit-btn" @click="startEditCourseInfo">
            {{ st('teacher.editar') }}
          </button>
        </div>

        <div v-if="!editingCourseInfo" class="esc-info-card">
          <p v-if="course.description" class="esc-info-desc">{{ course.description }}</p>
          <p v-else class="esc-muted">{{ st('teacher.sinDescripcion') }}</p>
        </div>

        <div v-else class="esc-info-card">
          <input v-model="courseTitleDraft" type="text" class="esc-input" :placeholder="st('teacher.nombreCurso')" />
          <textarea v-model="courseDescriptionDraft" rows="3" class="esc-textarea" :placeholder="st('teacher.descripcionCurso')"></textarea>
          <div class="esc-form-actions">
            <button class="esc-btn-approve" :disabled="savingCourseInfo" @click="saveCourseInfo">
              {{ savingCourseInfo ? st('teacher.guardando') : st('teacher.guardar') }}
            </button>
            <button class="esc-btn-return" @click="editingCourseInfo = false">{{ st('teacher.cancelar') }}</button>
          </div>
        </div>
      </section>

      <!-- Уроки -->
      <section class="esc-block">
        <div class="esc-section-header">
          <h2 class="esc-section-title">{{ st('teacher.lecciones') }}</h2>
          <button class="esc-create-course-btn" @click="lessonFormMode === 'new' ? closeLessonForm() : openNewLessonForm()">
            {{ lessonFormMode === 'new' ? st('teacher.cancelar') : st('teacher.anadirLeccion') }}
          </button>
        </div>

        <!-- форма добавления нового урока -->
        <div v-if="lessonFormMode === 'new'" class="esc-lesson-form">
          <LessonFormFields
            :form="lessonForm"
            :st="st"
            @video-file-change="onLessonVideoFileChange"
          />
          <p v-if="lessonFormError" class="esc-create-course-error">{{ lessonFormError }}</p>
          <div class="esc-form-actions">
            <button class="esc-btn-approve" :disabled="savingLessonForm" @click="submitLessonForm">
              {{ savingLessonForm ? st('teacher.guardando') : st('teacher.anadir') }}
            </button>
            <button class="esc-btn-return" @click="closeLessonForm">{{ st('teacher.cancelar') }}</button>
          </div>
        </div>

        <p v-if="lessons.length === 0 && lessonFormMode !== 'new'" class="esc-muted">{{ st('teacher.sinLecciones') }}</p>

        <div v-else class="esc-course-list">
          <div v-for="lesson in lessons" :key="lesson.id" class="esc-course-card">
            <button class="esc-course-head" @click="toggleLesson(lesson.id)">
              <span class="esc-course-title">{{ lesson.title }}</span>
              <span class="esc-course-meta">
                <span v-if="lesson.video_file || lesson.video_url">🎥</span>
                <span v-if="lesson.assignments && lesson.assignments.length">📝 {{ lesson.assignments.length }}</span>
                <span v-if="lesson.duration_minutes">{{ lesson.duration_minutes }} {{ st('course.min') }}</span>
              </span>
            </button>

            <div v-if="activeLessonId === lesson.id" class="esc-roster">
              <!-- редактирование урока -->
              <div v-if="lessonFormMode === lesson.id" class="esc-lesson-form">
                <LessonFormFields
                  :form="lessonForm"
                  :st="st"
                  @video-file-change="onLessonVideoFileChange"
                />
                <p v-if="lessonFormError" class="esc-create-course-error">{{ lessonFormError }}</p>
                <div class="esc-form-actions">
                  <button class="esc-btn-approve" :disabled="savingLessonForm" @click="submitLessonForm">
                    {{ savingLessonForm ? st('teacher.guardando') : st('teacher.guardar') }}
                  </button>
                  <button class="esc-btn-return" @click="closeLessonForm">{{ st('teacher.cancelar') }}</button>
                </div>
              </div>
              <template v-else>
                <button class="esc-edit-btn" @click="openEditLessonForm(lesson)">{{ st('teacher.editarLeccion') }}</button>

                <div
                  v-if="lesson.content && isHtmlContent(lesson.content)"
                  class="esc-lesson-content-preview esc-lesson-content-preview--rich"
                  v-html="sanitizeLessonHtml(lesson.content)"
                ></div>
                <p v-else-if="lesson.content" class="esc-lesson-content-preview">{{ lesson.content }}</p>

                <!-- задания урока -->
                <div class="esc-assignments-block">
                  <h3 class="esc-assignments-title">{{ st('teacher.tareas') }}</h3>

                  <div v-for="a in lesson.assignments" :key="a.id" class="esc-assignment-row">
                    <template v-if="assignmentFormMode && assignmentFormMode.assignmentId === a.id">
                      <AssignmentFormFields :form="assignmentForm" :st="st" />
                      <p v-if="assignmentFormError" class="esc-create-course-error">{{ assignmentFormError }}</p>
                      <div class="esc-form-actions">
                        <button class="esc-btn-approve" :disabled="savingAssignmentForm" @click="submitAssignmentForm">
                          {{ savingAssignmentForm ? st('teacher.guardando') : st('teacher.guardar') }}
                        </button>
                        <button class="esc-btn-return" @click="closeAssignmentForm">{{ st('teacher.cancelar') }}</button>
                      </div>
                    </template>
                    <template v-else>
                      <span class="esc-assignment-title">{{ a.title }}</span>
                      <span class="esc-required-badge" :class="{ optional: !a.is_required }">
                        {{ a.is_required ? st('teacher.obligatoria') : st('teacher.opcional') }}
                      </span>
                      <button class="esc-edit-btn esc-edit-btn--small" @click="openEditAssignmentForm(lesson.id, a)">
                        {{ st('teacher.editar') }}
                      </button>
                      <button class="esc-edit-btn esc-edit-btn--small" @click="toggleAssignmentRequired(a)">
                        {{ a.is_required ? st('teacher.hacerOpcional') : st('teacher.hacerObligatoria') }}
                      </button>
                    </template>
                  </div>

                  <div v-if="assignmentFormMode && assignmentFormMode.lessonId === lesson.id && !assignmentFormMode.assignmentId" class="esc-assignment-row esc-assignment-row--new">
                    <AssignmentFormFields :form="assignmentForm" :st="st" />
                    <p v-if="assignmentFormError" class="esc-create-course-error">{{ assignmentFormError }}</p>
                    <div class="esc-form-actions">
                      <button class="esc-btn-approve" :disabled="savingAssignmentForm" @click="submitAssignmentForm">
                        {{ savingAssignmentForm ? st('teacher.guardando') : st('teacher.anadir') }}
                      </button>
                      <button class="esc-btn-return" @click="closeAssignmentForm">{{ st('teacher.cancelar') }}</button>
                    </div>
                  </div>
                  <button
                    v-else
                    class="esc-create-course-btn esc-create-course-btn--small"
                    @click="openNewAssignmentForm(lesson.id)"
                  >
                    {{ st('teacher.anadirTarea') }}
                  </button>
                </div>

                <!-- материалы урока (PDF и т.п.) -->
                <div class="esc-assignments-block">
                  <h3 class="esc-assignments-title">{{ st('teacher.materiales') }}</h3>

                  <p v-if="!lesson.materials || !lesson.materials.length" class="esc-muted">
                    {{ st('teacher.sinMateriales') }}
                  </p>
                  <div v-for="m in lesson.materials" :key="m.id" class="esc-assignment-row">
                    <a :href="m.file" target="_blank" rel="noopener" class="esc-assignment-title">📎 {{ m.title }}</a>
                    <button class="esc-edit-btn esc-edit-btn--small" @click="deleteMaterial(m.id)">
                      {{ st('teacher.eliminar') }}
                    </button>
                  </div>

                  <div v-if="materialFormLessonId === lesson.id" class="esc-assignment-row esc-assignment-row--new">
                    <input v-model="materialForm.title" type="text" class="esc-input" :placeholder="st('teacher.nombreMaterial')" />
                    <input type="file" class="esc-file" @change="onMaterialFileChange" />
                    <p v-if="materialFormError" class="esc-create-course-error">{{ materialFormError }}</p>
                    <div class="esc-form-actions">
                      <button class="esc-btn-approve" :disabled="savingMaterialForm" @click="submitMaterialForm(lesson.id)">
                        {{ savingMaterialForm ? st('teacher.guardando') : st('teacher.anadir') }}
                      </button>
                      <button class="esc-btn-return" @click="closeMaterialForm">{{ st('teacher.cancelar') }}</button>
                    </div>
                  </div>
                  <button
                    v-else
                    class="esc-create-course-btn esc-create-course-btn--small"
                    @click="openNewMaterialForm(lesson.id)"
                  >
                    {{ st('teacher.anadirMaterial') }}
                  </button>
                </div>
              </template>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'
import LessonFormFields from './components/LessonFormFields.vue'
import AssignmentFormFields from './components/AssignmentFormFields.vue'
import { isHtmlContent, sanitizeLessonHtml } from '../../composables/useLessonContent'


const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const checking = ref(true)
const loading = ref(true)
const forbidden = ref(false)
const course = ref({ id: null, title: '', description: '', modules: [] })
const lessons = computed(() => course.value.modules.flatMap((m) => m.lessons || []))

const activeLessonId = ref(null)
const toggleLesson = (id) => {
  activeLessonId.value = activeLessonId.value === id ? null : id
  closeLessonForm()
  closeAssignmentForm()
  closeMaterialForm()
}

// --- название/описание курса ---
const editingCourseInfo = ref(false)
const courseTitleDraft = ref('')
const courseDescriptionDraft = ref('')
const savingCourseInfo = ref(false)

const startEditCourseInfo = () => {
  courseTitleDraft.value = course.value.title
  courseDescriptionDraft.value = course.value.description
  editingCourseInfo.value = true
}
const saveCourseInfo = async () => {
  if (!courseTitleDraft.value.trim()) return
  savingCourseInfo.value = true
  try {
    await schoolApi.updateTeacherCourse(course.value.id, {
      title: courseTitleDraft.value.trim(),
      description: courseDescriptionDraft.value.trim(),
    })
    course.value.title = courseTitleDraft.value.trim()
    course.value.description = courseDescriptionDraft.value.trim()
    editingCourseInfo.value = false
  } catch (error) {
    console.error('Error al actualizar el curso:', error)
    alert(error.response?.data?.error || 'Error al actualizar el curso.')
  } finally {
    savingCourseInfo.value = false
  }
}

// --- форма урока (общая для создания и редактирования) ---
const lessonFormMode = ref(null) // null | 'new' | <lessonId>
const lessonForm = reactive({ title: '', content: '', duration_minutes: '', videoMode: 'file', videoFile: null, videoUrl: '' })
const savingLessonForm = ref(false)
const lessonFormError = ref('')

const resetLessonForm = () => Object.assign(lessonForm, {
  title: '', content: '', duration_minutes: '', videoMode: 'file', videoFile: null, videoUrl: '',
})
const openNewLessonForm = () => {
  resetLessonForm()
  lessonFormMode.value = 'new'
  lessonFormError.value = ''
}
const openEditLessonForm = (lesson) => {
  Object.assign(lessonForm, {
    title: lesson.title,
    content: lesson.content || '',
    duration_minutes: lesson.duration_minutes || '',
    videoMode: (!lesson.video_file && lesson.video_url) ? 'url' : 'file',
    videoFile: null,
    videoUrl: lesson.video_url || '',
  })
  lessonFormMode.value = lesson.id
  lessonFormError.value = ''
}
const closeLessonForm = () => { lessonFormMode.value = null }
const onLessonVideoFileChange = (e) => { lessonForm.videoFile = e.target.files[0] || null }

const submitLessonForm = async () => {
  if (!lessonForm.title.trim()) {
    lessonFormError.value = st('teacher.nombreRequerido')
    return
  }
  savingLessonForm.value = true
  lessonFormError.value = ''
  try {
    const fd = new FormData()
    fd.append('title', lessonForm.title.trim())
    fd.append('content', lessonForm.content || '')
    if (lessonForm.duration_minutes) fd.append('duration_minutes', lessonForm.duration_minutes)
    if (lessonForm.videoMode === 'file' && lessonForm.videoFile) {
      fd.append('video_file', lessonForm.videoFile)
    } else if (lessonForm.videoMode === 'url') {
      fd.append('video_url', lessonForm.videoUrl || '')
    }
    if (lessonFormMode.value === 'new') {
      await schoolApi.createTeacherLesson(course.value.id, fd)
    } else {
      await schoolApi.updateTeacherLesson(lessonFormMode.value, fd)
    }
    await loadCourse()
    closeLessonForm()
  } catch (error) {
    console.error('Error al guardar la lección:', error)
    lessonFormError.value = error.response?.data?.error || 'Error al guardar la lección.'
  } finally {
    savingLessonForm.value = false
  }
}

// --- форма задания (общая для создания и редактирования) ---
const assignmentFormMode = ref(null) // null | { lessonId, assignmentId }
const assignmentForm = reactive({ title: '', description: '', max_score: 100, is_required: true })
const savingAssignmentForm = ref(false)
const assignmentFormError = ref('')

const openNewAssignmentForm = (lessonId) => {
  Object.assign(assignmentForm, { title: '', description: '', max_score: 100, is_required: true })
  assignmentFormMode.value = { lessonId, assignmentId: null }
  assignmentFormError.value = ''
}
const openEditAssignmentForm = (lessonId, a) => {
  Object.assign(assignmentForm, {
    title: a.title, description: a.description || '', max_score: a.max_score, is_required: a.is_required,
  })
  assignmentFormMode.value = { lessonId, assignmentId: a.id }
  assignmentFormError.value = ''
}
const closeAssignmentForm = () => { assignmentFormMode.value = null }

const submitAssignmentForm = async () => {
  if (!assignmentForm.title.trim()) {
    assignmentFormError.value = st('teacher.nombreRequerido')
    return
  }
  savingAssignmentForm.value = true
  assignmentFormError.value = ''
  try {
    const payload = {
      title: assignmentForm.title.trim(),
      description: assignmentForm.description || '',
      max_score: assignmentForm.max_score || 100,
      is_required: assignmentForm.is_required,
    }
    if (assignmentFormMode.value.assignmentId) {
      await schoolApi.updateTeacherAssignment(assignmentFormMode.value.assignmentId, payload)
    } else {
      await schoolApi.createTeacherAssignment(assignmentFormMode.value.lessonId, payload)
    }
    await loadCourse()
    closeAssignmentForm()
  } catch (error) {
    console.error('Error al guardar la tarea:', error)
    assignmentFormError.value = error.response?.data?.error || 'Error al guardar la tarea.'
  } finally {
    savingAssignmentForm.value = false
  }
}

const toggleAssignmentRequired = async (a) => {
  try {
    await schoolApi.updateTeacherAssignment(a.id, { is_required: !a.is_required })
    await loadCourse()
  } catch (error) {
    console.error('Error al cambiar la obligatoriedad:', error)
  }
}

// --- материалы урока (PDF и т.п.) ---
const materialFormLessonId = ref(null)
const materialForm = reactive({ title: '', file: null })
const savingMaterialForm = ref(false)
const materialFormError = ref('')

const openNewMaterialForm = (lessonId) => {
  Object.assign(materialForm, { title: '', file: null })
  materialFormLessonId.value = lessonId
  materialFormError.value = ''
}
const closeMaterialForm = () => { materialFormLessonId.value = null }
const onMaterialFileChange = (e) => { materialForm.file = e.target.files[0] || null }

const submitMaterialForm = async (lessonId) => {
  if (!materialForm.title.trim() || !materialForm.file) {
    materialFormError.value = st('teacher.nombreRequerido')
    return
  }
  savingMaterialForm.value = true
  materialFormError.value = ''
  try {
    const fd = new FormData()
    fd.append('title', materialForm.title.trim())
    fd.append('file', materialForm.file)
    await schoolApi.createTeacherMaterial(lessonId, fd)
    await loadCourse()
    closeMaterialForm()
  } catch (error) {
    console.error('Error al guardar el material:', error)
    materialFormError.value = error.response?.data?.error || 'Error al guardar el material.'
  } finally {
    savingMaterialForm.value = false
  }
}

const deleteMaterial = async (materialId) => {
  try {
    await schoolApi.deleteTeacherMaterial(materialId)
    await loadCourse()
  } catch (error) {
    console.error('Error al eliminar el material:', error)
  }
}

const loadCourse = async () => {
  try {
    const { data } = await schoolApi.teacherCourseEdit(route.params.courseId)
    course.value = data
  } catch (error) {
    if (error.response?.status === 403 || error.response?.status === 404) {
      forbidden.value = true
    } else {
      console.error('Error al cargar el curso:', error)
    }
  }
}

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  const fresh = await refreshUser()
  const roles = fresh?.roles ?? user.value?.roles ?? []
  if (!roles.includes('teacher')) {
    router.replace('/cuenta')
    return
  }

  checking.value = false
  await loadCourse()
  loading.value = false
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

.esc-hero { background: #0e0c0c; padding: 52px 32px; }
.esc-hero-container { max-width: 900px; margin: 0 auto; }

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

.esc-shell { max-width: 900px; margin: 0 auto; padding: 40px 32px 88px; }
.esc-block + .esc-block { margin-top: 40px; }

.esc-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.esc-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
  letter-spacing: -0.3px;
}

.esc-edit-btn {
  background: none;
  border: 1px solid #d8d1c8;
  border-radius: 999px;
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: #6b6259;
  padding: 7px 16px;
  cursor: pointer;
}
.esc-edit-btn:hover { border-color: #8e1519; color: #8e1519; }
.esc-edit-btn--small { padding: 5px 12px; font-size: 12.5px; }

.esc-create-course-btn {
  flex-shrink: 0;
  background: #0e0c0c;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 20px;
  cursor: pointer;
}
.esc-create-course-btn:hover { background: #2a2525; }
.esc-create-course-btn--small { padding: 7px 16px; font-size: 13px; margin-top: 10px; }

.esc-info-card, .esc-lesson-form {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 22px 24px;
}

.esc-info-desc { font-size: 15px; line-height: 1.6; color: #3f3a35; margin: 0; white-space: pre-line; }
.esc-muted { color: #8a8079; margin: 0; }

.esc-input, .esc-textarea {
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
  margin-bottom: 12px;
}
.esc-input--short { width: 160px; }
.esc-textarea { resize: vertical; }
.esc-input:focus, .esc-textarea:focus { border-color: #8e1519; }

.esc-form-actions { display: flex; gap: 10px; flex-wrap: wrap; }

.esc-btn-approve, .esc-btn-return {
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 20px;
  cursor: pointer;
}
.esc-btn-approve { background: #2f7a3a; color: #fff; }
.esc-btn-return { background: #fff; color: #a52a2a; border: 1px solid #e2b8b8; }
.esc-btn-approve:disabled, .esc-btn-return:disabled { opacity: 0.6; cursor: not-allowed; }

.esc-create-course-error { color: #8e1519; font-size: 13.5px; margin: 0 0 12px; }

/* --- список уроков (переиспользуем визуал карточек кабинета препода) --- */
.esc-course-list { display: flex; flex-direction: column; gap: 14px; }

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
  padding: 18px 22px;
}

.esc-course-title { font-weight: 600; color: #15110f; }

.esc-course-meta {
  font-size: 13.5px;
  color: #8a8079;
  display: flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
}

.esc-roster { border-top: 1px solid #ece7e1; padding: 18px 22px 22px; }

.esc-lesson-content-preview {
  font-size: 14.5px;
  line-height: 1.6;
  color: #3f3a35;
  margin: 12px 0;
  white-space: pre-line;
}
.esc-lesson-content-preview--rich { white-space: normal; }
.esc-lesson-content-preview--rich :deep(img) { max-width: 100%; height: auto; border-radius: 8px; margin: 6px 0; }
.esc-lesson-content-preview--rich :deep(ul),
.esc-lesson-content-preview--rich :deep(ol) { padding-left: 22px; }

.esc-video-mode { display: flex; gap: 18px; margin-bottom: 12px; font-size: 14px; color: #3f3a35; }
.esc-video-mode label { display: flex; align-items: center; gap: 6px; cursor: pointer; }

.esc-file { display: block; font-size: 13.5px; color: #6b6259; margin-bottom: 12px; }

/* --- задания --- */
.esc-assignments-block { margin-top: 16px; border-top: 1px dashed #ece7e1; padding-top: 16px; }

.esc-assignments-title {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #8a8079;
  margin: 0 0 12px;
}

.esc-assignment-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 10px 0;
  border-bottom: 1px solid #f0ebe5;
}
.esc-assignment-row--new { flex-direction: column; align-items: stretch; border-bottom: none; }

.esc-assignment-title { font-size: 14.5px; color: #15110f; flex: 1; min-width: 120px; }

.esc-required-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  background: #fff4e0;
  color: #9a6a00;
}
.esc-required-badge.optional { background: #eef1ec; color: #5a6b52; }

.esc-required-toggle { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #3f3a35; margin-bottom: 12px; }

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
