<template>
  <div class="crm-submissions">
    <header class="crm-page-head">
      <div>
        <h1 class="crm-page-title">Tareas</h1>
        <p class="crm-page-sub">Respuestas de alumnos a las tareas</p>
      </div>
      <div class="crm-page-count">
        <strong>{{ count }}</strong> tareas
      </div>
      <CrmExportButton
        url="/crm/submissions/export/"
        :params="exportParams"
      />
    </header>

    <div class="crm-filters">
      <div class="crm-filter-search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Buscar por alumno, curso o tarea..."
          @input="onSearch"
        >
      </div>

      <select v-model="statusFilter" @change="reload(1)">
        <option value="">Todos los estados</option>
        <option value="submitted">Pendiente</option>
        <option value="reviewed">Revisado</option>
        <option value="needs_revision">Revisión</option>
      </select>

      <input
        v-model="dateFrom"
        type="date"
        class="crm-date"
        placeholder="Desde"
        @change="reload(1)"
      >
      <input
        v-model="dateTo"
        type="date"
        class="crm-date"
        placeholder="Hasta"
        @change="reload(1)"
      >
    </div>

    <CrmDataTable
      :columns="columns"
      :rows="submissions"
      :loading="loading"
      :ordering="ordering"
      empty-text="No se encontraron tareas."
      clickable
      @update:ordering="onOrderingChange"
      @row-click="goToSubmission"
    >
      <template #submitted_at="{ row }">
        <span class="muted">{{ formatDate(row.submitted_at) }}</span>
      </template>

      <template #user_name="{ row }">
        <div class="cell-client">
          <div class="cell-name">{{ row.user_name }}</div>
          <div class="cell-email">{{ row.user_email }}</div>
        </div>
      </template>

      <template #course_title="{ row }">
        <router-link
          :to="{ name: 'CrmCourseDetail', params: { id: row.course_id } }"
          class="crm-link"
          @click.stop
        >
          {{ row.course_title }}
        </router-link>
      </template>

      <template #lesson_title="{ row }">
        <span class="cell-lesson">{{ row.lesson_title }}</span>
      </template>

      <template #assignment_title="{ row }">
        <span class="cell-assignment">{{ row.assignment_title }}</span>
      </template>

      <template #status="{ row }">
        <span class="badge" :class="statusBadgeClass(row.status)">
          {{ row.status_display }}
        </span>
      </template>

      <template #score="{ row }">
        <span v-if="row.score !== null && row.score !== undefined" class="cell-score">
          {{ row.score }}
        </span>
        <span v-else class="muted">—</span>
      </template>

      <template #reviewed_by="{ row }">
        <span v-if="row.reviewed_by" class="muted">{{ row.reviewed_by }}</span>
        <span v-else class="muted">—</span>
      </template>
    </CrmDataTable>

    <CrmPagination
      :page="page"
      :pages="pages"
      :count="count"
      :page-size="pageSize"
      @change="reload"
      @update:page-size="onPageSizeChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { crmApi } from '../../api/crm'
import CrmDataTable from './CrmDataTable.vue'
import CrmPagination from './CrmPagination.vue'
import CrmExportButton from './CrmExportButton.vue'

const router = useRouter()

const columns = [
  { key: 'submitted_at', label: 'Fecha', sortable: true },
  { key: 'user_name', label: 'Alumno' },
  { key: 'course_title', label: 'Curso' },
  { key: 'lesson_title', label: 'Lección' },
  { key: 'assignment_title', label: 'Tarea' },
  { key: 'status', label: 'Estado', align: 'center' },
  { key: 'score', label: 'Nota', align: 'center', sortable: true },
  { key: 'reviewed_by', label: 'Revisado por' },
]

const submissions = ref([])
const loading = ref(true)
const count = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(20)
const search = ref('')
const statusFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const ordering = ref('-submitted_at')

let searchTimeout = null

const loadSubmissions = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value
    if (ordering.value) params.ordering = ordering.value

    const res = await crmApi.getSubmissions(params)
    submissions.value = res.data.results
    count.value = res.data.count
    pages.value = res.data.pages || 1
    page.value = res.data.page || 1
  } catch (e) {
    console.error('Error loading submissions:', e)
    submissions.value = []
    count.value = 0
  } finally {
    loading.value = false
  }
}

const reload = (newPage = 1) => {
  page.value = newPage
  loadSubmissions()
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => reload(1), 350)
}

const onOrderingChange = (value) => {
  ordering.value = value
  reload(1)
}

const onPageSizeChange = (value) => {
  pageSize.value = value
  reload(1)
}

const goToSubmission = (row) => {
  router.push({ name: 'CrmSubmissionDetail', params: { id: row.id } })
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

const statusBadgeClass = (status) => {
  if (status === 'reviewed') return 'badge-success'
  if (status === 'needs_revision') return 'badge-danger'
  return 'badge-warn'
}

const exportParams = computed(() => ({
  search: search.value || undefined,
  status: statusFilter.value || undefined,
  date_from: dateFrom.value || undefined,
  date_to: dateTo.value || undefined,
}))

onMounted(loadSubmissions)
</script>

<style scoped>
.crm-page-head {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap;
  background: #ffffff; border: 1px solid #ece7e1; border-radius: 16px;
  padding: 22px 24px; margin-bottom: 20px;
}
.crm-page-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600; color: #15110f; margin: 0 0 4px;
}
.crm-page-sub { color: #8a8079; font-size: 14.5px; margin: 0; }
.crm-page-count { color: #8a8079; font-size: 14.5px; }
.crm-page-count strong {
  color: #8e1519; font-family: 'Playfair Display', serif;
  font-size: 20px; font-weight: 600;
}

.crm-filters {
  display: flex; gap: 12px; flex-wrap: wrap; align-items: center;
  background: #ffffff; border: 1px solid #ece7e1; border-radius: 16px;
  padding: 16px 20px; margin-bottom: 16px;
}
.crm-filter-search {
  flex: 1; min-width: 240px;
  display: flex; align-items: center; gap: 10px;
  background: #faf6f0; border-radius: 10px; padding: 0 14px; color: #8a8079;
}
.crm-filter-search input {
  flex: 1; border: none; background: transparent; outline: none;
  font-family: inherit; font-size: 14.5px; padding: 10px 0; color: #15110f;
}
.crm-filters select,
.crm-date {
  border: 1px solid #ece7e1; background: #faf6f0; border-radius: 10px;
  padding: 10px 12px; font-family: inherit; font-size: 14px;
  color: #15110f; cursor: pointer;
}

.cell-client .cell-name { font-weight: 600; color: #15110f; }
.cell-client .cell-email { font-size: 12.5px; color: #8a8079; }

.cell-lesson,
.cell-assignment {
  font-size: 13.5px; color: #3a342e;
  display: inline-block; max-width: 200px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

.cell-score {
  display: inline-block;
  font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 600;
  color: #1f7a3d;
}

.crm-link {
  color: #8e1519; text-decoration: none; font-size: 13.5px;
}
.crm-link:hover { text-decoration: underline; }

.badge {
  display: inline-block; font-size: 11.5px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
  white-space: nowrap;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-warn { background: #fff5e0; color: #8c6a10; }

.muted { color: #a59c93; font-size: 13.5px; }

.crm-page-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}
</style>