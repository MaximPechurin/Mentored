<template>
  <div class="crm-course">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando curso...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmCourses' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <template v-else-if="course">
      <!-- Хлебные крошки -->
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmCourses' }">Cursos</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ course.title }}</span>
      </nav>

      <!-- Хедер -->
      <header class="crm-header-card">
        <div class="crm-header-main">
          <div class="crm-header-info">
            <h1 class="crm-header-name">{{ course.title }}</h1>
            <div class="crm-header-meta">
              <span class="crm-meta-item mono">{{ course.slug }}</span>
              <span class="badge" :class="course.is_active ? 'badge-success' : 'badge-muted'">
                {{ course.is_active ? 'Activo' : 'Inactivo' }}
              </span>
              <span class="crm-meta-item">
                📅 Creado: {{ formatDate(course.created_at) }}
              </span>
              <span v-if="course.creator" class="crm-meta-item">
                👤 {{ course.creator.username }}
              </span>
            </div>
          </div>
        </div>
        <div class="crm-header-actions">
          <a
            v-if="course.whatsapp_group_url"
            :href="course.whatsapp_group_url"
            target="_blank"
            rel="noopener"
            class="crm-btn crm-btn-outline"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
            WhatsApp
          </a>
          <router-link
            :to="course.forum_url"
            class="crm-btn crm-btn-outline"
            target="_blank"
          >
            💬 Ir al foro
          </router-link>
          <a
            :href="`/admin/school/course/${course.id}/change/`"
            target="_blank"
            class="crm-btn crm-btn-outline"
          >
            Django admin →
          </a>
          <button
            class="crm-btn crm-btn-outline"
            @click="downloadCourseReport"
          >
            📊 Descargar reporte
          </button>
        </div>
      </header>

      <!-- Stats -->
      <div class="crm-stats">
        <div class="crm-stat">
          <span class="crm-stat-label">Alumnos</span>
          <span class="crm-stat-value">{{ course.stats.students_count }}</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Completados</span>
          <span class="crm-stat-value">{{ course.stats.completions_count }}</span>
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Progreso medio</span>
          <CrmProgressBar :percent="course.stats.avg_progress" style="margin-top: 6px" />
        </div>
        <div class="crm-stat">
          <span class="crm-stat-label">Pagos</span>
          <span class="crm-stat-value">{{ course.stats.payments_count }}</span>
        </div>
        <div class="crm-stat crm-stat--accent">
          <span class="crm-stat-label">Ventas</span>
          <span class="crm-stat-value">${{ course.stats.revenue_usd }}</span>
          <span class="crm-stat-sub">USD</span>
        </div>
      </div>

      <!-- Módulos y lecciones -->
      <CrmDetailSection title="Módulos y lecciones" :count="totalLessons">
        <div v-if="course.modules.length === 0" class="crm-empty">
          Este curso no tiene módulos todavía.
        </div>
        <div v-else class="modules">
          <div v-for="mod in course.modules" :key="mod.id" class="module">
            <header class="module-head">
              <span class="module-order">{{ mod.order }}</span>
              <h3 class="module-title">{{ mod.title }}</h3>
              <span class="module-count">{{ mod.lessons.length }} lecciones</span>
            </header>
            <ul class="lesson-list">
              <li v-for="l in mod.lessons" :key="l.id" class="lesson">
                <span class="lesson-order">{{ l.order }}</span>
                <span class="lesson-title">{{ l.title }}</span>
                <span class="lesson-meta">
                  <span v-if="l.duration_minutes" class="lesson-duration">
                    {{ l.duration_minutes }} min
                  </span>
                  <span v-if="l.is_free_preview" class="lesson-free">gratis</span>
                  <span v-if="l.has_video" class="lesson-video">🎬</span>
                </span>
              </li>
            </ul>
          </div>
        </div>
      </CrmDetailSection>

      <!-- Ограничения по срокам -->
      <CrmDetailSection title="Duración del acceso">
        <div class="access-info">
          <div class="access-info-row">
            <span class="access-info-label">Modo</span>
            <span class="access-info-value">{{ accessModeLabel }}</span>
          </div>

          <template v-if="course.access_mode === 'duration'">
            <div class="access-info-row">
              <span class="access-info-label">Duración</span>
              <span class="access-info-value">
                {{ course.access_duration_days }} días desde la compra
              </span>
            </div>
          </template>

          <template v-if="course.access_mode === 'dates'">
            <div class="access-info-row">
              <span class="access-info-label">Inicio</span>
              <span class="access-info-value">{{ formatDate(course.access_start) }}</span>
            </div>
            <div class="access-info-row">
              <span class="access-info-label">Fin</span>
              <span class="access-info-value">{{ formatDate(course.access_end) }}</span>
            </div>
          </template>

          <div v-if="course.access_mode === 'unlimited'" class="access-info-hint">
            Este curso no tiene restricción de tiempo.
          </div>

          <!-- Предупреждения -->
          <div
            v-if="course.stats.expiring_soon_count > 0"
            class="access-warning access-warning--warn"
          >
            ⏳ {{ course.stats.expiring_soon_count }} alumno(s) pierden acceso en los próximos 7 días
          </div>
          <div
            v-if="course.stats.expired_count > 0"
            class="access-warning access-warning--danger"
          >
            🔒 {{ course.stats.expired_count }} alumno(s) ya no tienen acceso
          </div>
        </div>
      </CrmDetailSection>

      <!-- Alumnos -->
      <CrmDetailSection title="Alumnos del curso" :count="studentsMeta.count">
        <div v-if="students.length === 0" class="crm-empty">
          Sin alumnos inscritos.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Alumno</th>
              <th>Email</th>
              <th class="align-center">Inscrito</th>
              <th class="align-center">Vence</th>
              <th>Progreso</th>
              <th class="align-center">Completado</th>
              <th class="align-right">Última actividad</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="s in students"
              :key="s.user_id"
              class="clickable"
              @click="goToStudent(s.user_id)"
            >
              <td>
                <div class="cell-user">
                  <span class="cell-avatar">{{ s.username.charAt(0).toUpperCase() }}</span>
                  <span class="cell-name">{{ s.username }}</span>
                </div>
              </td>
              <td class="muted">{{ s.email }}</td>
              <td class="align-center muted">{{ formatDate(s.enrolled_at) }}</td>
              <td class="align-center">
                <span
                  v-if="s.access_expires_at"
                  class="badge"
                  :class="accessBadgeClass(s.access_status)"
                >
                  {{ formatDate(s.access_expires_at) }}
                </span>
                <span v-else class="muted">Sin límite</span>
              </td>
              <td>
                <CrmProgressBar :percent="s.progress_percent" style="min-width: 140px" />
              </td>
              <td class="align-center">
                <span v-if="s.completed" class="badge badge-success">✓</span>
                <span v-else class="muted">—</span>
              </td>
              <td class="align-right muted">
                {{ s.last_activity ? formatDate(s.last_activity) : '—' }}
              </td>
            </tr>
          </tbody>
        </table>

        <CrmPagination
          v-if="studentsMeta.count > studentsMeta.page_size"
          :page="studentsPage"
          :pages="Math.ceil(studentsMeta.count / studentsMeta.page_size)"
          :count="studentsMeta.count"
          :page-size="studentsMeta.page_size"
          @change="loadStudentsPage"
          @update:page-size="onStudentsPageSize"
        />
      </CrmDetailSection>

      <!-- Pedidos -->
      <CrmDetailSection title="Pedidos" :count="ordersMeta.count">
        <div v-if="orders.length === 0" class="crm-empty">
          Sin pedidos todavía.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Pedido</th>
              <th>Cliente</th>
              <th>Productos</th>
              <th class="align-center">Estado</th>
              <th class="align-right">Total</th>
              <th class="align-right">Fecha</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="o in orders"
              :key="o.id"
              class="clickable"
              @click="goToOrder(o.id)"
            >
              <td class="mono">{{ o.order_number }}</td>
              <td>{{ o.user_name }}</td>
              <td class="muted">{{ o.items.join(', ') }}</td>
              <td class="align-center">
                <span
                  class="badge"
                  :class="o.status === 'paid' ? 'badge-success' : 'badge-muted'"
                >
                  {{ o.status_display }}
                </span>
              </td>
              <td class="align-right"><strong>${{ o.total }}</strong> USD</td>
              <td class="align-right muted">
                {{ formatDate(o.paid_at || o.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>

        <CrmPagination
          v-if="ordersMeta.count > ordersMeta.page_size"
          :page="ordersPage"
          :pages="Math.ceil(ordersMeta.count / ordersMeta.page_size)"
          :count="ordersMeta.count"
          :page-size="ordersMeta.page_size"
          @change="loadOrdersPage"
          @update:page-size="onOrdersPageSize"
        />
      </CrmDetailSection>

      <!-- Productos vinculados -->
      <CrmDetailSection title="Productos vinculados" :count="course.products.length">
        <div v-if="course.products.length === 0" class="crm-empty">
          Este curso no está vinculado a ningún producto de la tienda.
        </div>
        <table v-else class="crm-table-inner">
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Producto</th>
              <th class="align-right">Precio</th>
              <th class="align-center">Estado</th>
              <th class="align-right"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in course.products" :key="`${p.type}-${p.id}`">
              <td><span class="role-tag">{{ p.type }}</span></td>
              <td>{{ p.name }}</td>
              <td class="align-right"><strong>${{ p.price }}</strong> USD</td>
              <td class="align-center">
                <span class="badge" :class="p.is_active ? 'badge-success' : 'badge-muted'">
                  {{ p.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="align-right">
                <a :href="p.admin_url" target="_blank" class="crm-link">admin →</a>
              </td>
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
import CrmPagination from './CrmPagination.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const course = ref(null)

const students = ref([])
const studentsMeta = ref({ count: 0, page_size: 20 })
const studentsPage = ref(1)

const orders = ref([])
const ordersMeta = ref({ count: 0, page_size: 20 })
const ordersPage = ref(1)

const totalLessons = computed(() => {
  if (!course.value) return 0
  return course.value.modules.reduce((sum, m) => sum + m.lessons.length, 0)
})

// === Тайминги доступа ===
const accessModeLabel = computed(() => {
  if (!course.value) return '—'
  const mode = course.value.access_mode
  if (mode === 'unlimited') return 'Sin límite'
  if (mode === 'duration') return 'Duración desde la compra'
  if (mode === 'dates') return 'Fechas fijas'
  return '—'
})

// === Бейджи статуса доступа ===
const accessBadgeClass = (status) => {
  if (status === 'active') return 'badge-success'
  if (status === 'expired') return 'badge-danger'
  if (status === 'not_started') return 'badge-muted'
  if (status === 'blocked') return 'badge-muted'
  return 'badge-muted'
}

const loadCourse = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getCourse(route.params.id)
    course.value = res.data
    students.value = res.data.students.results
    studentsMeta.value = {
      count: res.data.students.count,
      page_size: res.data.students.page_size,
    }
    orders.value = res.data.orders.results
    ordersMeta.value = {
      count: res.data.orders.count,
      page_size: res.data.orders.page_size,
    }
  } catch (e) {
    console.error('Error loading course:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la información del curso.'
  } finally {
    loading.value = false
  }
}

const loadStudentsPage = async (newPage) => {
  studentsPage.value = newPage
  const res = await crmApi.getCourseStudents(route.params.id, {
    page: newPage,
    page_size: studentsMeta.value.page_size,
  })
  students.value = res.data.results
  studentsMeta.value.count = res.data.count
}

const onStudentsPageSize = async (size) => {
  studentsMeta.value.page_size = size
  await loadStudentsPage(1)
}

const loadOrdersPage = async (newPage) => {
  ordersPage.value = newPage
  const res = await crmApi.getCourseOrders(route.params.id, {
    page: newPage,
    page_size: ordersMeta.value.page_size,
  })
  orders.value = res.data.results
  ordersMeta.value.count = res.data.count
}

const onOrdersPageSize = async (size) => {
  ordersMeta.value.page_size = size
  await loadOrdersPage(1)
}

const goToStudent = (id) => {
  router.push({ name: 'CrmStudentDetail', params: { id } })
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

const accessModeLabel = computed(() => {
  if (!course.value) return '—'
  const mode = course.value.access_mode
  if (mode === 'unlimited') return 'Sin límite'
  if (mode === 'duration') return 'Duración desde la compra'
  if (mode === 'dates') return 'Fechas fijas'
  return '—'
})

onMounted(loadCourse)

const downloadCourseReport = async () => {
  try {
    await crmApi.downloadExport(`/crm/courses/${course.value.id}/report/`)
  } catch (e) {
    console.error('Report error:', e)
    alert('No se pudo generar el reporte.')
  }
}
</script>

<style scoped>
/* ...стили такие же, как в CrmStudentDetailPage + доп. для модулей/уроков */

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
  width: 48px; height: 48px;
  border: 4px solid #e4ddd2;
  border-top: 4px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
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
  font-size: 26px; font-weight: 600; color: #15110f; margin: 0 0 8px;
}
.crm-header-meta {
  display: flex; gap: 16px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c;
  align-items: center;
}
.crm-meta-item { color: #6f655c; }
.crm-header-actions { display: flex; gap: 10px; flex-wrap: wrap; }

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

.crm-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}
.crm-stat {
  background: #fff; border: 1px solid #ece7e1; border-radius: 14px;
  padding: 18px 20px; display: flex; flex-direction: column; gap: 6px;
}
.crm-stat--accent { background: #0e0c0c; border-color: #0e0c0c; }
.crm-stat-label {
  font-size: 12px; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase; color: #8a8079;
}
.crm-stat--accent .crm-stat-label { color: #c49a3f; }
.crm-stat-value {
  font-family: 'Playfair Display', serif; font-size: 26px;
  font-weight: 600; color: #15110f; line-height: 1.1;
}
.crm-stat--accent .crm-stat-value { color: #fff; }
.crm-stat-sub { font-size: 13px; color: #a59c93; }

/* --- Модули --- */
.modules { padding: 16px 24px; display: flex; flex-direction: column; gap: 20px; }
.module { border-bottom: 1px solid #f5f0e8; padding-bottom: 16px; }
.module:last-child { border-bottom: none; padding-bottom: 0; }
.module-head {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 10px;
}
.module-order {
  display: inline-flex; align-items: center; justify-content: center;
  width: 26px; height: 26px; border-radius: 50%;
  background: #faf6f0; color: #8e1519;
  font-size: 12px; font-weight: 700;
}
.module-title {
  font-family: 'Playfair Display', serif; font-size: 17px;
  font-weight: 600; color: #15110f; margin: 0;
}
.module-count {
  font-size: 12.5px; color: #8a8079;
  background: #faf6f0; padding: 3px 10px; border-radius: 999px;
  margin-left: auto;
}
.lesson-list { list-style: none; padding: 0; margin: 0; }
.lesson {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 12px; border-radius: 8px;
  transition: background 0.15s;
}
.lesson:hover { background: #faf6f0; }
.lesson-order {
  font-size: 12px; color: #a59c93; min-width: 22px;
  font-family: monospace;
}
.lesson-title { font-size: 14.5px; color: #3a342e; flex: 1; }
.lesson-meta { display: flex; gap: 10px; align-items: center; }
.lesson-duration { font-size: 12.5px; color: #8a8079; }
.lesson-free {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  color: #1f7a3d; background: #eaf5ed;
  padding: 2px 8px; border-radius: 999px;
}
.lesson-video { font-size: 14px; }

/* --- Внутренняя таблица --- */
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

.align-right { text-align: right; }
.align-center { text-align: center; }
.mono {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 13px; color: #8e1519;
}

.cell-user { display: flex; align-items: center; gap: 10px; }
.cell-avatar {
  display: inline-flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border-radius: 50%;
  background: #8e1519; color: #fff;
  font-weight: 600; font-size: 12px;
}
.cell-name { font-weight: 600; color: #15110f; }

.badge {
  display: inline-block; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-muted { background: #f0ede8; color: #8a8079; }

.role-tag {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.5px; padding: 3px 8px; border-radius: 999px;
  background: #f0ede8; color: #6f655c;
}

.crm-link {
  color: #8e1519; text-decoration: none; font-size: 13px;
}
.crm-link:hover { text-decoration: underline; }

.muted { color: #a59c93; font-size: 13.5px; }
.crm-empty {
  color: #a59c93; font-size: 15px;
  padding: 32px 24px; text-align: center;
}

/* --- Блок "Duración del acceso" --- */
.access-info {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.access-info-row {
  display: flex;
  align-items: baseline;
  gap: 16px;
  font-size: 14.5px;
}

.access-info-label {
  min-width: 100px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #8a8079;
}

.access-info-value {
  color: #15110f;
  font-weight: 500;
}

.access-info-hint {
  font-size: 13.5px;
  color: #8a8079;
  font-style: italic;
}

.access-warning {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
}

.access-warning--warn {
  background: #fff5e0;
  color: #8c6a10;
}

.access-warning--danger {
  background: #fbeaea;
  color: #8e1519;
}

/* --- Бейджи --- */
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-muted { background: #f0ede8; color: #8a8079; }
</style>