<template>
  <div class="blog-page">
    <BlogHero />
    <BlogFeatured />
    <BlogCategories v-model="activeCategory" />
    <BlogGrid :category="activeCategory" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BlogHero from './BlogHero.vue'
import BlogFeatured from './BlogFeatured.vue'
import BlogCategories from './BlogCategories.vue'
import BlogGrid from './BlogGrid.vue'

const activeCategory = ref('todos')
</script>

<style scoped>
.blog-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #ffffff;
}
</style>