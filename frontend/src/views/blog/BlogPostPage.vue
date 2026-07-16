<template>
  <div class="blog-post-page">
    <!-- Загрузка -->
    <div v-if="loading" class="bp-loading">
      <div class="bp-loading-spinner"></div>
      <p>Cargando artículo...</p>
    </div>

    <!-- Контент -->
    <template v-else-if="post">
      <!-- Хлебные крошки -->
      <div class="bp-breadcrumb">
        <div class="bp-breadcrumb-inner">
          <router-link to="/blog" class="bp-breadcrumb-link">Blog</router-link>
          <span class="bp-breadcrumb-sep">/</span>
          <span class="bp-breadcrumb-current">{{ post.title }}</span>
        </div>
      </div>

      <!-- Герой поста -->
      <section class="bp-hero">
        <div class="bp-hero-container">
          <span class="bp-hero-category">{{ post.category || 'Sin categoría' }}</span>
          <h1 class="bp-hero-title">{{ post.title }}</h1>
          <div class="bp-hero-meta">
            <span class="bp-hero-author">
              <span class="bp-hero-avatar">{{ getInitials(post.author) }}</span>
              {{ post.author || 'Mentored' }}
            </span>
            <span class="bp-hero-date">{{ formatDate(post.created_at) }}</span>
            <span class="bp-hero-reading">{{ post.reading_time || '5 min' }} de lectura</span>
          </div>
        </div>
      </section>

      <!-- Изображение -->
      <div v-if="post.image" class="bp-image-wrapper">
        <div class="bp-image-container">
          <img :src="post.image" :alt="post.title">
        </div>
      </div>

      <!-- Контент -->
      <section class="bp-content">
        <div class="bp-content-inner">
          <div class="bp-content-body" v-html="post.content"></div>
        </div>
      </section>

      <!-- Назад -->
      <div class="bp-back">
        <router-link to="/blog" class="bp-back-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          Volver al blog
        </router-link>
      </div>
    </template>

    <!-- Не найден -->
    <div v-else class="bp-not-found">
      <h2>Artículo no encontrado</h2>
      <router-link to="/blog" class="bp-back-btn">Volver al blog</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { blogApi } from '../../api/blog'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const post = ref(null)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const getInitials = (name) => {
  if (!name) return 'M'
  return name.charAt(0).toUpperCase()
}

const loadPost = async () => {
  const slug = route.params.slug
  loading.value = true

  try {
    const response = await blogApi.getBySlug(slug)
    post.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки поста:', error)
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPost()
})
</script>

<style scoped>
/* ===== ОБЩИЕ ===== */
.blog-post-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}

/* ===== ХЛЕБНЫЕ КРОШКИ ===== */
.bp-breadcrumb {
  background: #f5eee3;
  border-bottom: 1px solid #e6dccb;
}

.bp-breadcrumb-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 32px;
  font-size: 14.5px;
  color: #8a8079;
}

.bp-breadcrumb-link {
  color: #8a8079;
  text-decoration: none;
}

.bp-breadcrumb-link:hover {
  color: #8e1519;
}

.bp-breadcrumb-sep {
  margin: 0 8px;
  color: #c9bca6;
}

.bp-breadcrumb-current {
  color: #15110f;
}

/* ===== ГЕРОЙ ===== */
.bp-hero {
  background: #0e0c0c;
  padding: 64px 32px 48px;
  text-align: center;
}

.bp-hero-container {
  max-width: 820px;
  margin: 0 auto;
}

.bp-hero-category {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 16px;
}

.bp-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  line-height: 1.12;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 24px;
  letter-spacing: -0.5px;
}

.bp-hero-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 15px;
  color: #a59c93;
}

.bp-hero-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bp-hero-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.bp-hero-date,
.bp-hero-reading {
  color: #6f6862;
}

/* ===== ИЗОБРАЖЕНИЕ ===== */
.bp-image-wrapper {
  padding: 48px 32px 0;
  max-width: 1200px;
  margin: 0 auto;
}

.bp-image-container {
  border-radius: 22px;
  overflow: hidden;
  background: #1a1212;
  aspect-ratio: 1200/560;
}

.bp-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ===== КОНТЕНТ ===== */
.bp-content {
  padding: 56px 32px 80px;
}

.bp-content-inner {
  max-width: 780px;
  margin: 0 auto;
}

.bp-content-body {
  font-size: 18px;
  line-height: 1.8;
  color: #3a342e;
}

.bp-content-body h2 {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  color: #15110f;
  margin: 40px 0 16px;
  letter-spacing: -0.3px;
}

.bp-content-body h3 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #15110f;
  margin: 32px 0 12px;
}

.bp-content-body p {
  margin: 0 0 20px;
  color: #5d544c;
}

.bp-content-body ul,
.bp-content-body ol {
  margin: 0 0 20px;
  padding-left: 24px;
  color: #5d544c;
}

.bp-content-body li {
  margin-bottom: 8px;
}

.bp-content-body a {
  color: #8e1519;
  text-decoration: underline;
}

.bp-content-body img {
  max-width: 100%;
  border-radius: 12px;
  margin: 24px 0;
}

.bp-content-body blockquote {
  border-left: 4px solid #8e1519;
  padding: 16px 24px;
  margin: 24px 0;
  background: #faf6f0;
  border-radius: 0 12px 12px 0;
  font-style: italic;
  color: #3a342e;
}

/* ===== НАЗАД ===== */
.bp-back {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 32px 80px;
}

.bp-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #8e1519;
  font-weight: 500;
  font-size: 16px;
  transition: color 0.3s;
}

.bp-back-btn:hover {
  color: #a01a1f;
}

/* ===== ЗАГРУЗКА ===== */
.bp-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #8a8079;
}

.bp-loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e4ddd2;
  border-top: 4px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== НЕ НАЙДЕН ===== */
.bp-not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  padding: 40px 20px;
}

.bp-not-found h2 {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  color: #15110f;
  margin-bottom: 20px;
}

/* ===== АДАПТИВ ===== */
@media (max-width: 920px) {
  .bp-hero {
    padding: 48px 20px 32px;
  }
  .bp-hero-title {
    font-size: 32px;
  }
  .bp-hero-meta {
    gap: 12px;
    font-size: 14px;
  }
  .bp-image-wrapper {
    padding: 24px 20px 0;
  }
  .bp-content {
    padding: 32px 20px 56px;
  }
  .bp-content-body {
    font-size: 16px;
  }
  .bp-back {
    padding: 0 20px 56px;
  }
  .bp-breadcrumb-inner {
    padding: 14px 20px;
    font-size: 13px;
  }
}
</style>