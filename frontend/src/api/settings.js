import api from './index'

export const settingsApi = {
  get() {
    return api.get('/site-settings/')
  },
}
