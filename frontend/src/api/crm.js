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
  getCourse(id) {
  return api.get(`/crm/courses/${id}/`)
  },
  getCourseStudents(id, params = {}) {
    return api.get(`/crm/courses/${id}/students/`, { params })
  },
  getCourseOrders(id, params = {}) {
    return api.get(`/crm/courses/${id}/orders/`, { params })
  },
  getTeachers(params = {}) {
    return api.get('/crm/teachers/', { params })
  },
  getTeacher(id) {
    return api.get(`/crm/teachers/${id}/`)
  },
  getOrders(params = {}) {
    return api.get('/crm/orders/', { params })
  },
  getOrder(id) {
    return api.get(`/crm/orders/${id}/`)
  },
  getPayments(params = {}) {
    return api.get('/crm/payments/', { params })
  },
  getContactMessages(params = {}) {
    return api.get('/crm/contact-messages/', { params })
  },
  getContactMessage(id) {
    return api.get(`/crm/contact-messages/${id}/`)
  },
  updateContactMessage(id, data) {
    return api.patch(`/crm/contact-messages/${id}/`, data)
  },
  deleteContactMessage(id) {
    return api.delete(`/crm/contact-messages/${id}/`)
  },
  bulkContactMessages(data) {
    return api.post('/crm/contact-messages/bulk/', data)
  },
  getContactMessagesUnreadCount() {
    return api.get('/crm/contact-messages/unread-count/')
  },
  getSubmissions(params = {}) {
    return api.get('/crm/submissions/', { params })
  },
  getSubmission(id) {
    return api.get(`/crm/submissions/${id}/`)
  },
}