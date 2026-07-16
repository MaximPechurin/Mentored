import api from './index'

export const authApi = {
  // Вход
  login(email, password) {
    return api.post('/token/', { email, password })
  },

  // Регистрация
  register(userData) {
    return api.post('/register/', userData)
  },

  // Обновление токена
  refresh(refreshToken) {
    return api.post('/token/refresh/', { refresh: refreshToken })
  },

  // Проверка токена
  verify(token) {
    return api.post('/token/verify/', { token })
  },

  // Получить профиль
  getProfile() {
    return api.get('/profile/')
  },

  // Обновить профиль
  updateProfile(data) {
    return api.put('/profile/', data)
  },
  // Выход
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },
  // Сохранить токены
  setTokens(access, refresh) {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  },
  // Получить access_token
  getAccessToken() {
    return localStorage.getItem('access_token')
  },
  // Проверка авторизации
  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },
}