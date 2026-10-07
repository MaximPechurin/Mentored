import api from './index'

export const crmApi = {
  getDashboard() {
    return api.get('/crm/dashboard/')
  },
}