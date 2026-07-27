<template>
  <section class="cr-sec">
    <div class="cart-grid">
      <!-- Список товаров -->
      <div class="cart-items">
        <div
          v-for="item in items"
          :key="item.id"
          class="cart-row"
        >
          <div class="cart-img">
            <img :src="item.img" :alt="item.title">
          </div>
          <div class="cart-info">
            <span class="cart-category">{{ item.category }}</span>
            <h3 class="cart-title">{{ item.title }}</h3>
            <span class="cart-price">{{ item.price }} c/u</span>
          </div>
          <div class="cart-qty">
            <button @click="updateQuantity(item.id, item.qty - 1)" class="qty-btn">−</button>
            <span class="qty-value">{{ item.qty }}</span>
            <button @click="updateQuantity(item.id, item.qty + 1)" class="qty-btn">+</button>
          </div>
          <div class="cart-line-total">
            <span class="cart-total-price">{{ formatPrice(item.priceNum * item.qty) }}</span>
          </div>
          <button @click="removeItem(item.id)" class="cart-remove" aria-label="Eliminar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>

        <router-link to="/tienda" class="cart-continue">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          Seguir comprando
        </router-link>
      </div>

      <!-- Сводка -->
      <div class="cart-summary">
        <h3 class="summary-title">Resumen</h3>
        <div class="summary-row">
          <span>Subtotal ({{ totalItems }})</span>
          <span class="summary-value">{{ subtotal }}</span>
        </div>
        <div class="summary-row">
          <span>Impuestos</span>
          <span>Calculado al pagar</span>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-total">
          <span class="total-label">Total</span>
          <span class="total-price">{{ subtotal }}</span>
        </div>
        <button @click="handleCheckout" class="checkout-btn" :disabled="loading">
          <span v-if="!loading">Finalizar compra</span>
          <span v-else>Cargando...</span>
          <svg v-if="!loading" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </button>
        <button @click="clearCart" class="clear-btn">Vaciar carrito</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { orderApi } from '../../api/orders'

const router = useRouter()

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update-quantity', 'remove-item', 'clear-cart'])

const loading = ref(false)

const totalItems = computed(() => {
  return props.items.reduce((sum, item) => sum + item.qty, 0)
})

const subtotal = computed(() => {
  const total = props.items.reduce((sum, item) => sum + (item.priceNum * item.qty), 0)
  return formatPrice(total)
})

const formatPrice = (amount) => {
  return '$' + amount.toFixed(2)
}

const updateQuantity = (id, qty) => {
  emit('update-quantity', id, qty)
}

const removeItem = (id) => {
  emit('remove-item', id)
}

const clearCart = () => {
  emit('clear-cart')
}

// ===== ОСНОВНАЯ ЛОГИКА =====
const handleCheckout = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const response = await orderApi.createOrder()
    const orderNumber = response.data.order_number

    // Очищаем корзину (без confirm)
    emit('clear-cart')

    // Редирект на страницу заказа
    router.push(`/order/${orderNumber}`)
  } catch (error) {
    console.error('Ошибка создания заказа:', error)
    // 401 обрабатывает глобальный interceptor в api/index.js (редирект на
    // /login) - blocking alert() тут сбивал бы этот редирект, см. аналогичный
    // фикс в TiendaGrid.vue/ProductoPage.vue.
    if (error.response?.status !== 401) {
      alert('Error al crear el pedido. Inténtalo de nuevo.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.cr-sec {
  padding: 56px 32px 96px;
}

.cart-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 36px;
  align-items: start;
}

/* --- Список товаров --- */
.cart-items {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.cart-row {
  background: #ffffff;
  border-radius: 18px;
  padding: 18px;
  display: flex;
  gap: 20px;
  align-items: center;
  box-shadow: 0 18px 44px -34px rgba(0,0,0,0.4);
}

.cart-img {
  width: 128px;
  height: 88px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: #1a1212;
}

.cart-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.cart-info {
  flex: 1;
  min-width: 0;
}

.cart-category {
  display: block;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 6px;
}

.cart-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  line-height: 1.2;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 6px;
}

.cart-price {
  font-size: 15px;
  color: #8a8079;
}

/* --- Количество --- */
.cart-qty {
  display: flex;
  align-items: center;
  gap: 0;
  border: 1px solid #e4d8c8;
  border-radius: 999px;
  overflow: hidden;
  flex-shrink: 0;
}

.qty-btn {
  border: none;
  background: #fff;
  cursor: pointer;
  width: 40px;
  height: 40px;
  font-size: 20px;
  color: #3a332e;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.qty-btn:hover {
  background: #f0ece4;
}

.qty-value {
  min-width: 36px;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: #15110f;
}

/* --- Итог по строке --- */
.cart-line-total {
  width: 108px;
  text-align: right;
  flex-shrink: 0;
}

.cart-total-price {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 800;
  color: #8e1519;
}

/* --- Удалить --- */
.cart-remove {
  border: none;
  background: none;
  cursor: pointer;
  color: #b8aea2;
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.cart-remove:hover {
  color: #8e1519;
}

/* --- Продолжить --- */
.cart-continue {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #8e1519;
  font-weight: 600;
  font-size: 16px;
  margin-top: 6px;
}

/* --- Сводка --- */
.cart-summary {
  background: #ffffff;
  border-radius: 18px;
  padding: 30px;
  box-shadow: 0 18px 44px -34px rgba(0,0,0,0.4);
  position: sticky;
  top: 104px;
}

.summary-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 22px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 16px;
  color: #6b6259;
  margin-bottom: 14px;
}

.summary-value {
  font-weight: 600;
  color: #15110f;
}

.summary-divider {
  height: 1px;
  background: #ece3d6;
  margin-bottom: 20px;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 26px;
}

.total-label {
  font-size: 18px;
  font-weight: 600;
  color: #15110f;
}

.total-price {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 800;
  color: #8e1519;
}

.checkout-btn {
  width: 100%;
  border: none;
  cursor: pointer;
  background: #8e1519;
  color: #fff;
  font-family: inherit;
  font-size: 18px;
  font-weight: 600;
  padding: 17px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: background 0.3s;
}

.checkout-btn:hover {
  background: #a01a1f;
}

.clear-btn {
  width: 100%;
  border: none;
  background: none;
  cursor: pointer;
  color: #a89f93;
  font-family: inherit;
  font-size: 15px;
  margin-top: 16px;
  transition: color 0.3s;
}

.clear-btn:hover {
  color: #8e1519;
}

@media (max-width: 860px) {
  .cr-sec { padding: 40px 20px 64px !important; }
  .cart-grid { grid-template-columns: 1fr !important; gap: 24px !important; }
  .cart-row { flex-wrap: wrap !important; }
  .cart-line-total { width: auto !important; flex: 1; }
}
</style>