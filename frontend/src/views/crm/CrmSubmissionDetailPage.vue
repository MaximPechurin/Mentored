<template>
  <div class="crm-submission">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando tarea...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmSubmissions' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <template v-else-if="submission">
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmSubmissions' }">Tareas</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ submission.assignment.title }}</span>
      </nav>

      <!-- Хедер -->
      <header class="crm-header-card">
        <div>
          <h1 class="crm-header-name">{{ submission.assignment.title }}</h1>
          <div class="crm-header-meta">
            <span class="badge" :class="statusBadgeClass(submission.status)">
              {{ submission.status_display }}
            </span>
            <span class="crm-meta-item">📅 {{ formatDateTime(submission.submitted_at) }}</span>
            <span v-if="submission.score !== null" class="crm-meta-item crm-meta-item--score">
              ⭐ Nota: {{ submission.score }} / {{ submission.assignment.max_score }}
            </span>
          </div>
        </div>
        <div class="crm-header-actions">
          <a
            :href="`/admin/school/submission/${submission.id}/change/`"
            target="_blank"
            class="crm-btn crm-btn-outline"
          >
            Django admin →
          </a>
        </div>
      </header>

      <!-- Контекст: студент, курс, урок -->
      <div class="crm-context">
        <router-link
          :to="{ name: 'CrmStudentDetail', params: { id: submission.user.id } }"
          class="crm-context-item"
        >
          <span class="crm-context-label">Alumno</span>
          <span class="crm-context-value">{{ submission.user.username }}</span>
          <span class="crm-context-sub">{{ submission.user.email }}</span>
        </router-link>
        <router-link
          :to="{ name: 'CrmCourseDetail', params: { id: submission.course.id } }"
          class="crm-context-item"
        >
          <span class="crm-context-label">Curso</span>
          <span class="crm-context-value">{{ submission.course.title }}</span>
        </router-link>
        <div class="crm-context-item">
          <span class="crm-context-label">Lección</span>
          <span class="crm-context-value">{{ submission.lesson.title }}</span>
        </div>
      </div>

      <!-- Описание задания -->
      <CrmDetailSection title="Descripción del ejercicio">
        <div class="crm-body">{{ submission.assignment.description }}</div>
      </CrmDetailSection>

      <!-- Ответ студента -->
      <CrmDetailSection title="Respuesta del alumno">
        <div v-if="!submission.text && !submission.file_url" class="crm-empty">
          Sin respuesta de texto ni archivos.
        </div>
        <div v-else>
          <div v-if="submission.text" class="crm-body">{{ submission.text }}</div>
          <div v-if="submission.file_url" class="crm-file">
            <a :href="submission.file_url" target="_blank" class="crm-btn crm-btn-outline">
              📎 Abrir archivo adjunto
            </a>
          </div>
        </div>
      </CrmDetailSection>

      <!-- Revisión -->
      <CrmDetailSection title="Revisión">
        <div class="crm-review-form">
          <div class="crm-field">
            <label>Nota (0 - {{ submission.assignment.max_score }})</label>
            <input
              v-model.number="reviewForm.score"
              type="number"
              :min="0"
              :max="submission.assignment.max_score"
              placeholder="Ej. 85"
            >
          </div>
          <div class="crm-field">
            <label>Estado</label>
            <select v-model="reviewForm.status">
              <option value="reviewed">Revisado</option>
              <option value="needs_revision">Revisión</option>
              <option value="submitted">Pendiente</option>
            </select>
          </div>
          <div class="crm-field crm-field--full">
            <label>Comentario para el alumno</label>
            <textarea
              v-model="reviewForm.mentor_comment"
              rows="5"
              placeholder="Escribe tu revisión..."
            ></textarea>
          </div>

          <div class="crm-field crm-field--full">
            <div class="crm-info-note">
              ℹ️ El guardado estará disponible próximamente. Mientras tanto puedes escribir tu revisión y copiarla.
            </div>
          </div>

          <div class="crm-field crm-field--full crm-field--actions">
            <button class="crm-btn crm-btn-primary" disabled>
              Guardar revisión
            </button>
            <span class="crm-hint">Función en desarrollo</span>
          </div>
        </div>

        <div v-if="submission.reviewed_by" class="crm-reviewed-info">
          Revisado por <strong>{{ submission.reviewed_by.name }}</strong>
          <span v-if="submission.reviewed_at">
            · {{ formatDateTime(submission.reviewed_at) }}
          </span>
        </div>
      </CrmDetailSection>

      <!-- Comentarios -->
      <CrmDetailSection title="Comentarios" :count="submission.comments.length">
        <div v-if="submission.comments.length === 0" class="crm-empty">
          Sin comentarios todavía.
        </div>
        <ul v-else class="crm-comments">
          <li v-for="c in submission.comments" :key="c.id" class="crm-comment">
            <div class="crm-comment-head">
              <strong>{{ c.author_name }}</strong>
              <span class="muted">{{ formatDateTime(c.created_at) }}</span>
            </div>
            <div class="crm-comment-body">{{ c.text }}</div>
          </li>
        </ul>
      </CrmDetailSection>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { crmApi } from '../../api/crm'
import CrmDetailSection from './CrmDetailSection.vue'

const route = useRoute()

const loading = ref(true)
const error = ref(null)
const submission = ref(null)

const reviewForm = ref({
  score: null,
  status: 'reviewed',
  mentor_comment: '',
})

