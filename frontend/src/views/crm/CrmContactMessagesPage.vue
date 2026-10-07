<template>
  <div class="crm-messages">
    <header class="crm-page-head">
      <div>
        <h1 class="crm-page-title">Mensajes</h1>
        <p class="crm-page-sub">Mensajes del formulario de contacto</p>
      </div>
      <div class="crm-page-count">
        <strong>{{ count }}</strong> mensajes
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
          placeholder="Buscar por nombre, email, mensaje..."
          @input="onSearch"
        >
      </div>

      <select v-model="motivoFilter" @change="reload(1)">
        <option value="">Todos los motivos</option>
        <option v-for="m in motivos" :key="m" :value="m">{{ m }}</option>
      </select>

      <select v-model="readFilter" @change="reload(1)">
        <option value="">Todos</option>
        <option value="false">Sin leer</option>
        <option value="true">Leídos</option>
      </select>
    </div>

    <!-- Массовые действия -->
    <div v-if="selectedIds.length > 0" class="crm-bulk-bar">
      <span class="crm-bulk-count">{{ selectedIds.length }} seleccionados</span>
      <button class="crm-btn crm-btn-outline" @click="bulkAction('mark_read')">
        Marcar como leídos
      </button>
      <button class="crm-btn crm-btn-outline" @click="bulkAction('mark_unread')">
        Marcar como no leídos
      </button>
      <button class="crm-btn crm-btn-danger" @click="bulkAction('delete')">
        Eliminar
      </button>
      <button class="crm-btn crm-btn-link" @click="selectedIds = []">
        Cancelar
      </button>
    </div>

    <!-- Таблица -->
    <div class="crm-table-wrap" v-if="!loading">
      <table class="crm-table">
        <thead>
          <tr>
            <th class="col-check">
              <input
                type="checkbox"
                :checked="allSelected"
                :indeterminate.prop="someSelected && !allSelected"
                @change="toggleAll"
              >
            </th>
            <th>Fecha</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Motivo</th>
            <th>Mensaje</th>
            <th class="align-center">Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="m in messages"
            :key="m.id"
            :class="{ clickable: true, unread: !m.is_read }"
            @click="goToMessage(m.id)"
          >
            <td class="col-check" @click.stop>
              <input
                type="checkbox"
                :value="m.id"
                v-model="selectedIds"
              >
            </td>
            <td class="muted">{{ formatDate(m.created_at) }}</td>
            <td><strong>{{ m.name }}</strong></td>
            <td class="muted">{{ m.email }}</td>
            <td>
              <span class="motivo-tag">{{ m.motivo }}</span>
            </td>
            <td class="preview">{{ m.message_preview }}</td>
            <td class="align-center">
              <span class="badge" :class="m.is_read ? 'badge-muted' : 'badge-danger'">
                {{ m.is_read ? 'Leído' : 'Nuevo' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="messages.length === 0" class="crm-empty">
        No se encontraron mensajes.
      </div>
    </div>

    <div v-else class="crm-loading">
      <div class="crm-loading-spinner"></div>
    </div>

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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { crmApi } from '../../api/crm'
import CrmPagination from './CrmPagination.vue'

const router = useRouter()

const motivos = [
  'Consulta sobre cursos',
  'Reservar una consulta 1:1',
  'Mi pedido o pago',
  'Devoluciones',
  'Colaboraciones',
  'Otro',
]

const messages = ref([])
const loading = ref(true)
const count = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(20)
const search = ref('')
const motivoFilter = ref('')
const readFilter = ref('')
const selectedIds = ref([])

let searchTimeout = null

const allSelected = computed(() =>
  messages.value.length > 0 && selectedIds.value.length === messages.value.length
)
const someSelected = computed(() => selectedIds.value.length > 0)

const loadMessages = async () => {
  loading.value = true
  selectedIds.value = []
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (search.value) params.search = search.value
    if (motivoFilter.value) params.motivo = motivoFilter.value
    if (readFilter.value) params.is_read = readFilter.value

    const res = await crmApi.getContactMessages(params)
    messages.value = res.data.results
    count.value = res.data.count
    pages.value = res.data.pages || 1
    page.value = res.data.page || 1
  } catch (e) {
    console.error('Error loading messages:', e)
    messages.value = []
    count.value = 0
  } finally {
    loading.value = false
  }
}

const reload = (newPage = 1) => {
  page.value = newPage
  loadMessages()
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => reload(1), 350)
}

