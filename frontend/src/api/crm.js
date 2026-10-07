import api from './index'

export const crmApi = {
  getDashboard() {
    return api.get('/crm/dashboard/')
  },
  getStudents(params = {}) {
    return api.get('/crm/students/', { params })
  },
}