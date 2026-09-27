<template>
  <div class="ce-page">
    <div class="ce-card">
      <template v-if="checking">
        <div class="ce-icon ce-icon--pending">…</div>
        <h1 class="ce-title">Verificando tu pago…</h1>
        <p class="ce-text">Un momento, estamos confirmando el estado con Mercado Pago.</p>
      </template>

      <template v-else-if="displayStatus === 'success'">
        <div class="ce-icon ce-icon--ok">✓</div>
        <h1 class="ce-title">¡Pago recibido!</h1>

        <p v-if="isNew" class="ce-text">
          Hemos creado tu cuenta y te enviamos la <strong>contraseña a tu correo</strong>.
          Ya puedes iniciar sesión y acceder a tu curso.
        </p>
        <p v-else class="ce-text">
          Tu compra se realizó con éxito. Inicia sesión con tu cuenta para
          acceder a tu curso.
        </p>

        <router-link to="/login" class="ce-btn">Iniciar sesión</router-link>
        <p class="ce-note">
          El acceso al curso se activa automáticamente tras confirmar el pago.
          Si no ves el correo, revisa la carpeta de spam.
        </p>
      </template>

      <template v-else-if="displayStatus === 'pending'">
        <div class="ce-icon ce-icon--pending">…</div>
        <h1 class="ce-title">Pago en proceso</h1>
        <p v-if="pollExhausted" class="ce-text">
          Tu pago sigue en verificación con Mercado Pago. Si ya pagaste, no te
          preocupes: en cuanto se confirme activaremos tu acceso automáticamente
          y te enviaremos los datos por correo. Si tarda demasiado, escríbenos.
        </p>
        <p v-else class="ce-text">
          Tu pago se está procesando. En cuanto se confirme, activaremos tu
          acceso y te enviaremos los datos por correo.
        </p>
        <router-link to="/" class="ce-btn ce-btn--ghost">Volver al inicio</router-link>
      </template>

      <template v-else>
        <div class="ce-icon ce-icon--fail">✕</div>
        <h1 class="ce-title">El pago no se completó</h1>
        <p class="ce-text">
          No se pudo procesar tu pago. Puedes intentarlo de nuevo desde el
          enlace de compra.
        </p>
        <router-link to="/" class="ce-btn ce-btn--ghost">Volver al inicio</router-link>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { paymentApi } from '../../api/payments'

const route = useRoute()
const isNew = computed(() => route.query.new === '1')

// El parámetro ?status=... de la URL es solo una foto del momento del
// redirect de Mercado Pago (back_urls en QuickBuyView) - NO el estado final
// real. El mismo bug que en OrderPage.vue: si el webhook confirma el pago
// unos segundos después de que esta página ya se cargó, se quedaba
// mostrando "pago no completado" para siempre aunque el dinero ya se
// hubiera cobrado. Ahora, si tenemos el número de pedido en la URL,
// consultamos el estado REAL (endpoint público - el comprador es un
// invitado sin sesión) y lo sondeamos mientras siga pendiente.
const orderNumber = route.query.order
const realStatus = ref(null) // status crudo del pedido (pending/paid/...) o null si no se pudo consultar
const checking = ref(!!orderNumber)
const pollExhausted = ref(false)

const mapRealStatus = (status) => {
  if (['paid', 'processing', 'completed'].includes(status)) return 'success'
  if (['cancelled', 'refunded'].includes(status)) return 'failure'
  if (status === 'pending') return 'pending'
  return null
}

const displayStatus = computed(() => {
  const mapped = realStatus.value ? mapRealStatus(realStatus.value) : null
  if (mapped) return mapped
  // Sin order_number (enlace viejo) o la consulta falló - usamos la URL como antes.
  return route.query.status || 'success'
})

let pollTimer = null
let pollAttempts = 0
const MAX_POLL_ATTEMPTS = 10

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const fetchStatus = async () => {
  try {
    const { data } = await paymentApi.quickBuyOrderStatus(orderNumber)
    realStatus.value = data.status
  } catch (error) {
    console.error('Error al consultar el estado del pedido:', error)
  }
}

onMounted(async () => {
  if (!orderNumber) return
  await fetchStatus()
  checking.value = false
  if (mapRealStatus(realStatus.value) === 'pending') {
    pollTimer = setInterval(async () => {
      pollAttempts += 1
      await fetchStatus()
      if (mapRealStatus(realStatus.value) !== 'pending' || pollAttempts >= MAX_POLL_ATTEMPTS) {
        if (pollAttempts >= MAX_POLL_ATTEMPTS) pollExhausted.value = true
        stopPolling()
      }
    }, 3000)
  }
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.ce-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  background: #f5eee3;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
}

.ce-card {
  width: 100%;
  max-width: 520px;
  background: #fff;
  border-radius: 20px;
  padding: 44px 36px 38px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.ce-icon {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  font-weight: 700;
  margin: 0 auto 20px;
}
.ce-icon--ok { background: #e7f3ea; color: #2f7a3a; }
.ce-icon--pending { background: #fff4e0; color: #9a6a00; }
.ce-icon--fail { background: #fbe9e9; color: #8e1519; }

.ce-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 14px;
}

.ce-text {
  font-size: 15.5px;
  line-height: 1.6;
  color: #514b45;
  margin: 0 0 24px;
}
.ce-text strong { color: #15110f; }

.ce-btn {
  display: inline-block;
  background: #8e1519;
  color: #fff;
  border-radius: 999px;
  font-weight: 700;
  font-size: 15.5px;
  padding: 13px 30px;
  text-decoration: none;
  transition: background 0.15s;
}
.ce-btn:hover { background: #a01a1f; }
.ce-btn--ghost { background: #fff; color: #8e1519; border: 1px solid #e2b8b8; }
.ce-btn--ghost:hover { background: #fbe9e9; }

.ce-note { font-size: 13px; color: #8a8079; margin: 18px 0 0; line-height: 1.5; }
</style>
