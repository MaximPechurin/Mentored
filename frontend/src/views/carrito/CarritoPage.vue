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
import { cartApi } from '../../api/cart'
const items = ref([])
const loading = ref(true)


const loadCart = async () => {
  loading.value = true
  try {
    const response = await cartApi.getCart()
    items.value = response.data.items || []
  } catch (error) {
    console.error('Ошибка загрузки корзины:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

const updateQuantity = async (itemId, quantity) => {
  try {
    await cartApi.updateItem(itemId, quantity)
    await loadCart()
  } catch (error) {
    console.error('Ошибка обновления:', error)
  }
}

const removeItem = async (itemId) => {
  try {
    await cartApi.removeItem(itemId)
    await loadCart()
  } catch (error) {
    console.error('Ошибка удаления:', error)
  }
}

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