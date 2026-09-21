<template>
  <div class="cr-page">
    <div v-if="loading" class="cr-state">Cargando…</div>

    <div v-else-if="notFound" class="cr-state">
      <h1 class="cr-state-title">Producto no disponible</h1>
      <p>Este enlace de compra no es válido o el producto ya no está activo.</p>
      <router-link to="/tienda" class="cr-link">Ir a la tienda</router-link>
    </div>

    <div v-else class="cr-card">
      <div v-if="product.image" class="cr-media">
        <img :src="product.image" :alt="product.name" />
      </div>

      <div class="cr-body">
        <p class="cr-eyebrow">Compra rápida</p>
        <h1 class="cr-title">{{ product.name }}</h1>

        <p v-if="product.short_description || product.description" class="cr-desc">
          {{ product.short_description || product.description }}
        </p>

        <div class="cr-price">
          <span class="cr-price-now">S/ {{ product.price }}</span>
          <span v-if="hasDiscount" class="cr-price-old">S/ {{ product.old_price }}</span>
        </div>

        <form class="cr-form" @submit.prevent="comprar">
          <label class="cr-label" for="cr-email">Tu correo electrónico</label>
          <input
            id="cr-email"
            v-model="email"
            type="email"
            class="cr-input"
            placeholder="tucorreo@ejemplo.com"
            :disabled="submitting"
            required
          />
          <p class="cr-hint">
            No necesitas registrarte. Crearemos tu cuenta automáticamente y te
            enviaremos el acceso a este correo.
          </p>

          <p v-if="error" class="cr-error">{{ error }}</p>

          <button type="submit" class="cr-btn" :disabled="submitting">
            {{ submitting ? 'Redirigiendo al pago…' : 'Comprar ahora' }}
          </button>
        </form>

        <p class="cr-secure">🔒 Pago seguro con Mercado Pago</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { paymentApi } from '../../api/payments'

const route = useRoute()

const loading = ref(true)
const notFound = ref(false)
const product = ref({})
const productType = ref(route.params.productType)

const email = ref('')
const submitting = ref(false)
const error = ref('')

const hasDiscount = computed(() => {
  const old = parseFloat(product.value.old_price)
  const now = parseFloat(product.value.price)
  return !isNaN(old) && old > now
})

const comprar = async () => {
  if (!email.value.trim()) return
  submitting.value = true
  error.value = ''
  try {
    const { data } = await paymentApi.quickBuy({
      product_type: productType.value,
      slug: route.params.slug,
      email: email.value.trim(),
    })
    // Уводим на страницу оплаты Mercado Pago.
    window.location.href = data.init_point
  } catch (e) {
    error.value = e.response?.data?.error || 'No se pudo iniciar la compra. Inténtalo de nuevo.'
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await paymentApi.quickBuyProduct(route.params.productType, route.params.slug)
    product.value = data.product
    productType.value = data.product_type
  } catch (e) {
    notFound.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cr-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  background: #f5eee3;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
}

.cr-state {
  text-align: center;
  color: #6b6259;
  max-width: 460px;
}
.cr-state-title {
  font-family: 'Playfair Display', serif;
  color: #1c1c1c;
  margin-bottom: 12px;
}
.cr-link {
  display: inline-block;
  margin-top: 16px;
  color: #8e1519;
  font-weight: 600;
  text-decoration: none;
}

.cr-card {
  width: 100%;
  max-width: 640px;
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.cr-media { width: 100%; max-height: 280px; overflow: hidden; }
.cr-media img { width: 100%; height: 100%; object-fit: cover; display: block; }

.cr-body { padding: 32px 34px 34px; }

.cr-eyebrow {
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 8px;
}

.cr-title {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  line-height: 1.15;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 14px;
}

.cr-desc {
  font-size: 15px;
  line-height: 1.6;
  color: #514b45;
  margin: 0 0 20px;
  white-space: pre-line;
}

.cr-price { display: flex; align-items: baseline; gap: 12px; margin-bottom: 24px; }
.cr-price-now { font-size: 30px; font-weight: 700; color: #15110f; }
.cr-price-old { font-size: 18px; color: #a49a8e; text-decoration: line-through; }

.cr-form { display: flex; flex-direction: column; }

.cr-label { font-size: 14px; font-weight: 600; color: #3f3a35; margin-bottom: 8px; }

.cr-input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e4ddd2;
  border-radius: 12px;
  padding: 14px 16px;
  font-family: inherit;
  font-size: 15px;
  color: #15110f;
  background: #fbf9f6;
  outline: none;
}
.cr-input:focus { border-color: #8e1519; }

.cr-hint { font-size: 13px; color: #8a8079; margin: 10px 0 0; line-height: 1.5; }

.cr-error { color: #8e1519; font-size: 14px; margin: 14px 0 0; }

.cr-btn {
  margin-top: 22px;
  background: #8e1519;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 700;
  font-size: 16px;
  padding: 15px 24px;
  cursor: pointer;
  transition: background 0.15s;
}
.cr-btn:hover { background: #a01a1f; }
.cr-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.cr-secure { text-align: center; font-size: 13px; color: #8a8079; margin: 18px 0 0; }

@media (max-width: 620px) {
  .cr-body { padding: 26px 22px 28px; }
  .cr-title { font-size: 25px; }
}
</style>
