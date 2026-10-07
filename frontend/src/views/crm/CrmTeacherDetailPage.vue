<template>
  <div class="crm-teacher">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando profesor...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmTeachers' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <template v-else-if="teacher">
      <!-- Хлебные крошки -->
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmTeachers' }">Profesores</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ teacher.username }}</span>
      </nav>

      <!-- Хедер -->
      <header class="crm-header-card">
        <div class="crm-header-main">
          <div class="crm-avatar-lg">
            <img v-if="avatarUrl" :src="avatarUrl" :alt="teacher.username">
            <span v-else>{{ teacher.username.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="crm-header-info">
            <h1 class="crm-header-name">{{ teacher.username }}</h1>
            <div v-if="teacher.profile?.specialization" class="crm-header-spec">
              {{ teacher.profile.specialization }}
            </div>
            <div class="crm-header-meta">
              <a :href="`mailto:${teacher.email}`" class="crm-meta-item">
                ✉ {{ teacher.email }}
              </a>
              <span v-if="teacher.phone" class="crm-meta-item">
                📞 {{ teacher.phone }}
              </span>
              <span class="crm-meta-item">
                📅 Registro: {{ formatDate(teacher.created_at) }}
              </span>
              <span v-if="teacher.last_login" class="crm-meta-item">
                🕐 Último login: {{ formatDate(teacher.last_login) }}
              </span>
            </div>
            <div class="crm-header-roles">
              <span class="badge" :class="teacher.is_active ? 'badge-success' : 'badge-muted'">
                {{ teacher.is_active ? 'Activo' : 'Inactivo' }}
              </span>
              <span
                v-for="r in teacher.roles"
                :key="r"
                class="role-tag"
                :class="`role-${r}`"
              >{{ r }}</span>
              <span v-if="teacher.profile?.is_public" class="badge badge-gold">
                Público
              </span>
            </div>
          </div>
        </div>
        <div class="crm-header-actions">
          <a :href="`mailto:${teacher.email}`" class="crm-btn crm-btn-outline">
            ✉ Enviar email
          </a>
          <a
            :href="`/admin/mentored/user/${teacher.id}/change/`"
            target="_blank"
            class="crm-btn crm-btn-outline"
          >
            Django admin →
          </a>
        </div>
      </header>

      <!-- Bio -->
      <CrmDetailSection v-if="teacher.profile?.bio" title="Sobre el profesor">
        <div class="crm-bio">{{ teacher.profile.bio }}</div>
      </CrmDetailSection>

      <!-- Stats -->
      <div class="crm-stats">
        <div class="crm-stat">
          <span class="crm-stat-label">Cursos</span>
          <span class="crm-stat-value">{{ teacher.stats.courses_count }}</span>
          <span class="crm-stat-sub">asignados</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Alumnos</span>
          <span class="crm-stat-value">{{ teacher.stats.students_count }}</span>
          <span class="crm-stat-sub">únicos</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Grupos</span>
          <span class="crm-stat-value">{{ teacher.stats.groups_count }}</span>
          <span class="crm-stat-sub">cursos activos</span>
        </div>
      </div>

      <!-- Cursos asignados -->
      <CrmDetailSection title="Cursos asignados" :count="teacher.courses.length">
        <div v-if="teacher.courses.length === 0" class="crm-empty">
          Este profesor no tiene cursos asignados.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Curso</th>
              <th class="align-center">Estado</th>
              <th class="align-center">Alumnos</th>
              <th>Progreso medio</th>
              <th class="align-right">Asignado</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in teacher.courses"
              :key="c.course_id"
              class="clickable"
              @click="goToCourse(c.course_id)"
            >
              <td>
                <div class="crm-course-name">{{ c.course_title }}</div>
                <div class="crm-course-slug">{{ c.course_slug }}</div>
              </td>
              <td class="align-center">
                <span class="badge" :class="c.is_active ? 'badge-success' : 'badge-muted'">
                  {{ c.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="align-center">
                <span class="cell-count">{{ c.students_count }}</span>
              </td>
              <td>
                <CrmProgressBar :percent="c.avg_progress" style="min-width: 140px" />
              </td>
              <td class="align-right muted">{{ formatDate(c.assigned_at) }}</td>
            </tr>
          </tbody>
        </table>
      </CrmDetailSection>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { crmApi } from '../../api/crm'
import CrmDetailSection from './CrmDetailSection.vue'
import CrmProgressBar from './CrmProgressBar.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const teacher = ref(null)

const avatarUrl = computed(() => {
  if (!teacher.value) return null
  return teacher.value.profile?.photo || teacher.value.avatar || null
})

const loadTeacher = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getTeacher(route.params.id)
    teacher.value = res.data
  } catch (e) {
    console.error('Error loading teacher:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la información del profesor.'
  } finally {
    loading.value = false
  }
}

const goToCourse = (id) => {
  router.push({ name: 'CrmCourseDetail', params: { id } })
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

onMounted(loadTeacher)
</script>

<style scoped>
/* ===== Загрузка / ошибка ===== */
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

/* ===== Хлебные крошки ===== */
.crm-breadcrumb { font-size: 14px; color: #8a8079; margin-bottom: 12px; }
.crm-breadcrumb a { color: #8e1519; text-decoration: none; }
.crm-breadcrumb-sep { margin: 0 8px; color: #c9bca6; }
.crm-breadcrumb-current { color: #15110f; }

/* ===== Хедер ===== */
.crm-header-card {
  display: flex; justify-content: space-between; gap: 24px; flex-wrap: wrap;
  background: #fff; border: 1px solid #ece7e1; border-radius: 16px;
  padding: 24px; margin-bottom: 20px;
}
.crm-header-main {
  display: flex; align-items: center; gap: 20px;
  flex: 1; min-width: 0;
}
.crm-avatar-lg {
  width: 80px; height: 80px; border-radius: 50%;
  background: #8e1519; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 32px; font-weight: 600;
  overflow: hidden; flex-shrink: 0;
}
.crm-avatar-lg img { width: 100%; height: 100%; object-fit: cover; }
.crm-header-name {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600; color: #15110f;
  margin: 0 0 4px;
}
.crm-header-spec {
  font-size: 15px; color: #8e1519;
  font-weight: 500; margin-bottom: 8px;
}
.crm-header-meta {
  display: flex; gap: 16px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c; margin-bottom: 10px;
}
.crm-meta-item { color: #6f655c; text-decoration: none; }
a.crm-meta-item:hover { color: #8e1519; }
.crm-header-roles { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.crm-header-actions { display: flex; gap: 10px; flex-wrap: wrap; }

/* ===== Кнопки ===== */
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

/* ===== Bio ===== */
.crm-bio {
  padding: 20px 24px;
  font-size: 15px; line-height: 1.7;
  color: #3a342e;
  white-space: pre-line;
}

/* ===== Stats ===== */
.crm-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px; margin-bottom: 24px;
}
.crm-stat {
  background: #fff; border: 1px solid #ece7e1; border-radius: 14px;
  padding: 18px 20px; display: flex; flex-direction: column; gap: 6px;
}
.crm-stat-label {
  font-size: 12px; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase; color: #8a8079;
}
.crm-stat-value {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600; color: #15110f; line-height: 1.1;
}
.crm-stat-sub { font-size: 13px; color: #a59c93; }

/* ===== Внутренняя таблица ===== */
.crm-table-inner { width: 100%; border-collapse: collapse; font-size: 14.5px; }
.crm-table-inner th {
  text-align: left; font-size: 11.5px; font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase; color: #8a8079;
  padding: 12px 24px; background: #faf6f0;
  border-bottom: 1px solid #ece7e1;
}
.crm-table-inner td {
  padding: 14px 24px; border-bottom: 1px solid #f5f0e8;
  vertical-align: middle;
}
.crm-table-inner tbody tr:last-child td { border-bottom: none; }
.crm-table-inner tbody tr.clickable { cursor: pointer; transition: background 0.15s; }
.crm-table-inner tbody tr.clickable:hover { background: #faf6f0; }

.crm-course-name { font-weight: 600; color: #15110f; }
.crm-course-slug { font-size: 12.5px; color: #8a8079; margin-top: 2px; }

.align-right { text-align: right; }
.align-center { text-align: center; }

.cell-count {
  display: inline-block; font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 600; color: #15110f;
}

/* ===== Бейджи ===== */
.badge {
  display: inline-block; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-muted { background: #f0ede8; color: #8a8079; }
.badge-gold { background: #fff5e0; color: #8c6a10; }

.role-tag {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.5px; padding: 3px 8px; border-radius: 999px;
  background: #f0ede8; color: #6f655c;
}
.role-student { background: #eaf0ff; color: #2c4b8f; }
.role-teacher { background: #fff5e0; color: #8c6a10; }

.muted { color: #a59c93; font-size: 13.5px; }
.crm-empty {
  color: #a59c93; font-size: 15px;
  padding: 32px 24px; text-align: center;
}
</style>