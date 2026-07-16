<template>
  <section class="bl-grid-section">
    <!-- Загрузка -->
    <div v-if="loading" class="bl-loading">
      <div class="bl-loading-spinner"></div>
      <p>Cargando artículos...</p>
    </div>

    <!-- Посты -->
    <div v-else-if="filteredPosts.length > 0" class="bl-grid">
      <router-link
        v-for="post in filteredPosts"
        :key="post.id"
        :to="`/blog/${post.slug}`"
        class="bl-post-card"
      >
        <div class="bl-post-img" :class="{ 'no-image': !post.image }">
          <img v-if="post.image" :src="post.image" :alt="post.title">
          <span class="bl-post-category">{{ post.category_name || post.category }}</span>
        </div>
        <div class="bl-post-body">
          <h3 class="bl-post-title">{{ post.title }}</h3>
          <p class="bl-post-excerpt">{{ post.short_description }}</p>
          <div class="bl-post-meta">{{ formatDate(post.created_at) }} · {{ post.reading_time || '5 min' }}</div>
        </div>
      </router-link>
    </div>

    <!-- Пусто -->
    <p v-else class="bl-empty">
      No hay artículos en esta categoría todavía.
    </p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { blogApi } from '../../api/blog'

const props = defineProps({
  category: {
    type: String,
    default: 'todos'
  }
})

const loading = ref(true)
const posts = ref([])
const categories = ref([])

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

// Загрузка постов
const loadPosts = async () => {
  loading.value = true
  try {
    const response = await blogApi.getAll()
    posts.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки постов:', error)
    // Фолбэк на локальные данные
    posts.value = getLocalPosts()
  } finally {
    loading.value = false
  }
}

// Локальные данные (фолбэк)
const getLocalPosts = () => {
  return [
    {
      id: 1,
      slug: 'el-descanso-tambien-es-productividad',
      title: 'El descanso también es productividad',
      short_description: 'Por qué parar no es perder el tiempo, sino la base de tu rendimiento sostenible.',
      category: 'Energía',
      category_key: 'energia',
      created_at: '2026-06-05',
      reading_time: '5 min',
      image: null,
    },
    // ... остальные посты
  ]
}

// Фильтрация постов
const filteredPosts = computed(() => {
  if (props.category === 'todos') return posts.value

  return posts.value.filter(post => {
    // Вариант 1: сравниваем по названию категории (если приходит строка)
    if (post.category_name) {
      return post.category_name.toLowerCase() === props.category
    }
    // Вариант 2: сравниваем по slug категории (если приходит)
    if (post.category_slug) {
      return post.category_slug === props.category
    }
    // Вариант 3: если категория приходит как строка
    if (typeof post.category === 'string') {
      return post.category.toLowerCase() === props.category
    }
    return false
  })
})

// Загрузка при монтировании
onMounted(() => {
  loadPosts()
})

// Перезагрузка при смене категории (опционально)
watch(() => props.category, () => {
  // Если хочешь перезагружать с бэка при смене категории — раскомментируй
  // loadPosts()
})
</script>

<style scoped>
.bl-grid-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 64px 32px 96px;
}

.bl-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.bl-post-card {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  overflow: hidden;
  transition: box-shadow 0.3s, transform 0.3s;
}

.bl-post-card:hover {
  box-shadow: 0 18px 40px -28px rgba(0,0,0,0.25);
  transform: translateY(-2px);
}

.bl-post-img {
  height: 190px;
  background: #1a1212;
  position: relative;
  overflow: hidden;
}

.bl-post-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.bl-post-img::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(135deg, #241818 0 11px, #1a1212 11px 22px);
  opacity: 0.5;
}

.bl-post-img img + .bl-post-category {
  z-index: 2;
}

.bl-post-img.no-image::before {
  opacity: 1;
}
.bl-post-img::before {
  opacity: 0;
}

.bl-post-category {
  position: absolute;
  left: 16px;
  top: 16px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #0e0c0c;
  background: #c49a3f;
  padding: 5px 11px;
  border-radius: 999px;
  z-index: 1;
}

.bl-post-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.bl-post-title {
  font-family: 'Playfair Display', serif;
  font-size: 21px;
  line-height: 1.25;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 12px;
}

.bl-post-excerpt {
  font-size: 15.5px;
  line-height: 1.6;
  color: #6f655c;
  margin: 0 0 20px;
  flex: 1;
}

.bl-post-meta {
  margin-top: auto;
  font-size: 13.5px;
  color: #a59c93;
}

/* ===== ЗАГРУЗКА ===== */
.bl-loading {
  text-align: center;
  padding: 60px 20px;
  color: #8a8079;
}

.bl-loading-spinner {
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
.bl-empty {
  text-align: center;
  color: #8a8079;
  font-size: 18px;
  padding: 60px 0;
}

@media (max-width: 900px) {
  .bl-grid-section { padding: 48px 20px 80px !important; }
  .bl-grid { grid-template-columns: 1fr !important; }
}

@media (min-width: 901px) and (max-width: 1180px) {
  .bl-grid { grid-template-columns: 1fr 1fr !important; }
}
</style>