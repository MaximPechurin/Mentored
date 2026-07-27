import api from './index'

export const contactApi = {
  sendMessage(data) {
    return api.post('/contact/', data)
  },
}
