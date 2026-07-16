import { ref, computed } from 'vue'
import { authApi } from '../api/auth'

const user = ref(null)
const isAuthenticated = ref(false)

export function useAuth() {
  const loadUser = () => {
    try {
      const userData = localStorage.getItem('user')
      if (userData) {
        user.value = JSON.parse(userData)
        isAuthenticated.value = true
      }
    } catch (e) {
      console.error('Ошибка загрузки пользователя:', e)
    }
  }

  const setUser = (userData) => {
    user.value = userData
    isAuthenticated.value = !!userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  }

  const logout = () => {
    // 👇 ПОЛНАЯ ОЧИСТКА
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    user.value = null
    isAuthenticated.value = false
  }

  const refreshUser = async () => {
    try {
      const response = await authApi.getProfile()
      setUser(response.data)
      return response.data
    } catch (error) {
      console.error('Ошибка обновления профиля:', error)
      // Если 401 — разлогиниваем
      if (error.response?.status === 401) {
        logout()
      }
      return null
    }
  }

  // Загружаем пользователя при инициализации
  loadUser()

  return {
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    setUser,
    logout,
    refreshUser,
    loadUser,
  }
}