<template>
  <div class="crm-student">
    <!-- Загрузка -->
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando alumno...</p>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmStudents' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <!-- Контент -->
    <template v-else-if="student">
      <!-- Хлебные крошки -->
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmStudents' }">Alumnos</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ student.username || student.email }}</span>
      </nav>

      <!-- Хедер -->
      <header class="crm-header-card">
        <div class="crm-header-main">
          <div class="crm-avatar-lg">
            <img v-if="student.avatar" :src="student.avatar" :alt="student.username">
            <span v-else>{{ (student.username || student.email).charAt(0).toUpperCase() }}</span>
          </div>
          <div class="crm-header-info">
            <h1 class="crm-header-name">{{ student.username || student.email }}</h1>
            <div class="crm-header-meta">
              <a :href="`mailto:${student.email}`" class="crm-meta-item">{{ student.email }}</a>
              <span v-if="student.phone" class="crm-meta-item">📞 {{ student.phone }}</span>
              <span class="crm-meta-item">
                📅 Registro: {{ formatDate(student.created_at) }}
              </span>
              <span v-if="!student.is_active" class="badge badge-muted">Inactivo</span>
            </div>
            <div class="crm-header-roles">
              <span
                v-for="r in student.roles"
                :key="r"
                class="role-tag"
                :class="`role-${r}`"
              >{{ r }}</span>
            </div>
          </div>
        </div>
        <div class="crm-header-actions">
          <a
            :href="`mailto:${student.email}`"
            class="crm-btn crm-btn-outline"
          >
            ✉ Enviar email
          </a>
          <a
            :href="adminUserUrl"
            target="_blank"
            class="crm-btn crm-btn-outline"
          >
            Django admin →
          </a>
        </div>
      </header>

      <!-- Stats -->
      <div class="crm-stats">
        <div class="crm-stat">
          <span class="crm-stat-label">Cursos</span>
          <span class="crm-stat-value">{{ student.stats.courses_count }}</span>
          <span class="crm-stat-sub">{{ student.stats.courses_active }} activos</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Pedidos</span>
          <span class="crm-stat-value">{{ student.stats.orders_count }}</span>
          <span class="crm-stat-sub">{{ student.stats.orders_paid }} pagados</span>
        </div>
        <div class="crm-stat crm-stat--accent">
          <span class="crm-stat-label">Total pagado</span>
          <span class="crm-stat-value">${{ student.stats.total_paid_usd }}</span>
          <span class="crm-stat-sub">USD</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Última actividad</span>
          <span class="crm-stat-value crm-stat-value--sm">
            {{ student.stats.last_activity ? formatDateTime(student.stats.last_activity) : '—' }}
          </span>
        </div>
      </div>

      <!-- Cursos -->
      <CrmDetailSection title="Cursos" :count="student.courses.length">
        <div v-if="student.courses.length === 0" class="crm-empty">
          Este alumno no está inscrito en ningún curso.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Curso</th>
              <th class="align-center">Estado</th>
              <th class="align-center">Progreso</th>
              <th class="align-right">Inscrito</th>
              <th class="align-right">Última actividad</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in student.courses"
              :key="c.course_id"
              class="clickable"
              @click="goToCourse(c.course_id)"
            >
              <td>
                <div class="crm-course-name">{{ c.course_title }}</div>
                <div class="crm-course-sub">
                  {{ c.lessons_completed }} / {{ c.lessons_total }} lecciones
                </div>
              </td>
              <td class="align-center">
                <span class="badge" :class="c.is_active ? 'badge-success' : 'badge-muted'">
                  {{ c.is_active ? 'Activo' : 'Sin acceso' }}
                </span>
              </td>
              <td class="align-center">
                <CrmProgressBar :percent="c.progress_percent" style="min-width: 140px" />
              </td>
              <td class="align-right muted">{{ formatDate(c.enrolled_at) }}</td>
              <td class="align-right muted">
                {{ c.last_activity ? formatDate(c.last_activity) : '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </CrmDetailSection>

      <!-- Accesos a cursos (con extensión de plazo) -->
      <CrmDetailSection title="Accesos a cursos" :count="student.courses.length">
        <div v-if="student.courses.length === 0" class="crm-empty">
          Este alumno no está inscrito en ningún curso.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Curso</th>
              <th class="align-center">Estado</th>
              <th class="align-center">Vence</th>
              <th class="align-center">Días</th>
              <th class="align-right"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in student.courses" :key="c.enrollment_id">
              <td>
                <router-link
                  :to="{ name: 'CrmCourseDetail', params: { id: c.course_id } }"
                  class="crm-link"
                >
                  {{ c.course_title }}
                </router-link>
              </td>
              <td class="align-center">
                <span class="badge" :class="accessBadgeClass(c.access_status)">
                  {{ statusLabel(c.access_status) }}
                </span>
              </td>
              <td class="align-center muted">
                {{ c.access_expires_at ? formatDate(c.access_expires_at) : 'Sin límite' }}
              </td>
              <td class="align-center">
                <span
                  v-if="c.days_left !== null && c.days_left !== undefined"
                  :class="{ 'text-danger': c.days_left <= 3 && c.access_status === 'active' }"
                >
                  {{ c.days_left }}d
                </span>
                <span v-else class="muted">—</span>
              </td>
              <td class="align-right">
                <button class="crm-btn-sm" @click="openExtendModal(c)">
                  Extender
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </CrmDetailSection>

      <!-- Pedidos -->
      <CrmDetailSection title="Pedidos" :count="student.orders.length">
        <div v-if="student.orders.length === 0" class="crm-empty">
          Sin pedidos.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Pedido</th>
              <th>Productos</th>
              <th class="align-center">Estado</th>
              <th class="align-right">Total</th>
              <th class="align-right">Fecha</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="o in student.orders"
              :key="o.id"
              class="clickable"
              @click="goToOrder(o.id)"
            >
              <td class="mono">{{ o.order_number }}</td>
              <td class="muted">{{ o.items.join(', ') }}</td>
              <td class="align-center">
                <span
                  class="badge"
                  :class="o.status === 'paid' ? 'badge-success' : 'badge-muted'"
                >
                  {{ o.status_display }}
                </span>
              </td>
              <td class="align-right">
                <strong>${{ o.total }}</strong> {{ o.currency }}
              </td>
              <td class="align-right muted">
                {{ formatDate(o.paid_at || o.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>
      </CrmDetailSection>
    </template>
    <!-- Модалка продления доступа -->
    <div v-if="extendRow" class="crm-modal-overlay" @click.self="closeExtendModal">
      <div class="crm-modal">
        <h2 class="crm-modal-title">Extender acceso</h2>

        <div class="crm-modal-info">
          <div><strong>Alumno:</strong> {{ student.username || student.email }}</div>
          <div><strong>Curso:</strong> {{ extendRow.course_title }}</div>
          <div>
            <strong>Vence actualmente:</strong>
            {{ extendRow.access_expires_at ? formatDate(extendRow.access_expires_at) : 'Sin límite' }}
          </div>
        </div>

        <div class="crm-modal-field">
          <label>Extender por:</label>
          <div class="crm-extend-options">
            <button
              v-for="d in [7, 14, 30, 60, 90]"
              :key="d"
              class="crm-extend-btn"
              :class="{ active: extendDays === d }"
              @click="selectExtendDays(d)"
            >
              +{{ d }}d
            </button>
          </div>
        </div>

        <div class="crm-modal-field">
          <label>O fecha exacta:</label>
          <input
            v-model="extendDate"
            type="date"
            class="crm-modal-date"
            @input="extendDays = null"
          >
        </div>

        <div class="crm-modal-actions">
          <button class="crm-btn crm-btn-outline" @click="closeExtendModal">
            Cancelar
          </button>
          <button
            class="crm-btn crm-btn-primary"
            :disabled="extending || (!extendDays && !extendDate)"
            @click="confirmExtend"
          >
            {{ extending ? 'Extendiendo…' : 'Extender' }}
          </button>
        </div>
      </div>
    </div>
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
const student = ref(null)

const adminUserUrl = computed(() => {
  if (!student.value) return '#'
  // Допущение: Django admin на /admin/. Если у тебя другой префикс — поправь.
  return `/admin/mentored/user/${student.value.id}/change/`
})

const loadStudent = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getStudent(route.params.id)
    student.value = res.data
  } catch (e) {
    console.error('Error loading student:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la información del alumno.'
  } finally {
    loading.value = false
  }
}

const goToCourse = (id) => {
  router.push({ name: 'CrmCourseDetail', params: { id } })
}

const goToOrder = (id) => {
  router.push({ name: 'CrmOrderDetail', params: { id } })
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

const formatDateTime = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-ES', {
    day: '2-digit', month: '2-digit', year: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}

onMounted(loadStudent)
// ============ ПРОДЛЕНИЕ ДОСТУПА ============
const extendRow = ref(null)
const extendDays = ref(30)
const extendDate = ref('')
const extending = ref(false)

const openExtendModal = (courseRow) => {
  extendRow.value = courseRow
  extendDays.value = 30
  extendDate.value = ''
}

const closeExtendModal = () => {
  extendRow.value = null
  extendDays.value = 30
  extendDate.value = ''
}

const selectExtendDays = (d) => {
  extendDays.value = d
  extendDate.value = ''
}

const confirmExtend = async () => {
  if (!extendRow.value) return
  extending.value = true
  try {
    const payload = extendDate.value
      ? { new_expires_at: `${extendDate.value}T23:59:59Z` }
      : { days: extendDays.value }

    await crmApi.extendEnrollmentAccess(extendRow.value.enrollment_id, payload)
    closeExtendModal()
    await loadStudent()
  } catch (e) {
    console.error('extend error', e)
    alert('No se pudo extender el acceso.')
  } finally {
    extending.value = false
  }
}

// ============ СТАТУСЫ ДОСТУПА ============
const accessBadgeClass = (status) => {
  if (status === 'active') return 'badge-success'
  if (status === 'expired') return 'badge-danger'
  if (status === 'not_started') return 'badge-muted'
  if (status === 'blocked') return 'badge-muted'
  return 'badge-muted'
}

const statusLabel = (status) => {
  const map = {
    'active': 'Activo',
    'expired': 'Vencido',
    'not_started': 'Próximo',
    'blocked': 'Bloqueado',
  }
  return map[status] || status
}
</script>

<style scoped>
/* ===== Загрузка / ошибка ===== */
.crm-loading,
.crm-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: #8a8079;
  text-align: center;
}

.crm-loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e4ddd2;
  border-top: 4px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.crm-error h2 {
  font-family: 'Playfair Display', serif;
  color: #15110f;
}

/* ===== Хлебные крошки ===== */
.crm-breadcrumb {
  font-size: 14px;
  color: #8a8079;
  margin-bottom: 12px;
}

.crm-breadcrumb a {
  color: #8e1519;
  text-decoration: none;
}

.crm-breadcrumb-sep {
  margin: 0 8px;
  color: #c9bca6;
}

.crm-breadcrumb-current {
  color: #15110f;
}

/* ===== Хедер ===== */
.crm-header-card {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
}

.crm-header-main {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  min-width: 0;
}

.crm-avatar-lg {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  overflow: hidden;
  flex-shrink: 0;
}

.crm-avatar-lg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.crm-header-name {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 8px;
}

.crm-header-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 14px;
  color: #6f655c;
  margin-bottom: 10px;
}

.crm-meta-item {
  color: #6f655c;
  text-decoration: none;
}

a.crm-meta-item:hover {
  color: #8e1519;
}

.crm-header-roles {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.crm-header-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* ===== Кнопки ===== */
.crm-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  padding: 9px 16px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1.5px solid transparent;
}

.crm-btn-outline {
  background: #ffffff;
  border-color: #ece7e1;
  color: #5d544c;
}

.crm-btn-outline:hover {
  border-color: #8e1519;
  color: #8e1519;
}

/* ===== Stats ===== */
.crm-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.crm-stat {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.crm-stat--accent {
  background: #0e0c0c;
  border-color: #0e0c0c;
}

.crm-stat-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
}

.crm-stat--accent .crm-stat-label {
  color: #c49a3f;
}

.crm-stat-value {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #15110f;
  line-height: 1.1;
}

.crm-stat-value--sm {
  font-size: 16px;
}

.crm-stat--accent .crm-stat-value {
  color: #ffffff;
}

.crm-stat-sub {
  font-size: 13px;
  color: #a59c93;
}

/* ===== Внутренняя таблица ===== */
.crm-table-inner {
  width: 100%;
  border-collapse: collapse;
  font-size: 14.5px;
}

.crm-table-inner th {
  text-align: left;
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
  padding: 12px 24px;
  background: #faf6f0;
  border-bottom: 1px solid #ece7e1;
}

.crm-table-inner td {
  padding: 14px 24px;
  border-bottom: 1px solid #f5f0e8;
  vertical-align: middle;
}

.crm-table-inner tbody tr:last-child td {
  border-bottom: none;
}

.crm-table-inner tbody tr.clickable {
  cursor: pointer;
  transition: background 0.15s;
}

.crm-table-inner tbody tr.clickable:hover {
  background: #faf6f0;
}

.crm-course-name {
  font-weight: 600;
  color: #15110f;
}

.crm-course-sub {
  font-size: 12.5px;
  color: #8a8079;
  margin-top: 2px;
}

.align-right { text-align: right; }
.align-center { text-align: center; }

.mono {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 13px;
  color: #8e1519;
}

/* ===== Бейджи ===== */
.badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 4px 10px;
  border-radius: 999px;
}

.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-muted { background: #f0ede8; color: #8a8079; }

.role-tag {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 3px 8px;
  border-radius: 999px;
  background: #f0ede8;
  color: #6f655c;
}

.role-student { background: #eaf0ff; color: #2c4b8f; }
.role-teacher { background: #fff5e0; color: #8c6a10; }

.muted { color: #a59c93; font-size: 13.5px; }

.crm-empty {
  color: #a59c93;
  font-size: 15px;
  padding: 32px 24px;
  text-align: center;
}

/* --- Ссылки --- */
.crm-link {
  color: #8e1519;
  text-decoration: none;
  font-weight: 500;
}
.crm-link:hover { text-decoration: underline; }

/* --- Кнопка Extender --- */
.crm-btn-sm {
  background: #0e0c0c;
  color: #fff;
  border: none;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s;
}
.crm-btn-sm:hover { background: #2a1a1a; }

/* --- Text danger --- */
.text-danger { color: #8e1519; font-weight: 600; }

/* --- Бейджи --- */
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-muted { background: #f0ede8; color: #8a8079; }

/* --- Модалка продления --- */
.crm-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(14, 12, 12, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.crm-modal {
  background: #fff;
  border-radius: 18px;
  padding: 28px;
  max-width: 460px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.crm-modal-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 18px;
}

.crm-modal-info {
  background: #faf6f0;
  border-radius: 12px;
  padding: 14px 18px;
  font-size: 14px;
  color: #3a342e;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 20px;
}

.crm-modal-field {
  margin-bottom: 18px;
}

.crm-modal-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
  margin-bottom: 8px;
}

.crm-extend-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.crm-extend-btn {
  border: 1.5px solid #ece7e1;
  background: #fff;
  border-radius: 999px;
  padding: 8px 16px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  color: #5d544c;
  cursor: pointer;
  transition: all 0.15s;
}

.crm-extend-btn:hover {
  border-color: #8e1519;
  color: #8e1519;
}

.crm-extend-btn.active {
  background: #0e0c0c;
  color: #fff;
  border-color: #0e0c0c;
}

.crm-modal-date {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #ece7e1;
  border-radius: 10px;
  padding: 10px 14px;
  font-family: inherit;
  font-size: 14.5px;
  color: #15110f;
  background: #faf6f0;
  outline: none;
}

.crm-modal-date:focus {
  border-color: #8e1519;
}

.crm-modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 24px;
}

.crm-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1.5px solid transparent;
}

.crm-btn-outline {
  background: #fff;
  border-color: #ece7e1;
  color: #5d544c;
}

.crm-btn-outline:hover {
  border-color: #8e1519;
  color: #8e1519;
}

.crm-btn-primary {
  background: #0e0c0c;
  border-color: #0e0c0c;
  color: #fff;
}

.crm-btn-primary:hover:not(:disabled) {
  background: #2a1a1a;
}

.crm-btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>