<template>
  <div class="ct-grid">
    <!-- Форма -->
    <div class="ct-form-wrapper">
      <template v-if="!sent">
        <h2 class="ct-form-title">Envíanos un mensaje</h2>
        <form @submit.prevent="onSubmit" class="ct-form">
          <div class="ct-fields">
            <div>
              <label>Nombre *</label>
              <input
                id="ct-nombre"
                type="text"
                placeholder="Tu nombre"
                v-model="form.name"
              >
            </div>
            <div>
              <label>Email *</label>
              <input
                id="ct-email"
                type="email"
                placeholder="tu@email.com"
                v-model="form.email"
              >
            </div>
          </div>

          <div class="ct-field-full">
            <label>Motivo</label>
            <select id="ct-motivo" v-model="form.motivo">
              <option>Consulta sobre cursos</option>
              <option>Reservar una consulta 1:1</option>
              <option>Mi pedido o pago</option>
              <option>Devoluciones</option>
              <option>Colaboraciones</option>
              <option>Otro</option>
            </select>
          </div>

          <div class="ct-field-full">
            <label>Mensaje *</label>
            <textarea
              id="ct-mensaje"
              rows="5"
              placeholder="Cuéntanos en qué podemos ayudarte"
              v-model="form.message"
            ></textarea>
          </div>

          <p v-if="error" class="ct-error">{{ error }}</p>

          <button type="submit" class="ct-submit-btn">
            Enviar mensaje
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </form>
      </template>

      <!-- Спасибо -->
      <template v-else>
        <div class="ct-thanks">
          <div class="ct-thanks-icon">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
          <h2 class="ct-thanks-title">¡Mensaje enviado!</h2>
          <p class="ct-thanks-text">
            Gracias por escribirnos. Te responderemos a tu correo en un plazo de 24-48 horas.
          </p>
          <button @click="resetForm" class="ct-thanks-btn">Enviar otro mensaje</button>
        </div>
      </template>
    </div>

    <!-- Блоки контактов -->
    <div class="ct-contact-blocks">
      <!-- WhatsApp -->
      <a href="https://wa.me/51940304595" class="ct-block ct-block-whatsapp">
        <div class="ct-block-header">
          <span class="ct-block-icon ct-icon-whatsapp">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
          </span>
          <div>
            <span class="ct-block-label">WhatsApp</span>
            <span class="ct-block-sub">Respuesta más rápida</span>
          </div>
        </div>
        <span class="ct-block-value">+51 940 304 595</span>
      </a>

      <!-- Email -->
      <a href="mailto:hola@mentored.com" class="ct-block ct-block-email">
        <div class="ct-block-header">
          <span class="ct-block-icon ct-icon-email">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="4" width="20" height="16" rx="2"/>
              <path d="m22 7-10 6L2 7"/>
            </svg>
          </span>
          <div>
            <span class="ct-block-label">Email</span>
            <span class="ct-block-sub">Para consultas detalladas</span>
          </div>
        </div>
        <span class="ct-block-value ct-email-value">hola@mentored.com</span>
      </a>

      <!-- Horario -->
      <div class="ct-block ct-block-hours">
        <div class="ct-block-header">
          <span class="ct-block-icon ct-icon-hours">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="9"/>
              <polyline points="12 7 12 12 15 14"/>
            </svg>
          </span>
          <span class="ct-block-label">Horario de atención</span>
        </div>
        <p class="ct-hours-text">
          Lunes a viernes, 9:00 – 18:00<br>Respondemos en 24-48 h hábiles.
        </p>
        <div class="ct-social-links">
          <a href="https://www.instagram.com/irina.karbonova?utm_source=qr" aria-label="Instagram">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="2" y="2" width="20" height="20" rx="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>
            </svg>
          </a>
          <a href="https://youtube.com/mentored" aria-label="YouTube">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">
              <path d="M22.5 6.4a2.8 2.8 0 0 0-1.9-2C18.9 4 12 4 12 4s-6.9 0-8.6.4a2.8 2.8 0 0 0-1.9 2A29 29 0 0 0 1.1 12a29 29 0 0 0 .4 5.6 2.8 2.8 0 0 0 1.9 2C5.1 20 12 20 12 20s6.9 0 8.6-.4a2.8 2.8 0 0 0 1.9-2 29 29 0 0 0 .4-5.6 29 29 0 0 0-.4-5.6z"/>
              <polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="currentColor"/>
            </svg>
          </a>
          <a href="https://facebook.com/mentored" aria-label="Facebook">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const sent = ref(false)
const error = ref('')
const form = ref({
  name: '',
  email: '',
  motivo: 'Consulta sobre cursos',
  message: ''
})

