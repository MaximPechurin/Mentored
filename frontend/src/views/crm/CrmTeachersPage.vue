<template>
  <div class="crm-teachers">
    <header class="crm-page-head">
      <div>
        <h1 class="crm-page-title">Profesores</h1>
        <p class="crm-page-sub">Profesores y mentores de la plataforma</p>
      </div>
      <div class="crm-page-count">
        <strong>{{ count }}</strong> profesores
      </div>
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
          placeholder="Buscar por nombre, email o teléfono..."
          @input="onSearch"
        >
      </div>

      <select v-model="statusFilter" @change="reload(1)">
        <option value="">Todos</option>
        <option value="active">Activos</option>
        <option value="inactive">Inactivos</option>
      </select>
    </div>

    <CrmDataTable
      :columns="columns"
      :rows="teachers"
      :loading="loading"
      :ordering="ordering"
      empty-text="No se encontraron profesores."
      clickable
      @update:ordering="onOrderingChange"
      @row-click="goToTeacher"
    >
      <template #username="{ row }">
        <div class="cell-user">
          <span class="cell-avatar">
            <img v-if="row.photo" :src="row.photo" :alt="row.username">
            <template v-else>{{ row.username.charAt(0).toUpperCase() }}</template>
          </span>
          <div>
            <div class="cell-name">{{ row.username }}</div>
            <div v-if="row.specialization" class="cell-spec">{{ row.specialization }}</div>
          </div>
        </div>
      </template>

      <template #email="{ row }">
        <span class="muted">{{ row.email }}</span>
      </template>

      <template #phone="{ row }">
        <span v-if="row.phone">{{ row.phone }}</span>
        <span v-else class="muted">—</span>
      </template>

      <template #courses_count="{ row }">
        <span class="cell-count">{{ row.courses_count }}</span>
      </template>

      <template #students_count="{ row }">
        <span class="cell-count">{{ row.students_count }}</span>
      </template>

      <template #is_active="{ row }">
        <span class="badge" :class="row.is_active ? 'badge-success' : 'badge-muted'">
          {{ row.is_active ? 'Activo' : 'Inactivo' }}
        </span>
      </template>

      <template #created_at="{ row }">
        <span class="muted">{{ formatDate(row.created_at) }}</span>
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

const router = useRouter()

const columns = [
  { key: 'username', label: 'Profesor', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'phone', label: 'Teléfono' },
  { key: 'courses_count', label: 'Cursos', align: 'center', sortable: true },
  { key: 'students_count', label: 'Alumnos', align: 'center', sortable: true },
  { key: 'is_active', label: 'Estado', align: 'center' },
  { key: 'created_at', label: 'Registro', align: 'right', sortable: true },
]

const teachers = ref([])
const loading = ref(true)
const count = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(20)
const search = ref('')
const statusFilter = ref('')
const ordering = ref('username')

let searchTimeout = null

const loadTeachers = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (ordering.value) params.ordering = ordering.value

    const res = await crmApi.getTeachers(params)
    teachers.value = res.data.results
    count.value = res.data.count
    pages.value = res.data.pages || 1
    page.value = res.data.page || 1
  } catch (e) {
    console.error('Error loading teachers:', e)
    teachers.value = []
    count.value = 0
  } finally {
    loading.value = false
  }
}

const reload = (newPage = 1) => {
  page.value = newPage
  loadTeachers()
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

const goToTeacher = (row) => {
  router.push({ name: 'CrmTeacherDetail', params: { id: row.id } })
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

onMounted(loadTeachers)
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
.crm-filters select {
  border: 1px solid #ece7e1; background: #faf6f0; border-radius: 10px;
  padding: 10px 14px; font-family: inherit; font-size: 14.5px;
  color: #15110f; cursor: pointer;
}

.cell-user { display: flex; align-items: center; gap: 12px; }
.cell-avatar {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 50%;
  background: #8e1519; color: #fff;
  font-weight: 600; font-size: 14px;
  overflow: hidden; flex-shrink: 0;
}
.cell-avatar img { width: 100%; height: 100%; object-fit: cover; }
.cell-name { font-weight: 600; color: #15110f; }
.cell-spec { font-size: 12.5px; color: #8a8079; margin-top: 2px; }

.cell-count {
  display: inline-block; font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 600; color: #15110f;
}

.badge {
  display: inline-block; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-muted { background: #f0ede8; color: #8a8079; }

.muted { color: #a59c93; font-size: 13.5px; }
</style>