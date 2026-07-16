import api from './index'

export const productApi = {
  // Все товары (все типы)
  getAll() {
    return api.get('/products/')
  },
  getBySlug(slug) {
    return api.get(`/products/${slug}/`)
  },

  // Курсы
  getCourses() {
    return api.get('/courses/')
  },
  getCourse(slug) {
    return api.get(`/courses/${slug}/`)
  },

  // Книги
  getBooks() {
    return api.get('/books/')
  },
  getBook(slug) {
    return api.get(`/books/${slug}/`)
  },

  // Консультации
  getConsultations() {
    return api.get('/consultations/')
  },
  getConsultation(slug) {
    return api.get(`/consultations/${slug}/`)
  },

  // Мембершипы
  getMemberships() {
    return api.get('/memberships/')
  },
  getMembership(slug) {
    return api.get(`/memberships/${slug}/`)
  },
}