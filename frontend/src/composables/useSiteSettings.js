import { ref } from 'vue'
import { settingsApi } from '../api/settings'

// Контакты/соцсети сайта - раньше были зашиты в коде (Footer.vue и
// т.п.), теперь редактируются из /admin/ (MENTORED · Настройки сайта).
// Публичный эндпоинт, грузим один раз на всё приложение и переиспользуем
// между всеми компонентами, которые его используют (тот же паттерн, что
// useLanguage/useAuth - модульный ref, а не per-component состояние).
const settings = ref({
  contact_email: '',
  whatsapp_number: '',
  instagram_url: '',
  facebook_url: '',
  youtube_url: '',
  linkedin_url: '',
})
let loaded = false
let loadingPromise = null

async function ensureLoaded() {
  if (loaded) return
  if (!loadingPromise) {
    loadingPromise = settingsApi.get()
      .then(({ data }) => {
        settings.value = data
        loaded = true
      })
      .catch((error) => {
        console.error('Error al cargar la configuración del sitio:', error)
        loadingPromise = null
      })
  }
  await loadingPromise
}

export function useSiteSettings() {
  ensureLoaded()
  return { settings }
}
