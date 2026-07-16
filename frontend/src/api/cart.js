import api from './index'

export const cartApi = {
  // Получить корзину
  getCart() {
    return api.get('/cart/')
  },

  // Добавить товар
  addItem(productType, productId, quantity = 1) {
    return api.post('/cart/add/', {
      product_type: productType,
      product_id: productId,
      quantity,
    })
  },

  // Обновить количество
  updateItem(itemId, quantity) {
    return api.put(`/cart/update/${itemId}/`, { quantity })
  },

  // Удалить товар
  removeItem(itemId) {
    return api.delete(`/cart/remove/${itemId}/`)
  },

  // Очистить корзину
  clearCart() {
    return api.delete('/cart/clear/')
  },
}