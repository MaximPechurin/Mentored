<template>
  <div class="carrito-page">
    <CarritoHero />
    <CarritoEmpty v-if="items.length === 0" />
    <CarritoContent
      v-else
      :items="items"
      @update-quantity="updateQuantity"
      @remove-item="removeItem"
      @clear-cart="clearCart"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CarritoHero from './CarritoHero.vue'
import CarritoEmpty from './CarritoEmpty.vue'
import CarritoContent from './CarritoContent.vue'

const items = ref([])

const loadCart = () => {
  try {
    const saved = localStorage.getItem('mentored_cart')
    if (saved) {
      items.value = JSON.parse(saved)
    }
  } catch (e) {
    console.error('Ошибка загрузки корзины:', e)
  }
}

const saveCart = (data) => {
  try {
    localStorage.setItem('mentored_cart', JSON.stringify(data))
  } catch (e) {
    console.error('Ошибка сохранения корзины:', e)
  }
}

const updateQuantity = (id, qty) => {
  const item = items.value.find(i => i.id === id)
  if (!item) return
  if (qty <= 0) {
    removeItem(id)
    return
  }
  item.qty = qty
  saveCart(items.value)
}

const removeItem = (id) => {
  items.value = items.value.filter(i => i.id !== id)
  saveCart(items.value)
}

const clearCart = () => {
  items.value = []
  saveCart(items.value)
}

onMounted(() => {
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