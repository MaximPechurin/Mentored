<template>
  <div class="crm-order">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando pedido...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmOrders' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <template v-else-if="order">
      <!-- Хлебные крошки -->
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmOrders' }">Pedidos</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ order.order_number }}</span>
      </nav>

      <!-- Хедер -->
      <header class="crm-header-card">
        <div class="crm-header-main">
          <div class="crm-header-info">
            <h1 class="crm-header-name mono">{{ order.order_number }}</h1>
            <div class="crm-header-meta">
              <span class="badge" :class="orderBadgeClass(order.status)">
                {{ order.status_display }}
              </span>
              <span class="crm-meta-item">
                📅 {{ formatDateTime(order.created_at) }}
              </span>
              <span v-if="order.paid_at" class="crm-meta-item crm-meta-item--success">
                ✓ Pagado: {{ formatDateTime(order.paid_at) }}
              </span>
              <span class="crm-meta-item">
                💵 <strong>${{ order.total }}</strong> {{ order.currency }}
              </span>
            </div>
          </div>
        </div>
        <div class="crm-header-actions">
          <a
            :href="`/admin/mentored/order/${order.id}/change/`"
            target="_blank"
            class="crm-btn crm-btn-outline"
          >
            Django admin →
          </a>
        </div>
      </header>

      <!-- Cliente -->
      <CrmDetailSection title="Cliente">
        <div class="crm-client">
          <div class="crm-avatar-lg">
            {{ order.client.username.charAt(0).toUpperCase() }}
          </div>
          <div class="crm-client-info">
            <div class="crm-client-name">{{ order.client.username }}</div>
            <div class="crm-client-contacts">
              <a :href="`mailto:${order.client.email}`" class="crm-meta-item">
                ✉ {{ order.client.email }}
              </a>
              <span v-if="order.client.phone" class="crm-meta-item">
                📞 {{ order.client.phone }}
              </span>
            </div>
            <router-link
              :to="{ name: 'CrmStudentDetail', params: { id: order.client.id } }"
              class="crm-btn crm-btn-outline crm-btn-sm"
            >
              Ver perfil del alumno →
            </router-link>
          </div>
        </div>
      </CrmDetailSection>

      <!-- Productos -->
      <CrmDetailSection title="Productos" :count="order.items.length">
        <table class="crm-table-inner">
          <thead>
            <tr>
              <th>Producto</th>
              <th class="align-center">Cantidad</th>
              <th class="align-right">Precio</th>
              <th class="align-right">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td>
                <div class="crm-item-name">{{ item.product_name }}</div>
                <div v-if="item.product_type" class="crm-item-type">
                  {{ item.product_type }}
                </div>
              </td>
              <td class="align-center">{{ item.quantity }}</td>
              <td class="align-right">${{ item.price }}</td>
              <td class="align-right"><strong>${{ item.total }}</strong></td>
            </tr>
          </tbody>
        </table>
      </CrmDetailSection>

      <!-- Totales -->
      <CrmDetailSection title="Totales">
        <div class="crm-totals">
          <div v-if="order.subtotal" class="crm-total-row">
            <span>Subtotal</span>
            <span>${{ order.subtotal }}</span>
          </div>
          <div class="crm-total-row">
            <span>Impuestos</span>
            <span>${{ order.tax }}</span>
          </div>
          <div class="crm-total-row">
            <span>Envío</span>
            <span>${{ order.shipping }}</span>
          </div>
          <div class="crm-total-row crm-total-row--main">
            <span>Total</span>
            <span>${{ order.total }} {{ order.currency }}</span>
          </div>
        </div>
      </CrmDetailSection>

      <!-- Pago -->
      <CrmDetailSection title="Pago">
        <div v-if="!order.payment" class="crm-empty">
          Sin información de pago.
        </div>
        <div v-else class="crm-payment">
          <div class="crm-payment-row">
            <span class="crm-payment-label">Estado</span>
            <span class="badge" :class="paymentBadgeClass(order.payment.status)">
              {{ order.payment.status_display || order.payment.status }}
            </span>
          </div>
          <div v-if="order.payment.method" class="crm-payment-row">
            <span class="crm-payment-label">Método</span>
            <span class="method">{{ order.payment.method }}</span>
          </div>
          <div v-if="order.payment.transaction_id" class="crm-payment-row">
            <span class="crm-payment-label">ID transacción</span>
            <span class="mono">{{ order.payment.transaction_id }}</span>
          </div>
          <div v-if="order.payment.amount" class="crm-payment-row">
            <span class="crm-payment-label">Monto</span>
            <span><strong>${{ order.payment.amount }}</strong></span>
          </div>
          <div v-if="order.payment.paid_at" class="crm-payment-row">
            <span class="crm-payment-label">Fecha de pago</span>
            <span>{{ formatDateTime(order.payment.paid_at) }}</span>
          </div>
        </div>
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
const order = ref(null)

