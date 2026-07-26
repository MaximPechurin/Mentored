import api from './index'

export const orderApi = {
  createOrder() {
    return api.post('/create_order/')
  },

  listOrders() {
    return api.get('/orders/')
  },

  getOrder(orderNumber) {
    return api.get(`/orders/${orderNumber}/`)
  },
}