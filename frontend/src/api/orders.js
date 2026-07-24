import api from './index'

export const orderApi = {
  createOrder() {
    return api.post('/create_order/')
  },

  getOrder(orderNumber) {
    return api.get(`/orders/${orderNumber}/`)
  },
}