const loadOrder = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getOrder(route.params.id)
    order.value = res.data
  } catch (e) {
    console.error('Error loading order:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la información del pedido.'
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

onMounted(loadOrder)
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
.crm-header-name {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600; color: #15110f;
  margin: 0 0 12px;
}
.mono {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 22px;
}
.crm-header-meta {
  display: flex; gap: 16px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c; align-items: center;
}
.crm-meta-item { color: #6f655c; text-decoration: none; }
.crm-meta-item--success { color: #1f7a3d; font-weight: 500; }
a.crm-meta-item:hover { color: #8e1519; }
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
.crm-btn-sm { font-size: 13px; padding: 7px 14px; }

/* ===== Клиент ===== */
.crm-client {
  display: flex; align-items: center; gap: 18px;
  padding: 20px 24px;
}
.crm-avatar-lg {
  width: 64px; height: 64px; border-radius: 50%;
  background: #8e1519; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600;
  flex-shrink: 0;
}
.crm-client-info {
  display: flex; flex-direction: column; gap: 8px;
}
.crm-client-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px; font-weight: 600; color: #15110f;
}
.crm-client-contacts {
  display: flex; gap: 14px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c;
}

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
.crm-item-name { font-weight: 600; color: #15110f; }
.crm-item-type {
  font-size: 11.5px; text-transform: uppercase;
  letter-spacing: 0.5px; color: #8a8079; margin-top: 2px;
}

.align-right { text-align: right; }
.align-center { text-align: center; }

/* ===== Totales ===== */
.crm-totals {
  padding: 20px 24px;
  display: flex; flex-direction: column; gap: 10px;
  max-width: 400px; margin-left: auto;
}
.crm-total-row {
  display: flex; justify-content: space-between;
  font-size: 14.5px; color: #5d544c;
}
.crm-total-row--main {
  border-top: 1px solid #ece7e1;
  padding-top: 12px; margin-top: 6px;
  font-size: 18px; font-weight: 700; color: #15110f;
  font-family: 'Playfair Display', serif;
}

/* ===== Pago ===== */
.crm-payment {
  padding: 20px 24px;
  display: flex; flex-direction: column; gap: 14px;
}
.crm-payment-row {
  display: flex; align-items: center; gap: 16px;
  font-size: 14.5px;
}
.crm-payment-label {
  min-width: 140px; color: #8a8079;
  font-size: 12px; text-transform: uppercase;
  letter-spacing: 0.5px; font-weight: 600;
}

.method {
  font-size: 12px; text-transform: uppercase;
  letter-spacing: 0.5px; color: #6f655c;
  background: #f0ede8; padding: 3px 8px; border-radius: 999px;
}
.mono-sm {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 13px; color: #8e1519;
}

/* ===== Бейджи ===== */
.badge {
  display: inline-block; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-success { background: #eaf5ed; color: #1f7a3d; }
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-warn { background: #fff5e0; color: #8c6a10; }

.crm-empty {
  color: #a59c93; font-size: 15px;
  padding: 32px 24px; text-align: center;
}
</style>