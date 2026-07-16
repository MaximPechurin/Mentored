import api from './index'

export const blogApi = {
  // Получить все посты
  getAll() {
    return api.get('/blog/posts/')
  },

  // Получить один пост по slug
  getBySlug(slug) {
    return api.get(`/blog/posts/${slug}/`)
  },

  // Получить категории
  getCategories() {
    return api.get('/blog/categories/')
  },

  // Получить посты по категории
  getByCategory(categorySlug) {
    return api.get(`/blog/posts/?category=${categorySlug}`)
  },
}