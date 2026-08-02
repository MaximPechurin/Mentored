import api from './index'

export const schoolApi = {
  // Список курсов, купленных студентом (с прогрессом)
  myCourses() {
    return api.get('/school/my-courses/')
  },

  // Модули/уроки конкретного курса (нужен активный доступ)
  getCourse(slug) {
    return api.get(`/school/courses/${slug}/`)
  },

  // Отметить прогресс по уроку: { is_completed, last_position_seconds }
  updateLessonProgress(lessonId, data) {
    return api.post(`/school/lessons/${lessonId}/progress/`, data)
  },
}
