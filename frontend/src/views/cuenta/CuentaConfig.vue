<template>
  <div>
    <h2 class="ac-section-title">Configuración</h2>

    <!-- Datos personales -->
    <form class="ac-card" @submit.prevent="saveSettings">
      <h3 class="ac-card-title">Datos personales</h3>
      <div class="ac-grid2" v-if="formData">
        <label class="ac-field">
          <span class="ac-field-label">Nombre completo</span>
          <input type="text" v-model="formData.full_name" class="ac-input">
        </label>
        <label class="ac-field">
          <span class="ac-field-label">Correo electrónico</span>
          <input type="email" v-model="formData.email" class="ac-input" disabled>
        </label>
        <label class="ac-field">
          <span class="ac-field-label">WhatsApp</span>
          <input type="tel" v-model="formData.phone" class="ac-input">
        </label>
        <label class="ac-field">
          <span class="ac-field-label">Nueva contraseña</span>
          <input type="password" v-model="formData.new_password" placeholder="••••••••" class="ac-input">
        </label>
      </div>
      <button type="submit" class="ac-save-btn" :disabled="loading">
        {{ loading ? 'Guardando...' : 'Guardar cambios' }}
      </button>
    </form>

    <!-- Notificaciones -->
    <div class="ac-card">
      <h3 class="ac-card-title">Notificaciones</h3>
      <label class="ac-toggle">
        <span>Novedades y recursos por correo</span>
        <input type="checkbox" v-model="notifications.email">
      </label>
      <label class="ac-toggle">
        <span>Recordatorios de consultas por WhatsApp</span>
        <input type="checkbox" v-model="notifications.whatsapp">
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuth } from '../../composables/useAuth'
import { authApi } from '../../api/auth'

const { user, refreshUser } = useAuth()
const loading = ref(false)

const formData = reactive({
  full_name: '',
  email: '',
  phone: '',
  new_password: '',
})

const notifications = reactive({
  email: true,
  whatsapp: true,
})

// Загружаем данные пользователя в форму
const loadUserData = () => {
  if (user.value) {
    formData.full_name = user.value.full_name || user.value.username || ''
    formData.email = user.value.email || ''
    formData.phone = user.value.phone || ''
  }
}

// Сохраняем изменения
const saveSettings = async () => {
  loading.value = true
  try {
    const data = {
      full_name: formData.full_name,
      phone: formData.phone,
    }
    if (formData.new_password) {
      data.password = formData.new_password
    }
    await authApi.updateProfile(data)
    await refreshUser()
    alert('¡Cambios guardados exitosamente! ✅')
    formData.new_password = ''
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    // 401 обрабатывает глобальный interceptor в api/index.js (редирект на
    // /login) - blocking alert() тут сбивал бы этот редирект.
    if (error.response?.status !== 401) {
      alert('Error al guardar los cambios. Inténtalo de nuevo.')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
/* стили без изменений */
.ac-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}
.ac-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 32px;
  margin-bottom: 24px;
}
.ac-card-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 20px;
}
.ac-grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}
.ac-field {
  display: block;
}
.ac-field-label {
  display: block;
  font-size: 13.5px;
  font-weight: 500;
  color: #6f655c;
  margin-bottom: 8px;
}
.ac-input {
  width: 100%;
  border: 1px solid #e2dcd4;
  border-radius: 11px;
  padding: 13px 15px;
  font-size: 16px;
  font-family: inherit;
  color: #15110f;
  outline: none;
  background: #fbf9f6;
  transition: border-color 0.3s;
}
.ac-input:focus {
  border-color: #8e1519;
}
.ac-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.ac-save-btn {
  border: none;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 15.5px;
  padding: 13px 30px;
  border-radius: 999px;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.3s;
}
.ac-save-btn:hover:not(:disabled) {
  background: #a01a1f;
}
.ac-save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.ac-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid #f3efe9;
  font-size: 16px;
  color: #3a342e;
  cursor: pointer;
}
.ac-toggle:last-child {
  border-bottom: none;
}
.ac-toggle input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #8e1519;
  cursor: pointer;
}
@media (max-width: 920px) {
  .ac-grid2 { grid-template-columns: 1fr !important; }
}
</style>