const onSubmit = () => {
  if (!form.value.name || !form.value.email || !form.value.message) {
    error.value = 'Por favor completa tu nombre, email y mensaje.'
    return
  }
  error.value = ''
  sent.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetForm = () => {
  sent.value = false
  form.value = { name: '', email: '', motivo: 'Consulta sobre cursos', message: '' }
  error.value = ''
}
</script>

<style scoped>
.ct-grid {
  max-width: 1160px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 36px;
  padding: 56px 32px 32px;
  align-items: start;
}

/* --- ФОРМА --- */
.ct-form-wrapper {
  background: #ffffff;
  border-radius: 20px;
  padding: 38px;
  box-shadow: 0 22px 50px -36px rgba(0,0,0,0.45);
}

.ct-form-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.ct-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}

.ct-fields label,
.ct-field-full label {
  display: block;
  font-size: 14.5px;
  color: #15110f;
  margin-bottom: 8px;
}

.ct-fields input,
.ct-field-full input,
.ct-field-full select,
.ct-field-full textarea {
  width: 100%;
  border: 1px solid #e4ddd2;
  border-radius: 12px;
  padding: 14px 15px;
  font-size: 16px;
  font-family: inherit;
  color: #15110f;
  outline: none;
  background: #fbf9f6;
  transition: border-color 0.3s;
}

.ct-fields input:focus,
.ct-field-full select:focus,
.ct-field-full textarea:focus {
  border-color: #8e1519;
}

.ct-field-full {
  margin-bottom: 18px;
}

.ct-field-full textarea {
  resize: vertical;
  line-height: 1.5;
}

.ct-error {
  margin: 0 0 16px;
  color: #8e1519;
  font-size: 14.5px;
  font-weight: 500;
}

.ct-submit-btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  border: none;
  cursor: pointer;
  background: #8e1519;
  color: #fff;
  font-family: inherit;
  font-size: 16.5px;
  font-weight: 600;
  padding: 15px 32px;
  border-radius: 12px;
  transition: background 0.3s;
}

.ct-submit-btn:hover {
  background: #a01a1f;
}

/* --- СПАСИБО --- */
.ct-thanks {
  text-align: center;
  padding: 24px 8px;
}

.ct-thanks-icon {
  width: 74px;
  height: 74px;
  border-radius: 50%;
  background: #e3f1e8;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1f7a3d;
  margin: 0 auto 22px;
}

.ct-thanks-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 12px;
}

.ct-thanks-text {
  font-size: 17px;
  line-height: 1.6;
  color: #6b6259;
  margin: 0 0 26px;
  max-width: 380px;
  margin-left: auto;
  margin-right: auto;
}

.ct-thanks-btn {
  border: 1.5px solid #0e0c0c;
  background: none;
  cursor: pointer;
  color: #0e0c0c;
  font-family: inherit;
  font-size: 15.5px;
  font-weight: 600;
  padding: 13px 28px;
  border-radius: 12px;
  transition: all 0.3s;
}

.ct-thanks-btn:hover {
  background: #0e0c0c;
  color: #fff;
}

/* --- БЛОКИ КОНТАКТОВ --- */
.ct-contact-blocks {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ct-block {
  display: block;
  text-decoration: none;
  border-radius: 18px;
  padding: 26px 28px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.ct-block:hover {
  transform: translateY(-2px);
}

.ct-block-whatsapp {
  background: #0e0c0c;
}

.ct-block-email {
  background: #ffffff;
  box-shadow: 0 18px 44px -36px rgba(0,0,0,0.4);
}

.ct-block-email:hover {
  box-shadow: 0 22px 48px -36px rgba(0,0,0,0.5);
}

.ct-block-hours {
  background: #ffffff;
  border-radius: 18px;
  padding: 26px 28px;
  box-shadow: 0 18px 44px -36px rgba(0,0,0,0.4);
}

.ct-block-header {
  display: flex;
  align-items: center;
  gap: 13px;
  margin-bottom: 12px;
}

.ct-block-icon {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ct-icon-whatsapp {
  background: #8e1519;
  color: #fff;
}

.ct-icon-email {
  background: #f7ece9;
  color: #8e1519;
}

.ct-icon-hours {
  background: #faf2e2;
  color: #b3852f;
}

.ct-block-label {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.ct-block-email .ct-block-label {
  color: #15110f;
}

.ct-block-hours .ct-block-label {
  color: #15110f;
}

.ct-block-sub {
  display: block;
  font-size: 14px;
  color: #9a938d;
}

.ct-block-value {
  font-size: 16px;
  color: #cfc7be;
}

.ct-email-value {
  color: #8e1519 !important;
}

.ct-hours-text {
  font-size: 15.5px;
  line-height: 1.6;
  color: #6b6259;
  margin: 0 0 18px;
}

.ct-social-links {
  display: flex;
  gap: 10px;
}

.ct-social-links a {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f3ece2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3a332e;
  text-decoration: none;
  transition: background 0.3s;
}

.ct-social-links a:hover {
  background: #e5dcd0;
}

@media (max-width: 920px) {
  .ct-grid {
    grid-template-columns: 1fr !important;
    gap: 24px !important;
    padding: 40px 20px 24px !important;
  }
  .ct-fields {
    grid-template-columns: 1fr !important;
  }
}
</style>