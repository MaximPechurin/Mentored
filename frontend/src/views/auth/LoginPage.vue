<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Левая часть: форма -->
      <div class="auth-form-wrapper">
        <div class="auth-form">
          <span class="auth-tag">Bienvenido de nuevo</span>
          <h1 class="auth-title">Iniciar sesión</h1>
          <p class="auth-subtitle">Accede a tu cuenta para continuar tu camino de transformación.</p>

          <form @submit.prevent="handleLogin" class="auth-form-fields">
            <div class="auth-field">
              <label>Email</label>
              <input
                type="email"
                v-model="form.email"
                placeholder="tu@email.com"
                required
              >
            </div>

            <div class="auth-field">
              <label>Contraseña</label>
              <div class="auth-password-wrapper">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="form.password"
                  placeholder="••••••••"
                  required
                >
                <button
                  type="button"
                  class="auth-password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <svg v-if="!showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="auth-options">
              <label class="auth-remember">
                <input type="checkbox" v-model="form.remember">
                Recordarme
              </label>
              <a href="#" class="auth-forgot">¿Olvidaste tu contraseña?</a>
            </div>

            <button type="submit" class="auth-submit-btn" :disabled="loading">
              <span v-if="!loading">Iniciar sesión</span>
              <span v-else>Cargando...</span>
            </button>
          </form>

          <p class="auth-footer">
            ¿No tienes cuenta? <router-link to="/register" class="auth-link">Regístrate aquí</router-link>
          </p>
        </div>
      </div>

      <!-- Правая часть: баннер -->
      <div class="auth-banner">
        <div class="auth-banner-content">
          <span class="auth-banner-tag">Mentored</span>
          <h2 class="auth-banner-title">Tu camino de transformación empieza aquí</h2>
          <p class="auth-banner-text">
            Accede a tus cursos, consultas y recursos para seguir creciendo con propósito.
          </p>
          <div class="auth-banner-quote">
            «No se trata de hacerlo perfecto. Se trata de volver a ti y avanzar.»
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from "../../composables/useAuth.js";
import { useRouter } from 'vue-router'
import { authApi } from '../../api/auth'

const router = useRouter()
const { setUser } = useAuth()
const loading = ref(false)
const showPassword = ref(false)

const form = ref({
  email: '',
  password: '',
  remember: false,
})

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    alert('Por favor completa todos los campos.')
    return
  }

  loading.value = true
  try {
    const response = await authApi.login(form.value.email, form.value.password)

    // Сохраняем токены
    authApi.setTokens(response.data.access, response.data.refresh)

    // Получаем профиль пользователя
    const profileResponse = await authApi.getProfile()
    setUser(profileResponse.data)
    //localStorage.setItem('user', JSON.stringify(profileResponse.data))

    // Редирект на главную
    router.push('/')
  } catch (error) {
    console.error('Error de login:', error)
    alert('Email o contraseña incorrectos.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #f5eee3;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
}

.auth-container {
  max-width: 1120px;
  width: 100%;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  background: #ffffff;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 40px 80px -32px rgba(0,0,0,0.35);
}

/* === ЛЕВАЯ ЧАСТЬ — ФОРМА === */
.auth-form-wrapper {
  padding: 56px 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 12px;
}

.auth-title {
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  font-size: 16px;
  color: #6b6259;
  margin: 0 0 32px;
}

/* === ПОЛЯ ФОРМЫ === */
.auth-field {
  margin-bottom: 20px;
}

.auth-field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #15110f;
  margin-bottom: 6px;
}

.auth-field input,
.auth-field select {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #e4ddd2;
  border-radius: 12px;
  font-size: 16px;
  font-family: inherit;
  color: #15110f;
  background: #fbf9f6;
  outline: none;
  transition: border-color 0.3s;
}

.auth-field input:focus {
  border-color: #8e1519;
}

.auth-password-wrapper {
  position: relative;
}

.auth-password-wrapper input {
  padding-right: 48px;
}

.auth-password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #a89f93;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-password-toggle:hover {
  color: #6b6259;
}

/* === ОПЦИИ === */
.auth-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  font-size: 14.5px;
}

.auth-remember {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b6259;
  cursor: pointer;
}

.auth-remember input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #8e1519;
  cursor: pointer;
}

.auth-forgot {
  color: #8e1519;
  text-decoration: none;
  font-weight: 500;
}

.auth-forgot:hover {
  text-decoration: underline;
}

/* === КНОПКА === */
.auth-submit-btn {
  width: 100%;
  padding: 16px;
  background: #8e1519;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.3s;
}

.auth-submit-btn:hover:not(:disabled) {
  background: #a01a1f;
}

.auth-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* === ФУТЕР === */
.auth-footer {
  text-align: center;
  font-size: 15px;
  color: #6b6259;
  margin-top: 24px;
}

.auth-link {
  color: #8e1519;
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}

/* === ПРАВАЯ ЧАСТЬ — БАННЕР === */
.auth-banner {
  background: #0e0c0c;
  padding: 56px 44px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-banner-content {
  max-width: 380px;
}

.auth-banner-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 16px;
}

.auth-banner-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  line-height: 1.15;
  letter-spacing: -0.3px;
}

.auth-banner-text {
  font-size: 16px;
  line-height: 1.6;
  color: #a59c93;
  margin: 0 0 32px;
}

.auth-banner-quote {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 18px;
  line-height: 1.5;
  color: #9a9088;
  padding-top: 24px;
  border-top: 1px solid #262020;
}

/* === АДАПТИВ === */
@media (max-width: 920px) {
  .auth-container {
    grid-template-columns: 1fr;
    border-radius: 20px;
  }

  .auth-form-wrapper {
    padding: 40px 28px;
  }

  .auth-banner {
    padding: 40px 28px;
    min-height: 220px;
  }

  .auth-banner-title {
    font-size: 26px;
  }
}

@media (max-width: 520px) {
  .auth-form-wrapper {
    padding: 28px 20px;
  }

  .auth-title {
    font-size: 28px;
  }

  .auth-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>