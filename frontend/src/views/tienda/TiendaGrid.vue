<template>
  <section class="t-store">
    <!-- Состояние загрузки -->
    <div v-if="loading" class="t-loading">
      <div class="t-loading-spinner"></div>
      <p>Cargando productos...</p>
    </div>

    <!-- Товары -->
    <div v-else-if="filteredProducts.length > 0" class="t-grid">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="t-product-card"
      >
        <router-link :to="`/producto/${product.slug || product.id}`" class="t-product-img">
          <img
            :src="product.image ? `http://localhost:8000${product.image}` : '/images/placeholder.png'"
            :alt="product.name"
          >
        </router-link>
        <div class="t-product-body">
          <span class="t-product-category">{{ product.category_name || product.category }}</span>
          <router-link :to="`/producto/${product.slug || product.id}`" class="t-product-title-link">
            <h3 class="t-product-title">{{ product.name }}</h3>
          </router-link>
          <p class="t-product-desc">{{ product.short_description || product.desc }}</p>
          <div class="t-product-price">
            <span class="t-product-current">{{ formatPrice(product.price) }}</span>
            <span v-if="product.old_price" class="t-product-old">{{ formatPrice(product.old_price) }}</span>
          </div>
          <button
            @click="addToCart(product)"
            class="t-product-btn"
            :class="{ added: isAdded(product) }"
          >
            <template v-if="isAdded(product)">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Agregado
            </template>
            <template v-else>
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"/>
                <circle cx="20" cy="21" r="1"/>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
              </svg>
              Agregar al carrito
            </template>
          </button>
        </div>
      </div>
    </div>

    <!-- Пусто -->
    <p v-else class="t-empty">
      No hay productos en esta categoría todavía.
    </p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productApi } from '../../api/products.js'
import { cartApi } from '../../api/cart.js'

const props = defineProps({
  filter: {
    type: String,
    default: 'todos'
  }
})

// ===== СОСТОЯНИЕ =====
const loading = ref(true)
const products = ref({
  courses: [],
  books: [],
  consultations: [],
  memberships: [],
})
const addedItems = ref({})

// ===== КАТЕГОРИИ ДЛЯ ФИЛЬТРА =====
const categoryMap = {
  todos: 'all',
  libros: 'books',
  cursos: 'courses',
  consultas: 'consultations',
  comunidad: 'memberships',
}

// ===== ВСЕ ТОВАРЫ (плоский список) =====
const allProducts = computed(() => {
  const all = []
  const map = {
    courses: { category: 'Cursos', key: 'cursos' },
    books: { category: 'Libros', key: 'libros' },
    consultations: { category: 'Consultas', key: 'consultas' },
    memberships: { category: 'Comunidad', key: 'comunidad' },
  }

  for (const [key, { category, key: filterKey }] of Object.entries(map)) {
    for (const item of products.value[key] || []) {
      all.push({
        ...item,
        category_name: category,
        category_key: filterKey,
      })
    }
  }

  return all
})

// ===== ФИЛЬТРОВАННЫЕ ТОВАРЫ =====
const filteredProducts = computed(() => {
  if (props.filter === 'todos') return allProducts.value
  return allProducts.value.filter(p => p.category_key === props.filter)
})

// ===== ФОРМАТИРОВАНИЕ ЦЕНЫ =====
const formatPrice = (price) => {
  if (!price) return '$0.00'
  return `$${Number(price).toFixed(2)}`
}

// ===== ЗАГРУЗКА ТОВАРОВ =====
const loadProducts = async () => {
  console.log('🟡 loadProducts вызван')
  loading.value = true
  try {
    const response = await productApi.getAll()
    console.log('🔍 Данные с бэка:', response.data)
    console.log('🔍 Первый товар:', response.data.courses[0])
    products.value = {
      courses: response.data.courses || [],
      books: response.data.books || [],
      consultations: response.data.consultations || [],
      memberships: response.data.memberships || [],
    }
  } catch (error) {
    console.error('Ошибка загрузки товаров:', error)
    // Если бэк недоступен — используем локальные данные
    useLocalFallback()
  } finally {
    loading.value = false
  }
}

