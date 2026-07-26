import api from './index'

export const paymentApi = {
  createPreference(orderNumber) {
    return api.post('/payment/create-preference/', { order_number: orderNumber })
  },
}
