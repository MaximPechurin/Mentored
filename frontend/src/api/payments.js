import api from './index'

export const paymentApi = {
  createPreference(orderNumber) {
    return api.post('/payment/create-preference/', { order_number: orderNumber })
  },

  // «Магическая ссылка»: публичная карточка товара для лендинга покупки.
  quickBuyProduct(productType, slug) {
    return api.get(`/payment/quick-buy/product/${productType}/${slug}/`)
  },

  // «Магическая ссылка»: быстрая покупка одного товара по email, без регистрации.
  // payload: { product_type, email, slug | product_id }
  quickBuy(payload) {
    return api.post('/payment/quick-buy/', payload)
  },
}
