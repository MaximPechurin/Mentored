<template>
  <div>
    <h2 class="ac-section-title">Mis pedidos</h2>

    <div v-if="loading" class="ac-orders-loading">Cargando pedidos...</div>

    <div v-else-if="error" class="ac-orders-error">
      No se pudieron cargar tus pedidos. Inténtalo de nuevo más tarde.
    </div>

    <div v-else-if="orders.length === 0" class="ac-orders-empty">
      Todavía no tenés pedidos.
    </div>

    <div v-else class="ac-orders">
      <router-link
        v-for="order in orders"
        :key="order.id"
        :to="`/order/${order.order_number}`"
        class="ac-order"
      >
        <div>
          <div class="ac-order-header">
            <span class="ac-order-id">#{{ order.order_number }}</span>
            <span class="ac-order-status" :style="statusStyle(order.status)">{{ statusLabel(order.status) }}</span>
          </div>
          <div class="ac-order-title">{{ itemsSummary(order) }}</div>
          <div class="ac-order-date">{{ formatDate(order.created_at) }}</div>
        </div>
        <div class="ac-order-total">{{ formatPrice(order.total) }}</div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../../api/orders'

const orders = ref([])
const loading = ref(true)
const error = ref(false)

const STATUS_LABELS = {
  pending: 'Pendiente',
  paid: 'Pagado',
  processing: 'En procesamiento',
  completed: 'Completado',
  cancelled: 'Cancelado',
  refunded: 'Reembolsado',
}

const STATUS_STYLES = {
  paid: 'color:#1f7a44;background:#e7f4ec;',
  completed: 'color:#1f7a44;background:#e7f4ec;',
  processing: 'color:#8a5a00;background:#fbf0d9;',
  pending: 'color:#8a5a00;background:#fbf0d9;',
  cancelled: 'color:#8e1519;background:#f7e3e3;',
  refunded: 'color:#8e1519;background:#f7e3e3;',
}

const BADGE_BASE = 'display:inline-block;font-size:12px;font-weight:600;letter-spacing:0.4px;padding:3px 10px;border-radius:999px;'

const statusLabel = (status) => STATUS_LABELS[status] || status
const statusStyle = (status) => BADGE_BASE + (STATUS_STYLES[status] || '')

const itemsSummary = (order) => {
  const items = order.items || []
  if (items.length === 0) return 'Pedido'
  if (items.length === 1) return items[0].product_name
  return `${items[0].product_name} y ${items.length - 1} más`
}

const formatPrice = (amount) => {
  if (!amount) return '$0.00'
  return `$${Number(amount).toFixed(2)}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })
}

const loadOrders = async () => {
  loading.value = true
  error.value = false
  try {
    const response = await orderApi.listOrders()
    orders.value = response.data
  } catch (err) {
    console.error('Ошибка загрузки заказов:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(loadOrders)
</script>

<style scoped>
.ac-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.ac-orders-loading,
.ac-orders-error,
.ac-orders-empty {
  color: #8a8079;
  font-size: 16px;
  padding: 24px 0;
}

.ac-orders {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ac-order {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 24px 26px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  text-decoration: none;
  transition: border-color 0.2s;
}

.ac-order:hover {
  border-color: #cfc6ba;
}

.ac-order-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}

.ac-order-id {
  font-size: 14px;
  font-weight: 600;
  color: #15110f;
}

.ac-order-status {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.4px;
  padding: 3px 10px;
  border-radius: 999px;
}

.ac-order-title {
  font-size: 16px;
  color: #15110f;
  font-weight: 400;
  margin-bottom: 3px;
}

.ac-order-date {
  font-size: 14px;
  color: #a59c93;
}

.ac-order-total {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #15110f;
  text-align: right;
}

@media (max-width: 920px) {
  .ac-order { flex-wrap: wrap !important; }
}
</style>
