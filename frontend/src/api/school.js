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

  // Задание + мой ответ
  getAssignment(assignmentId) {
    return api.get(`/school/assignments/${assignmentId}/`)
  },

  // Сдать задание. formData: FormData с полями text и/или file
  // (Content-Type multipart проставит браузер сам)
  submitAssignment(assignmentId, formData) {
    return api.post(`/school/assignments/${assignmentId}/submit/`, formData)
  },

  // --- Преподаватель ---
  // Мои курсы (как препода) со счётчиками
  teacherCourses() {
    return api.get('/school/teacher/courses/')
  },

  // Ростер студентов курса с прогрессом
  teacherCourseStudents(courseId) {
    return api.get(`/school/teacher/courses/${courseId}/students/`)
  },

  // Очередь домашних заданий на проверку (по умолчанию submitted)
  teacherSubmissions() {
    return api.get('/school/teacher/submissions/')
  },

  // Проверить сдачу: { status: 'reviewed'|'needs_revision', score, mentor_comment }
  reviewSubmission(submissionId, data) {
    return api.post(`/school/teacher/submissions/${submissionId}/review/`, data)
  },
}
