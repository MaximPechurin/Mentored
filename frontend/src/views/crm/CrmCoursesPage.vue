<template>
  <div class="crm-courses">
    <header class="crm-page-head">
      <div>
        <h1 class="crm-page-title">Cursos</h1>
        <p class="crm-page-sub">Cursos de la escuela con sus métricas</p>
      </div>
      <div class="crm-page-count">
        <strong>{{ count }}</strong> cursos
      </div>
    </header>

    <!-- Фильтры -->
    <div class="crm-filters">
      <div class="crm-filter-search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Buscar por título o slug..."
          @input="onSearch"
        >
      </div>

      <select v-model="statusFilter" @change="reload(1)">
        <option value="">Todos los estados</option>
        <option value="active">Activos</option>
        <option value="inactive">Inactivos</option>
      </select>

      <label class="crm-check">
        <input type="checkbox" v-model="hasWhatsapp" @change="reload(1)">
        <span>Con WhatsApp</span>
      </label>
    </div>

    <!-- Таблица -->
    <CrmDataTable
      :columns="columns"
      :rows="courses"
      :loading="loading"
      :ordering="ordering"
      empty-text="No se encontraron cursos."
      clickable
      @update:ordering="onOrderingChange"
      @row-click="goToCourse"
    >
      <template #title="{ row }">
        <div class="cell-course">
          <div class="cell-course-name">{{ row.title }}</div>
          <div class="cell-course-slug">{{ row.slug }}</div>
        </div>
      </template>

      <template #is_active="{ row }">
        <span class="badge" :class="row.is_active ? 'badge-success' : 'badge-muted'">
          {{ row.is_active ? 'Activo' : 'Inactivo' }}
        </span>
      </template>

      <template #students_count="{ row }">
        <span class="cell-count">{{ row.students_count }}</span>
      </template>

      <template #completions_count="{ row }">
        <span class="cell-count">{{ row.completions_count }}</span>
      </template>

      <template #avg_progress="{ row }">
        <CrmProgressBar :percent="row.avg_progress" style="min-width: 140px" />
      </template>

      <template #payments_count="{ row }">
        <span class="cell-count">{{ row.payments_count }}</span>
      </template>

      <template #revenue_usd="{ row }">
        <strong class="cell-money">${{ row.revenue_usd }}</strong>
      </template>

      <template #has_whatsapp="{ row }">
        <span v-if="row.has_whatsapp" class="wa-icon" title="Tiene grupo de WhatsApp">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
          </svg>
        </span>
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
import CrmProgressBar from './CrmProgressBar.vue'

const router = useRouter()

const columns = [
  { key: 'title', label: 'Curso', sortable: true },
  { key: 'is_active', label: 'Estado', align: 'center' },
  { key: 'students_count', label: 'Alumnos', align: 'center', sortable: true },
  { key: 'completions_count', label: 'Completados', align: 'center', sortable: true },
  { key: 'avg_progress', label: 'Progreso medio' },
  { key: 'payments_count', label: 'Pagos', align: 'center' },
  { key: 'revenue_usd', label: 'Ventas', align: 'right' },
  { key: 'has_whatsapp', label: 'WhatsApp', align: 'center' },
]

const courses = ref([])
const loading = ref(true)
const count = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(20)
const search = ref('')
const statusFilter = ref('')
const hasWhatsapp = ref(false)
const ordering = ref('title')

let searchTimeout = null

const loadCourses = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (hasWhatsapp.value) params.has_whatsapp = 'true'
    if (ordering.value) params.ordering = ordering.value

    const res = await crmApi.getCourses(params)
    courses.value = res.data.results
    count.value = res.data.count
    pages.value = res.data.pages || 1
    page.value = res.data.page || 1
  } catch (e) {
    console.error('Error loading courses:', e)
    courses.value = []
    count.value = 0
  } finally {
    loading.value = false
  }
}

const reload = (newPage = 1) => {
  page.value = newPage
  loadCourses()
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

const goToCourse = (row) => {
  router.push({ name: 'CrmCourseDetail', params: { id: row.id } })
}

onMounted(loadCourses)
</script>

<style scoped>
.crm-page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 22px 24px;
  margin-bottom: 20px;
}

.crm-page-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 4px;
}

.crm-page-sub {
  color: #8a8079;
  font-size: 14.5px;
  margin: 0;
}

.crm-page-count {
  color: #8a8079;
  font-size: 14.5px;
}

.crm-page-count strong {
  color: #8e1519;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
}

/* --- Фильтры --- */
.crm-filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 16px;
}

.crm-filter-search {
  flex: 1;
  min-width: 240px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #faf6f0;
  border-radius: 10px;
  padding: 0 14px;
  color: #8a8079;
}

.crm-filter-search input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-family: inherit;
  font-size: 14.5px;
  padding: 10px 0;
  color: #15110f;
}

.crm-filters select {
  border: 1px solid #ece7e1;
  background: #faf6f0;
  border-radius: 10px;
  padding: 10px 14px;
  font-family: inherit;
  font-size: 14.5px;
  color: #15110f;
  cursor: pointer;
}

.crm-check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14.5px;
  color: #5d544c;
  cursor: pointer;
  user-select: none;
}

.crm-check input {
  accent-color: #8e1519;
}

/* --- Ячейки --- */
.cell-course-name {
  font-weight: 600;
  color: #15110f;
}

.cell-course-slug {
  font-size: 12.5px;
  color: #8a8079;
  margin-top: 2px;
}

.cell-count {
  display: inline-block;
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #15110f;
}

.cell-money {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  color: #8e1519;
}

.wa-icon {
  color: #1f7a3d;
}

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

.muted { color: #a59c93; font-size: 13.5px; }
</style>