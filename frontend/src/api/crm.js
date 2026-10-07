import api from './index'

export const crmApi = {
  getDashboard() {
    return api.get('/crm/dashboard/')
  },
  getStudents(params = {}) {
    return api.get('/crm/students/', { params })
  },
  getStudent(id) {
    return api.get(`/crm/students/${id}/`)
  },
  getCourses(params = {}) {
    return api.get('/crm/courses/', { params })
  },
}