const onPageSizeChange = (value) => {
  pageSize.value = value
  reload(1)
}

const toggleAll = (e) => {
  if (e.target.checked) {
    selectedIds.value = messages.value.map(m => m.id)
  } else {
    selectedIds.value = []
  }
}

const goToMessage = (id) => {
  router.push({ name: 'CrmContactMessageDetail', params: { id } })
}

const bulkAction = async (action) => {
  if (!selectedIds.value.length) return
  if (action === 'delete' && !confirm(`¿Eliminar ${selectedIds.value.length} mensajes?`)) return

  try {
    await crmApi.bulkContactMessages({ action, ids: selectedIds.value })
    selectedIds.value = []
    await loadMessages()
  } catch (e) {
    console.error('Bulk action error:', e)
    alert('Error al ejecutar la acción')
  }
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

onMounted(loadMessages)
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

.crm-bulk-bar {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  background: #0e0c0c; color: #ffffff;
  border-radius: 12px; padding: 12px 20px; margin-bottom: 16px;
}
.crm-bulk-count {
  font-weight: 600; margin-right: auto;
  color: #c49a3f;
}
.crm-bulk-bar .crm-btn-outline {
  background: transparent; border-color: #3a342e; color: #cfc9c4;
}
.crm-bulk-bar .crm-btn-outline:hover { border-color: #c49a3f; color: #c49a3f; }
.crm-btn-danger {
  background: #8e1519; border-color: #8e1519; color: #fff;
}
.crm-btn-danger:hover { background: #a01a1f; border-color: #a01a1f; }
.crm-btn-link {
  background: transparent; border: none; color: #cfc9c4;
  text-decoration: underline; cursor: pointer;
  font-family: inherit; font-size: 14px; padding: 9px 8px;
}
.crm-btn-link:hover { color: #fff; }

.crm-btn {
  display: inline-flex; align-items: center; gap: 6px;
  font-family: inherit; font-size: 14px; font-weight: 600;
  padding: 9px 16px; border-radius: 999px;
  cursor: pointer; transition: all 0.2s;
  border: 1.5px solid transparent;
}

.crm-table-wrap {
  background: #ffffff; border: 1px solid #ece7e1;
  border-radius: 16px; overflow: hidden;
}
.crm-table {
  width: 100%; border-collapse: collapse; font-size: 14.5px;
}
.crm-table thead { background: #faf6f0; }
.crm-table th {
  text-align: left; font-size: 11.5px; font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase; color: #8a8079;
  padding: 12px 16px; border-bottom: 1px solid #ece7e1;
  white-space: nowrap;
}
.crm-table td {
  padding: 14px 16px; border-bottom: 1px solid #f5f0e8;
  color: #3a342e; vertical-align: middle;
}
.crm-table tbody tr:last-child td { border-bottom: none; }
.crm-table tbody tr.clickable { cursor: pointer; transition: background 0.15s; }
.crm-table tbody tr.clickable:hover { background: #faf6f0; }
.crm-table tbody tr.unread td { font-weight: 500; }
.crm-table tbody tr.unread { background: #fffbf5; }

.col-check {
  width: 40px;
  text-align: center;
}
.col-check input { cursor: pointer; accent-color: #8e1519; }

.preview {
  max-width: 300px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  color: #6f655c; font-size: 13.5px;
}

.motivo-tag {
  font-size: 11.5px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.5px; color: #8e1519;
  background: #faf6f0; padding: 3px 10px; border-radius: 999px;
  white-space: nowrap;
}

.badge {
  display: inline-block; font-size: 11.5px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-muted { background: #f0ede8; color: #8a8079; }

.align-center { text-align: center; }
.muted { color: #a59c93; font-size: 13.5px; }
.crm-empty {
  color: #a59c93; font-size: 15px;
  padding: 32px 24px; text-align: center;
}
.crm-loading {
  padding: 60px 20px; text-align: center;
}
.crm-loading-spinner {
  width: 36px; height: 36px;
  border: 3px solid #e4ddd2; border-top: 3px solid #8e1519;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin: 0 auto;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>