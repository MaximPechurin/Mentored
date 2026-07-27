<template>
  <div style="font-family:'Hanken Grotesk',-apple-system,Helvetica,Arial,sans-serif;font-weight:300;color:#1c1c1c;background:#f5eee3;">
    <div class="producto-page">
      <!-- Загрузка -->
      <div v-if="loading" class="pd-loading">
        <div class="pd-loading-spinner"></div>
        <p>Cargando producto...</p>
      </div>

      <!-- Контент -->
      <template v-else-if="product">
        <ProductoBreadcrumb :product="product" />
        <div class="pd-wrap">
          <ProductoMedia :product="product" />
          <ProductoInfo :product="product" @add-to-cart="addToCart" @buy-now="buyNow" />
        </div>
        <ProductoDescription :product="product" />
      </template>

      <!-- Товар не найден -->
      <div v-else class="pd-not-found">
        <h2>Producto no encontrado</h2>
        <router-link to="/tienda" class="pd-back-btn">Volver a la tienda</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {productApi} from '../../api/products'
import {cartApi} from '../../api/cart'
import ProductoBreadcrumb from './ProductoBreadcrumb.vue'
import ProductoMedia from './ProductoMedia.vue'
import ProductoInfo from './ProductoInfo.vue'
import ProductoDescription from './ProductoDescription.vue'

const route = useRoute()
const router = useRouter()

// ===== СОСТОЯНИЕ =====
const loading = ref(true)
const productData = ref(null)

// ===== ЗАГРУЗКА ТОВАРА =====
const loadProduct = async () => {
  const slug = route.params.id
  loading.value = true

  try {
    const response = await productApi.getBySlug(slug)
    productData.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки товара:', error)
    productData.value = null
  } finally {
    loading.value = false
  }
}

// ===== ФОРМАТИРОВАНИЕ ДАННЫХ =====
const product = computed(() => {
  if (!productData.value) return null

  const p = productData.value

  // Определяем тип товара
  let type = 'course'
  let category = 'Cursos'
  let kindWord = 'curso'

  if (p.book_format !== undefined) {
    type = 'book'
    category = 'Книги'
    kindWord = 'libro'
  } else if (p.duration_minutes !== undefined) {
    type = 'consultation'
    category = 'Консультации'
    kindWord = 'servicio'
  } else if (p.cycle !== undefined) {
    type = 'membership'
    category = 'Сообщество'
    kindWord = 'plan'
  }

  // Форматируем цену
  const formatPrice = (price) => {
    if (!price) return 'S/ 0.00'
    return `S/ ${Number(price).toFixed(2)}`
  }

  // Собираем мета-информацию
  const meta = []
  if (type === 'book') {
    if (p.book_format) meta.push({ label: 'Формат', value: p.book_format })
    if (p.pages) meta.push({ label: 'Страниц', value: `${p.pages} страниц` })
    if (p.book_language) meta.push({ label: 'Язык', value: p.book_language })
  } else if (type === 'course') {
    if (p.duration) meta.push({ label: 'Длительность', value: p.duration })
    if (p.lessons) meta.push({ label: 'Уроков', value: p.lessons })
    if (p.video_hours) meta.push({ label: 'Часов видео', value: p.video_hours })
  } else if (type === 'consultation') {
    if (p.duration_minutes) meta.push({ label: 'Длительность', value: `${p.duration_minutes} мин` })
    if (p.expert) meta.push({ label: 'Эксперт', value: p.expert })
    if (p.platform) meta.push({ label: 'Платформа', value: p.platform })
  } else if (type === 'membership') {
    if (p.cycle) meta.push({ label: 'Период', value: p.cycle })
    if (p.cancel_anytime) meta.push({ label: 'Отмена', value: 'В любое время' })
  }

  return {
    id: p.id,
    slug: p.slug,
    category: category,
    kindWord: kindWord,
    title: p.name,
    desc: p.short_description || p.description,
    price: formatPrice(p.price),
    priceNum: parseFloat(p.price),
    oldPrice: p.old_price ? formatPrice(p.old_price) : '',
    hasOld: !!p.old_price,
    img: p.image || '/images/placeholder.png',
    includes: p.includes ? p.includes.split('\n').filter(i => i.trim()) : [],
    meta: meta,
    descHeading: p.description || p.name,
    longDesc: p.long_description ? p.long_description.split('\n').filter(i => i.trim()) : [p.description || ''],
  }
})

// ===== ДОБАВЛЕНИЕ В КОРЗИНУ =====
const addToCart = async () => {
  if (!productData.value) return

  const p = productData.value
  let type = 'course'
  if (p.book_format !== undefined) type = 'book'
  else if (p.duration_minutes !== undefined) type = 'consultation'
  else if (p.cycle !== undefined) type = 'membership'

  try {
    await cartApi.addItem(type, p.id)
    alert('¡Agregado al carrito! 🛒')
  } catch (error) {
    console.error('Ошибка добавления в корзину:', error)
    // 401 уже обрабатывается глобальным interceptor'ом в api/index.js (редирект
    // на /login) - если ещё показать тут blocking alert(), он перехватывает поток
    // выполнения и сбивает/маскирует этот редирект (пользователь видит зависший
    // диалог "Error al agregar al carrito" вместо перехода на страницу входа).
    if (error.response?.status !== 401) {
      alert('Error al agregar al carrito')
    }
  }
}

const buyNow = async () => {
  await addToCart()
  router.push('/carrito')
}

// ===== МОНТИРОВАНИЕ =====
onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.pd-wrap {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.05fr 1fr;  /* 👈 ЭТО ГЛАВНОЕ! */
  gap: 56px;
  padding: 52px 32px 72px;
  align-items: start;
}

@media (max-width: 920px) {
  .pd-wrap {
    grid-template-columns: 1fr !important;  /* 👈 НА МОБИЛКЕ СТАНОВИТСЯ 1 КОЛОНКА */
    gap: 32px !important;
    padding: 36px 20px 72px !important;
  }
}
</style>