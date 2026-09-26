<template>
  <div class="order-page">
    <div class="order-container">
      <!-- Загрузка -->
      <div v-if="loading" class="order-loading">
        <div class="order-loading-spinner"></div>
        <p>Cargando información del pedido...</p>
      </div>

      <!-- Успех -->
      <template v-else-if="order">
        <div class="order-success">
          <div class="order-icon">🎉</div>
          <h1 class="order-title">¡Pedido creado con éxito!</h1>
          <p class="order-number">
            Número de pedido: <strong>#{{ order.order_number }}</strong>
          </p>

          <div v-if="paymentBanner" :class="['order-payment-banner', paymentBanner.type]">
            {{ paymentBanner.text }}
          </div>

          <div class="order-details">
            <div class="order-summary">
              <div class="order-row">
                <span>Estado</span>
                <span class="order-status">{{ getStatusLabel(order.status) }}</span>
              </div>
              <div class="order-row">
                <span>Total</span>
                <span class="order-total">{{ formatPrice(order.total) }}</span>
              </div>
              <div class="order-row">
                <span>Fecha</span>
                <span>{{ formatDate(order.created_at) }}</span>
              </div>
            </div>

            <div class="order-items">
              <h3>Productos</h3>
              <div
                v-for="item in order.items"
                :key="item.id"
                class="order-item"
              >
                <span class="order-item-name">{{ item.product_name }}</span>
                <span class="order-item-qty">x{{ item.quantity }}</span>
                <span class="order-item-price">{{ formatPrice(item.total) }}</span>
              </div>
            </div>
          </div>

          <div class="order-actions">
            <button v-if="order.status === 'pending'" class="order-btn-primary" @click="goToPayment" :disabled="paying">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                <circle cx="12" cy="12" r="4"/>
              </svg>
              {{ paying ? 'Redirigiendo...' : 'Ir a pagar' }}
            </button>
            <router-link to="/cuenta?tab=pedidos" class="order-btn-secondary">
              Ver mis pedidos
            </router-link>
            <router-link to="/tienda" class="order-btn-text">
              Seguir comprando
            </router-link>
          </div>
        </div>
      </template>

      <!-- Ошибка -->
      <div v-else class="order-error">
        <div class="order-error-icon">😕</div>
        <h2>Pedido no encontrado</h2>
        <p>El pedido que buscas no existe o ha sido eliminado.</p>
        <router-link to="/tienda" class="order-btn-primary">
          Volver a la tienda
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderApi } from '../../api/orders'
import { paymentApi } from '../../api/payments'

const route = useRoute()
const router = useRouter()

const order = ref(null)
const loading = ref(true)
const paying = ref(false)
const pollExhausted = ref(false)

// Баннер de resultado de pago - basado en el estado REAL del pedido
// (order.status), no en el parámetro ?payment=... de la URL. Ese parámetro
// es solo una foto del momento del redirect de Mercado Pago y puede quedar
// desactualizado: el webhook que confirma el pago (backend/payments/views.py
// payment_webhook) suele llegar en segundos, pero si aún no llegó cuando se
// cargó esta página, antes se mostraba para siempre "pago no completado"
// aunque el dinero ya se hubiera cobrado - de ahí el bug reportado por
// usuarias reales. Ahora se sondea el pedido (pollOrderStatus) mientras siga
// "pending" y venimos de un redirect de MP.
const paymentBanner = computed(() => {
  if (!order.value) return null
  const status = order.value.status

  if (['paid', 'processing', 'completed'].includes(status)) {
    return { type: 'success', text: '¡Pago recibido! Gracias por tu compra.' }
  }
  if (['cancelled', 'refunded'].includes(status)) {
    return { type: 'failure', text: 'El pago no se pudo completar. Podés intentarlo de nuevo.' }
  }
  if (status === 'pending' && route.query.payment) {
    if (pollExhausted.value) {
      return {
        type: 'pending',
        text: 'Tu pago sigue en verificación con Mercado Pago. Si ya pagaste, no te preocupes: '
          + 'en cuanto se confirme verás el acceso automáticamente. Si tarda demasiado, escríbenos.',
      }
    }
    return { type: 'pending', text: 'Estamos confirmando tu pago con Mercado Pago. No cierres esta página...' }
  }
  return null
})

