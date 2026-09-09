import axios from 'axios'

// Определяем базовый URL динамически
const API_URL = process.env.NODE_ENV === 'production'
    ? '' // Пустая строка означает "тот же домен, где открыт сайт"
    : 'http://localhost:8000';

// Или явно:
// const API_URL = window.location.origin;

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ✅ ДОБАВЛЯЕМ ТОКЕН В КАЖДЫЙ ЗАПРОС
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // Для загрузки файлов (FormData) убираем дефолтный
    // Content-Type: application/json - иначе браузер не проставит
    // multipart-границу и файл не долетит до сервера. Также увеличиваем
    // timeout - глобальные 10с достаточны для обычных запросов, но большой
    // видеофайл грузится намного дольше и axios обрывал запрос сам, ещё до
    // ответа сервера (в логах nginx это виднелось как код 499 - клиент
    // закрыл соединение). 600000мс = 10 мин, как proxy_read/send_timeout в
    // nginx для school-эндпоинтов.
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
      config.timeout = 600000
    }
    console.log('📤 Запрос:', config.method.toUpperCase(), config.url)
    return config
  },
  (error) => Promise.reject(error)
)

// ✅ ОБРАБОТКА 401 (неавторизован)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/token/refresh/`, {
            refresh: refreshToken,
          })
          localStorage.setItem('access_token', response.data.access)
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`
          return api(originalRequest)
        } catch (refreshError) {
          console.error('❌ Не удалось обновить токен:', refreshError)
          authApi.logout()
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api