// ===== ЛОКАЛЬНЫЙ ФОЛБЭК (если бэк не доступен) =====
const useLocalFallback = () => {
  products.value = {
    courses: [
      {
        id: 1,
        name: 'Curso: Recupera tu Energía',
        slug: 'curso-recupera-tu-energia',
        short_description: 'Activa tu vitalidad y toma el control de tu día.',
        price: '97.00',
        old_price: '147.00',
        image: '/images/curso-energia.png',
      }
    ],
    books: [
      {
        id: 2,
        name: 'Libro Digital: El Camino del Propósito',
        slug: 'libro-el-camino-del-proposito',
        short_description: 'Comprende tu propósito y crea la vida que deseas.',
        price: '27.00',
        old_price: '47.00',
        image: '/images/libro-proposito.png',
      }
    ],
    consultations: [
      {
        id: 3,
        name: 'Consulta 1:1 con Irina Karbonova',
        slug: 'consulta-con-irina',
        short_description: 'Acompañamiento personalizado con la fundadora.',
        price: '297.00',
        old_price: null,
        image: '/images/consulta-irina.png',
      }
    ],
    memberships: [
      {
        id: 4,
        name: 'Membresía Comunidad Mentored — Premium',
        slug: 'membresia-comunidad-premium',
        short_description: 'Acceso completo a la comunidad con beneficios exclusivos.',
        price: '77.00',
        old_price: '97.00',
        image: '/images/membresia-premium.png',
      }
    ],
  }
}

// ===== ДОБАВЛЕНИЕ В КОРЗИНУ =====
const addToCart = async (product) => {
  // Определяем тип товара
  const typeMap = {
    cursos: 'course',
    libros: 'book',
    consultas: 'consultation',
    comunidad: 'membership',
  }
  const productType = typeMap[product.category_key] || 'course'

  // УНИКАЛЬНЫЙ КЛЮЧ ЧТОБЫ ТОВАРЫ С ОДИНАКОВЫМ АЙДИ НЕ ПОДСВЕЧИВАЛИСЬ КАК БУДТО ДОБАВЛЕНЫ ВСЕ СРАЗУ
  const uniqueKey = `${product.category_key}-${product.id}`

  try {
    await cartApi.addItem(productType, product.id)
    addedItems.value = { ...addedItems.value, [uniqueKey]: true }
    setTimeout(() => {
      const newAdded = { ...addedItems.value }
      delete newAdded[uniqueKey]
      addedItems.value = newAdded
    }, 1500)
  } catch (error) {
    console.error('Ошибка добавления в корзину:', error)
    alert('Error al agregar al carrito')
  }
}

// ===== ПРОВЕРКА ДОБАВЛЕНИЯ =====
const isAdded = (product) => {
  const uniqueKey = `${product.category_key}-${product.id}`
  return !!addedItems.value[uniqueKey]
}

// ===== МОНТИРОВАНИЕ =====
onMounted(() => {
  console.log('🟢 TiendaGrid mounted — загружаем товары')
  loadProducts()
})
</script>

<style scoped>
.t-store {
  background: #f5eee3;
  padding: 56px 32px 96px;
}

.t-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 26px;
}

/* ===== КАРТОЧКА ТОВАРА ===== */
.t-product-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 22px 48px -32px rgba(0,0,0,0.4);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s, box-shadow 0.3s;
}

.t-product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 28px 56px -32px rgba(0,0,0,0.5);
}

.t-product-img {
  position: relative;
  aspect-ratio: 545/286;
  overflow: hidden;
  background: #1a1212;
  display: block;
}

.t-product-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.t-product-body {
  padding: 24px 26px 28px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.t-product-category {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 10px;
}

.t-product-title-link {
  text-decoration: none;
}

.t-product-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 12px;
}

.t-product-desc {
  font-size: 15.5px;
  line-height: 1.55;
  color: #6b6259;
  margin: 0 0 20px;
  flex: 1;
}

.t-product-price {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 20px;
}

.t-product-current {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 800;
  color: #8e1519;
}

.t-product-old {
  font-size: 17px;
  color: #a59c93;
  text-decoration: line-through;
}

/* ===== КНОПКА ===== */
.t-product-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: none;
  cursor: pointer;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  padding: 15px 20px;
  border-radius: 12px;
  font-family: inherit;
  background: #8e1519;
  transition: background 0.3s;
}

.t-product-btn:hover {
  background: #a01a1f;
}

.t-product-btn.added {
  background: #1f7a3d;
}

/* ===== ЗАГРУЗКА ===== */
.t-loading {
  text-align: center;
  padding: 80px 20px;
  color: #8a8079;
}

.t-loading-spinner {
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

/* ===== ПУСТО ===== */
.t-empty {
  text-align: center;
  color: #8a8079;
  font-size: 18px;
  padding: 60px 0;
  max-width: 1320px;
  margin: 0 auto;
}

/* ===== АДАПТИВ ===== */
@media (max-width: 860px) {
  .t-store { padding: 40px 20px 64px !important; }
  .t-grid { grid-template-columns: 1fr 1fr !important; gap: 18px !important; }
}

@media (max-width: 520px) {
  .t-grid { grid-template-columns: 1fr !important; }
}
</style>