const formatPrice = (amount) => {
  if (!amount) return 'S/ 0.00'
  return `S/ ${Number(amount).toFixed(2)}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getStatusLabel = (status) => {
  const map = {
    pending: 'Pendiente',
    paid: 'Pagado',
    processing: 'En procesamiento',
    completed: 'Completado',
    cancelled: 'Cancelado',
    refunded: 'Reembolsado',
  }
  return map[status] || status
}

// Без переключения loading - используется и при первой загрузке (после
// собственного показа спиннера), и при фоновом опросе (poll), где спиннер на
// весь экран был бы лишним морганием поверх уже показанного заказа.
const fetchOrder = async () => {
  const orderNumber = route.params.orderNumber
  if (!orderNumber) {
    router.push('/tienda')
    return
  }
  try {
    const response = await orderApi.getOrder(orderNumber)
    order.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки заказа:', error)
    order.value = null
  }
}

const loadOrder = async () => {
  loading.value = true
  await fetchOrder()
  loading.value = false
}

const goToPayment = async () => {
  if (paying.value || !order.value) return
  paying.value = true
  try {
    const response = await paymentApi.createPreference(order.value.order_number)
    // init_point - внешний домен Mercado Pago, поэтому обычный редирект,
    // а не router.push (SPA-роутер тут не при делах).
    window.location.href = response.data.init_point
  } catch (error) {
    console.error('Ошибка создания платежа:', error)
    alert('No se pudo iniciar el pago. Inténtalo de nuevo.')
    paying.value = false
  }
}

// Пока webhook не отработал, статус заказа может ненадолго остаться
// "pending" даже после реально успешной оплаты - опрашиваем сервер, вместо
// того чтобы один раз показать (возможно устаревший) статус и забыть.
// Останавливаемся, как только статус перестал быть pending, или после
// разумного числа попыток (10 x 3с = 30с - вебхук почти всегда быстрее).
let pollTimer = null
let pollAttempts = 0
const MAX_POLL_ATTEMPTS = 10

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const startPollingIfNeeded = () => {
  if (!route.query.payment || !order.value || order.value.status !== 'pending') return
  pollTimer = setInterval(async () => {
    pollAttempts += 1
    await fetchOrder()
    if (order.value?.status !== 'pending' || pollAttempts >= MAX_POLL_ATTEMPTS) {
      if (pollAttempts >= MAX_POLL_ATTEMPTS) pollExhausted.value = true
      stopPolling()
    }
  }, 3000)
}

onMounted(async () => {
  await loadOrder()
  startPollingIfNeeded()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.order-page {
  min-height: 100vh;
  background: #f5eee3;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.order-container {
  max-width: 560px;
  width: 100%;
}

/* ===== ЗАГРУЗКА ===== */
.order-loading {
  text-align: center;
  padding: 60px 20px;
  color: #8a8079;
}

.order-loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e4ddd2;
  border-top: 4px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== УСПЕХ ===== */
.order-success {
  background: #ffffff;
  border-radius: 24px;
  padding: 48px 40px 36px;
  text-align: center;
  box-shadow: 0 40px 80px -32px rgba(0, 0, 0, 0.35);
}

.order-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.order-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 8px;
  letter-spacing: -0.3px;
}

.order-number {
  font-size: 16px;
  color: #6b6259;
  margin: 0 0 28px;
}

.order-number strong {
  color: #8e1519;
}

.order-payment-banner {
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 20px;
}

.order-payment-banner.success {
  background: #e6f4ea;
  color: #1f7a3d;
}

.order-payment-banner.pending {
  background: #fdf3e0;
  color: #9a6a00;
}

.order-payment-banner.failure {
  background: #fbe7e8;
  color: #8e1519;
}

/* ===== ДЕТАЛИ ===== */
.order-details {
  text-align: left;
  margin-bottom: 32px;
  border-top: 1px solid #ece3d6;
  padding-top: 20px;
}

.order-summary {
  margin-bottom: 20px;
}

.order-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 16px;
  color: #6b6259;
  border-bottom: 1px solid #f5eee3;
}

.order-row:last-child {
  border-bottom: none;
}

.order-status {
  font-weight: 600;
  color: #1f7a3d;
}

.order-total {
  font-weight: 700;
  color: #15110f;
  font-size: 18px;
}

.order-items h3 {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #15110f;
  margin: 16px 0 12px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 15px;
  color: #5d544c;
  border-bottom: 1px solid #f5eee3;
}

.order-item:last-child {
  border-bottom: none;
}

.order-item-name {
  flex: 1;
}

.order-item-qty {
  margin: 0 16px;
  color: #8a8079;
}

.order-item-price {
  font-weight: 600;
  color: #15110f;
}

/* ===== КНОПКИ ===== */
.order-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #8e1519;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 16px 24px;
  font-size: 17px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.3s;
  text-decoration: none;
}

.order-btn-primary:hover {
  background: #a01a1f;
}

.order-btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f5eee3;
  color: #15110f;
  border: none;
  border-radius: 12px;
  padding: 16px 24px;
  font-size: 17px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.3s;
  text-decoration: none;
}

.order-btn-secondary:hover {
  background: #ece3d6;
}

.order-btn-text {
  background: none;
  border: none;
  color: #8a8079;
  font-size: 15px;
  font-family: inherit;
  cursor: pointer;
  padding: 8px;
  transition: color 0.3s;
  text-decoration: underline;
  text-align: center;
}

.order-btn-text:hover {
  color: #15110f;
}

/* ===== ОШИБКА ===== */
.order-error {
  background: #ffffff;
  border-radius: 24px;
  padding: 48px 40px 36px;
  text-align: center;
  box-shadow: 0 40px 80px -32px rgba(0, 0, 0, 0.35);
}

.order-error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.order-error h2 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 8px;
}

.order-error p {
  font-size: 16px;
  color: #6b6259;
  margin: 0 0 24px;
}

@media (max-width: 520px) {
  .order-success,
  .order-error {
    padding: 32px 24px 28px;
  }
  .order-title {
    font-size: 24px;
  }
}
</style>