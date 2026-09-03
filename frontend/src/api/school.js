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

  // Лента «Ответы и комментарии» под заданием (публичные + свой).
  // sort: 'old' (по умолчанию) | 'new'
  assignmentAnswers(assignmentId, sort = 'old') {
    return api.get(`/school/assignments/${assignmentId}/answers/`, { params: { sort } })
  },

  // Комментарий к ответу на задание
  addSubmissionComment(submissionId, text) {
    return api.post(`/school/submissions/${submissionId}/comments/`, { text })
  },

  // Открыть/скрыть свой ответ для других учеников
  setSubmissionVisibility(submissionId, isPublic) {
    return api.post(`/school/submissions/${submissionId}/visibility/`, { is_public: isPublic })
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

  // Модули/уроки курса с прогрессом конкретного студента (вид препода)
  teacherStudentCourse(courseId, userId) {
    return api.get(`/school/teacher/courses/${courseId}/students/${userId}/`)
  },

  // Очередь домашних заданий на проверку (по умолчанию submitted)
  teacherSubmissions() {
    return api.get('/school/teacher/submissions/')
  },

  // Сводка ДЗ по всем курсам препода: по каждому студенту все задания
  // со статусом выполнено/не выполнено
  teacherHomework() {
    return api.get('/school/teacher/homework/')
  },

  // Проверить сдачу: { status: 'reviewed'|'needs_revision', score, mentor_comment }
  reviewSubmission(submissionId, data) {
    return api.post(`/school/teacher/submissions/${submissionId}/review/`, data)
  },

  // --- Чат / личные сообщения ---
  // Дерево чата: курсы -> собеседники + непрочитанные
  chatDirectory() {
    return api.get('/school/chat/directory/')
  },
  // Переписка с пользователем (GET помечает входящие прочитанными)
  getConversation(userId) {
    return api.get(`/school/messages/${userId}/`)
  },
  // Отправить сообщение
  sendMessage(userId, content) {
    return api.post(`/school/messages/${userId}/`, { content })
  },

  // --- Форум курса ---
  // Список форумов моих курсов (студент и/или препод)
  forumsList() {
    return api.get('/school/foros/')
  },
  courseThreads(courseId) {
    return api.get(`/school/courses/${courseId}/threads/`)
  },
  createThread(courseId, data) {
    return api.post(`/school/courses/${courseId}/threads/`, data)
  },
  getThread(threadId) {
    return api.get(`/school/threads/${threadId}/`)
  },
  replyThread(threadId, content) {
    return api.post(`/school/threads/${threadId}/posts/`, { content })
  },
  moderateThread(threadId, data) {
    return api.post(`/school/threads/${threadId}/moderate/`, data)
  },

  // --- Аналитика ---
  courseAnalytics(courseId) {
    return api.get(`/school/teacher/courses/${courseId}/analytics/`)
  },
  platformAnalytics() {
    return api.get('/school/analytics/overview/')
  },
}