const loadSubmission = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getSubmission(route.params.id)
    submission.value = res.data
    // предзаполняем форму существующими данными (если есть)
    reviewForm.value.score = res.data.score
    reviewForm.value.status = res.data.status
    reviewForm.value.mentor_comment = res.data.mentor_comment || ''
  } catch (e) {
    console.error('Error loading submission:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la tarea.'
  } finally {
    loading.value = false
  }
}

const formatDateTime = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const statusBadgeClass = (status) => {
  if (status === 'reviewed') return 'badge-success'
  if (status === 'needs_revision') return 'badge-danger'
  return 'badge-warn'
}

onMounted(loadSubmission)
</script>

<style scoped>
.crm-loading,
.crm-error {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; min-height: 300px;
  color: #8a8079; text-align: center;
}
.crm-loading-spinner {
  width: 48px; height: 48px;
  border: 4px solid #e4ddd2; border-top: 4px solid #8e1519;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.crm-error h2 { font-family: 'Playfair Display', serif; color: #15110f; }

.crm-breadcrumb { font-size: 14px; color: #8a8079; margin-bottom: 12px; }
.crm-breadcrumb a { color: #8e1519; text-decoration: none; }
.crm-breadcrumb-sep { margin: 0 8px; color: #c9bca6; }
.crm-breadcrumb-current { color: #15110f; }

.crm-header-card {
  display: flex; justify-content: space-between; gap: 24px; flex-wrap: wrap;
  background: #fff; border: 1px solid #ece7e1; border-radius: 16px;
  padding: 24px; margin-bottom: 20px;
}
.crm-header-name {
  font-family: 'Playfair Display', serif;
  font-size: 24px; font-weight: 600; color: #15110f;
  margin: 0 0 12px;
}
.crm-header-meta {
  display: flex; gap: 14px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c; align-items: center;
}
.crm-meta-item { color: #6f655c; }
.crm-meta-item--score { color: #1f7a3d; font-weight: 600; }
.crm-header-actions { display: flex; gap: 10px; flex-wrap: wrap; }

/* Контекст */
.crm-context {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}
.crm-context-item {
  display: flex; flex-direction: column; gap: 4px;
  background: #fff; border: 1px solid #ece7e1; border-radius: 14px;
  padding: 16px 20px;
  text-decoration: none; color: inherit;
  transition: border-color 0.2s, transform 0.2s;
}
a.crm-context-item:hover {
  border-color: #8e1519;
  transform: translateY(-1px);
}
.crm-context-label {
  font-size: 11.5px; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase; color: #8a8079;
}
.crm-context-value {
  font-family: 'Playfair Display', serif;
  font-size: 17px; font-weight: 600; color: #15110f;
}
.crm-context-sub { font-size: 12.5px; color: #8a8079; }

/* Тело */
.crm-body {
  padding: 20px 24px;
  font-size: 15px; line-height: 1.7; color: #3a342e;
  white-space: pre-line;
}
.crm-file {
  padding: 0 24px 20px;
}

/* Форма ревью */
.crm-review-form {
  padding: 20px 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.crm-field { display: flex; flex-direction: column; gap: 6px; }
.crm-field--full { grid-column: 1 / -1; }
.crm-field label {
  font-size: 12px; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase; color: #8a8079;
}
.crm-field input,
.crm-field select,
.crm-field textarea {
  border: 1px solid #ece7e1; background: #faf6f0;
  border-radius: 10px; padding: 10px 14px;
  font-family: inherit; font-size: 14.5px; color: #15110f;
  outline: none; transition: border-color 0.2s;
}
.crm-field input:focus,
.crm-field select:focus,
.crm-field textarea:focus {
  border-color: #8e1519;
}
.crm-field textarea { resize: vertical; min-height: 100px; }

.crm-field--actions {
  flex-direction: row; align-items: center; gap: 14px;
}
.crm-info-note {
  font-size: 13.5px; color: #8c6a10;
  background: #fff5e0; border-radius: 8px;
  padding: 10px 14px;
}
.crm-hint { font-size: 13px; color: #a59c93; }

.crm-reviewed-info {
  padding: 0 24px 20px;
  font-size: 14px; color: #6f655c;
}

.crm-btn {
  display: inline-flex; align-items: center; gap: 6px;
  text-decoration: none; font-family: inherit; font-size: 14px;
  font-weight: 600; padding: 9px 16px; border-radius: 999px;
  cursor: pointer; transition: all 0.2s;
  border: 1.5px solid transparent;
}
.crm-btn-outline {
  background: #fff; border-color: #ece7e1; color: #5d544c;
}
.crm-btn-outline:hover { border-color: #8e1519; color: #8e1519; }
.crm-btn-primary {
  background: #8e1519; border-color: #8e1519; color: #fff;
}
.crm-btn-primary:disabled {
  opacity: 0.5; cursor: not-allowed;
}

/* Комментарии */
.crm-comments {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column;
}
.crm-comment {
  padding: 16px 24px;
  border-bottom: 1px solid #f5f0e8;
}
.crm-comment:last-child { border-bottom: none; }
.crm-comment-head {
  display: flex; gap: 12px; align-items: baseline;
  margin-bottom: 8px;
}
.crm-comment-head strong { color: #15110f; }
.crm-comment-body {
  font-size: 14.5px; line-height: 1.6; color: #3a342e;
  white-space: pre-line;
}

.badge {
  display: inline-block; font-size: 11.5px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-warn { background: #fff5e0; color: #8c6a10; }

.muted { color: #a59c93; font-size: 13.5px; }
.crm-empty {
  color: #a59c93; font-size: 15px;
  padding: 32px 24px; text-align: center;
}
</style>