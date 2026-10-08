<template>
  <div class="crm-orders">
    <header class="crm-page-head">
      <div>
        <h1 class="crm-page-title">Pedidos</h1>
        <p class="crm-page-sub">Todos los pedidos de la plataforma</p>
      </div>
      <div class="crm-page-count">
        <strong>{{ count }}</strong> pedidos
      </div>
      <CrmExportButton
        url="/crm/orders/export/"
        :params="exportParams"
      />
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
          placeholder="Buscar por número, email o nombre..."
          @input="onSearch"
        >
      </div>

      <select v-model="statusFilter" @change="reload(1)">
        <option value="">Todos los estados</option>
        <option value="pending">Pendiente</option>
        <option value="paid">Aprobado</option>
        <option value="processing">En proceso</option>
        <option value="completed">Completado</option>
        <option value="cancelled">Cancelado</option>
        <option value="refunded">Reembolsado</option>
      </select>

      <select v-model="paymentStatusFilter" @change="reload(1)">
        <option value="">Estado del pago</option>
        <option value="approved">Aprobado</option>
        <option value="pending">Pendiente</option>
        <option value="rejected">Rechazado</option>
        <option value="cancelled">Cancelado</option>
        <option value="refunded">Reembolsado</option>
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

    <!-- Таблица -->
    <CrmDataTable
      :columns="columns"
      :rows="orders"
      :loading="loading"
      :ordering="ordering"
      empty-text="No se encontraron pedidos."
      clickable
      @update:ordering="onOrderingChange"
      @row-click="goToOrder"
    >
      <template #order_number="{ row }">
        <span class="mono">{{ row.order_number }}</span>
      </template>

      <template #user_name="{ row }">
        <div class="cell-client">
          <div class="cell-name">{{ row.user_name }}</div>
          <div class="cell-email">{{ row.user_email }}</div>
        </div>
      </template>

      <template #products_summary="{ row }">
        <span class="cell-products" :title="row.products_summary">
          {{ row.products_summary }}
        </span>
      </template>

      <template #total="{ row }">
        <strong class="cell-money">${{ row.total }}</strong>
      </template>

      <template #status="{ row }">
        <span class="badge" :class="orderBadgeClass(row.status)">
          {{ row.status_display }}
        </span>
      </template>

      <template #payment_status="{ row }">
        <span v-if="row.payment_status" class="badge" :class="paymentBadgeClass(row.payment_status)">
          {{ row.payment_status_display }}
        </span>
        <span v-else class="muted">—</span>
      </template>

      <template #payment_method="{ row }">
        <span v-if="row.payment_method" class="method">{{ row.payment_method }}</span>
        <span v-else class="muted">—</span>
      </template>

      <template #created_at="{ row }">
        <span class="muted">{{ formatDate(row.paid_at || row.created_at) }}</span>
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
  { key: 'order_number', label: 'Pedido', sortable: true },
  { key: 'user_name', label: 'Cliente' },
  { key: 'products_summary', label: 'Productos' },
  { key: 'total', label: 'Total', align: 'right', sortable: true },
  { key: 'status', label: 'Estado', align: 'center' },
  { key: 'payment_status', label: 'Pago', align: 'center' },
  { key: 'payment_method', label: 'Método', align: 'center' },
  { key: 'created_at', label: 'Fecha', align: 'right', sortable: true },
]

const orders = ref([])
const loading = ref(true)
const count = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(20)
const search = ref('')
const statusFilter = ref('')
const paymentStatusFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const ordering = ref('-created_at')

let searchTimeout = null

const loadOrders = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (paymentStatusFilter.value) params.payment_status = paymentStatusFilter.value
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value
    if (ordering.value) params.ordering = ordering.value

    const res = await crmApi.getOrders(params)
    orders.value = res.data.results
    count.value = res.data.count
    pages.value = res.data.pages || 1
    page.value = res.data.page || 1
  } catch (e) {
    console.error('Error loading orders:', e)
    orders.value = []
    count.value = 0
  } finally {
    loading.value = false
  }
}

const reload = (newPage = 1) => {
  page.value = newPage
  loadOrders()
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

const goToOrder = (row) => {
  router.push({ name: 'CrmOrderDetail', params: { id: row.id } })
}

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

const orderBadgeClass = (status) => {
  if (status === 'paid' || status === 'completed') return 'badge-success'
  if (status === 'cancelled' || status === 'refunded') return 'badge-danger'
  return 'badge-warn'
}

const paymentBadgeClass = (status) => {
  if (status === 'approved') return 'badge-success'
  if (status === 'rejected' || status === 'cancelled' || status === 'refunded') return 'badge-danger'
  return 'badge-warn'
}

const exportParams = computed(() => ({
  search: search.value || undefined,
  status: statusFilter.value || undefined,
  payment_status: paymentStatusFilter.value || undefined,
  date_from: dateFrom.value || undefined,
  date_to: dateTo.value || undefined,
}))

onMounted(loadOrders)
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
  flex: 1; min-width: 220px;
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
.cell-products {
  display: inline-block; max-width: 220px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-size: 13.5px; color: #3a342e;
}
.cell-money {
  font-family: 'Playfair Display', serif;
  font-size: 15px; color: #8e1519;
}
.method {
  font-size: 12px; text-transform: uppercase;
  letter-spacing: 0.5px; color: #6f655c;
  background: #f0ede8; padding: 3px 8px; border-radius: 999px;
}
.mono {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 12.5px; color: #8e1519;
}

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