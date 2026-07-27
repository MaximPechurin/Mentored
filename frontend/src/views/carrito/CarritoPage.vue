<template>
  <div class="carrito-page">
    <CarritoHero />
    <div v-if="loading" class="cr-loading">
      <div class="cr-loading-spinner"></div>
      <p>Cargando carrito...</p>
    </div>
    <template v-else>
      <CarritoEmpty v-if="items.length === 0" />
      <CarritoContent
        v-else
        :items="items"
        @update-quantity="updateQuantity"
        @remove-item="removeItem"
        @clear-cart="clearCart"
      />
    </template>
  </div>
</template>

<script setup>
console.log(' CARRIOT PAGE SCRIPT ЗАГРУЗИЛСЯ!')

import { ref, computed, onMounted } from 'vue'
import CarritoHero from './CarritoHero.vue'
import CarritoEmpty from './CarritoEmpty.vue'
import CarritoContent from './CarritoContent.vue'
import { cartApi } from '../../api/cart'

const items = ref([])
const loading = ref(true)

// ===== ЗАГРУЗКА КОРЗИНЫ =====
const loadCart = async () => {
  loading.value = true
  try {
    const response = await cartApi.getCart()
    const cartData = response.data

    // 👇 ТРАНСФОРМИРУЕМ ДАННЫЕ
    items.value = (cartData.items || []).map(item => ({
      id: item.id,
      // Определяем категорию по product_type
      category: item.product_type === 'course' ? 'Cursos' :
                item.product_type === 'book' ? 'Libros' :
                item.product_type === 'consultation' ? 'Consultas' :
                item.product_type === 'membership' ? 'Comunidad' : 'Producto',
      title: item.product_name || 'Producto',
      price: `S/ ${Number(item.product_price).toFixed(2)}`,
      priceNum: Number(item.product_price),
      qty: item.quantity || 1,
      img: item.product_image || '/images/placeholder.png',
    }))

    console.log('✅ Корзина загружена:', items.value)

  } catch (error) {
    console.error('❌ Ошибка загрузки корзины:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

// ===== ОБНОВЛЕНИЕ КОЛИЧЕСТВА =====
const updateQuantity = async (itemId, quantity) => {
  if (quantity <= 0) {
    await removeItem(itemId)
    return
  }
  try {
    await cartApi.updateItem(itemId, quantity)
    await loadCart()
  } catch (error) {
    console.error('Ошибка обновления:', error)
  }
}

// ===== УДАЛЕНИЕ ТОВАРА =====
const removeItem = async (itemId) => {
  try {
    await cartApi.removeItem(itemId)
    await loadCart()
  } catch (error) {
    console.error('Ошибка удаления:', error)
  }
}

// ===== ОЧИСТКА КОРЗИНЫ =====
const clearCart = async () => {
  if (confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
    try {
      await cartApi.clearCart()
      await loadCart()
    } catch (error) {
      console.error('Ошибка очистки:', error)
    }
  }
}

onMounted(() => {
  console.log('🟢 CarritoPage mounted')
  loadCart()
})
</script>

<style scoped>
.carrito-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f5eee3;
  min-height: 100vh;
}
</style>