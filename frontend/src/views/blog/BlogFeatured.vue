<template>
  <div v-if="featuredPost" class="bl-featured-wrapper">
    <div class="bl-feat">
      <div class="bl-feat-img" :class="{ 'no-image': !featuredPost.image }">
        <img v-if="featuredPost.image" :src="featuredPost.image" :alt="featuredPost.title">
        <span class="bl-feat-badge">artículo destacado</span>
      </div>
      <div class="bl-feat-content">
        <span class="bl-feat-category">{{ featuredPost.category_name || featuredPost.category }}</span>
        <h2 class="bl-feat-title">{{ featuredPost.title }}</h2>
        <p class="bl-feat-excerpt">{{ featuredPost.short_description }}</p>
        <div class="bl-feat-author">
          <span class="bl-feat-avatar">{{ getInitials(featuredPost.author) }}</span>
          <div>
            <div class="bl-feat-name">{{ featuredPost.author || 'Mentored' }}</div>
            <div class="bl-feat-meta">{{ formatDate(featuredPost.created_at) }} · {{ featuredPost.reading_time || '6 min' }} de lectura</div>
          </div>
        </div>
        <router-link :to="`/blog/${featuredPost.slug}`" class="bl-feat-btn">
          Leer artículo
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { blogApi } from '../../api/blog'

const featuredPost = ref(null)

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

const loadFeaturedPost = async () => {
  try {
    const response = await blogApi.getAll()
    const posts = response.data
    // Берём первый пост или помеченный как featured
    const featured = posts.find(p => p.is_featured) || posts[0]
    featuredPost.value = featured || null
  } catch (error) {
    console.error('Ошибка загрузки главного поста:', error)
    // Фолбэк
    featuredPost.value = {
      id: 1,
      slug: 'como-recuperar-tu-energia',
      title: 'Cómo recuperar tu energía cuando todo parece urgente',
      short_description: 'Tres claves para dejar de vivir en piloto automático y volver a elegir dónde pones tu atención y tu tiempo.',
      category: 'Energía',
      author: 'Irina Karbonova',
      created_at: '2026-06-10',
      reading_time: '6 min',
      image: null,
    }
  }
}

onMounted(() => {
  loadFeaturedPost()
})
</script>

<style scoped>
.bl-featured-wrapper {
  background: #0e0c0c;
  padding: 0 32px 64px;
}

.bl-feat {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  background: #161111;
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid #241c1c;
}

.bl-feat-img {
  position: relative;
  min-height: 380px;
  background: #1a1212;
  overflow: hidden;
}

.bl-feat-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.bl-feat-img::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(135deg, #241818 0 12px, #1a1212 12px 24px);
  opacity: 0.4;
}

.bl-feat-img img + .bl-feat-badge {
  z-index: 2;
}

.bl-feat-img.no-image::before {
  opacity: 1;
}
.bl-feat-img::before {
  opacity: 0;
}

.bl-feat-badge {
  position: absolute;
  left: 24px;
  top: 24px;
  font-family: 'Hanken Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  color: #cfc7be;
  background: rgba(0,0,0,0.45);
  padding: 6px 12px;
  border-radius: 999px;
  z-index: 1;
}

.bl-feat-content {
  padding: 48px 44px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.bl-feat-category {
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 16px;
}

.bl-feat-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  line-height: 1.2;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.3px;
}

.bl-feat-excerpt {
  font-size: 17px;
  line-height: 1.65;
  color: #a59c93;
  margin: 0 0 26px;
}

.bl-feat-author {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 26px;
}

.bl-feat-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-family: 'Playfair Display', serif;
  font-weight: 600;
}

.bl-feat-name {
  font-size: 15px;
  color: #ffffff;
  font-weight: 500;
}

.bl-feat-meta {
  font-size: 13.5px;
  color: #6f6862;
}

.bl-feat-btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  background: #ffffff;
  color: #0e0c0c;
  font-weight: 600;
  font-size: 15.5px;
  padding: 13px 26px;
  border-radius: 999px;
  align-self: flex-start;
}

@media (max-width: 900px) {
  .bl-feat { grid-template-columns: 1fr !important; }
  .bl-feat-img { min-height: 240px !important; }
  .bl-featured-wrapper { padding: 0 20px 40px !important; }
}
</style>