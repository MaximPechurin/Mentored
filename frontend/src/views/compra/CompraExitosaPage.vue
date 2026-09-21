<template>
  <div class="ce-page">
    <div class="ce-card">
      <template v-if="status === 'success'">
        <div class="ce-icon ce-icon--ok">✓</div>
        <h1 class="ce-title">¡Pago recibido!</h1>

        <p v-if="isNew" class="ce-text">
          Hemos creado tu cuenta y te enviamos la <strong>contraseña a tu correo</strong>.
          Ya puedes iniciar sesión y acceder a tu curso.
        </p>
        <p v-else class="ce-text">
          Tu compra se realizó con éxito. Inicia sesión con tu cuenta para
          acceder a tu curso.
        </p>

        <router-link to="/login" class="ce-btn">Iniciar sesión</router-link>
        <p class="ce-note">
          El acceso al curso se activa automáticamente tras confirmar el pago.
          Si no ves el correo, revisa la carpeta de spam.
        </p>
      </template>

      <template v-else-if="status === 'pending'">
        <div class="ce-icon ce-icon--pending">…</div>
        <h1 class="ce-title">Pago en proceso</h1>
        <p class="ce-text">
          Tu pago se está procesando. En cuanto se confirme, activaremos tu
          acceso y te enviaremos los datos por correo.
        </p>
        <router-link to="/" class="ce-btn ce-btn--ghost">Volver al inicio</router-link>
      </template>

      <template v-else>
        <div class="ce-icon ce-icon--fail">✕</div>
        <h1 class="ce-title">El pago no se completó</h1>
        <p class="ce-text">
          No se pudo procesar tu pago. Puedes intentarlo de nuevo desde el
          enlace de compra.
        </p>
        <router-link to="/" class="ce-btn ce-btn--ghost">Volver al inicio</router-link>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
// status: success | pending | failure (по умолчанию success — auto_return MP
// ведёт сюда только при одобрении, но параметр надёжнее).
const status = computed(() => route.query.status || 'success')
const isNew = computed(() => route.query.new === '1')
</script>

<style scoped>
.ce-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  background: #f5eee3;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
}

.ce-card {
  width: 100%;
  max-width: 520px;
  background: #fff;
  border-radius: 20px;
  padding: 44px 36px 38px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.ce-icon {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  font-weight: 700;
  margin: 0 auto 20px;
}
.ce-icon--ok { background: #e7f3ea; color: #2f7a3a; }
.ce-icon--pending { background: #fff4e0; color: #9a6a00; }
.ce-icon--fail { background: #fbe9e9; color: #8e1519; }

.ce-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 14px;
}

.ce-text {
  font-size: 15.5px;
  line-height: 1.6;
  color: #514b45;
  margin: 0 0 24px;
}
.ce-text strong { color: #15110f; }

.ce-btn {
  display: inline-block;
  background: #8e1519;
  color: #fff;
  border-radius: 999px;
  font-weight: 700;
  font-size: 15.5px;
  padding: 13px 30px;
  text-decoration: none;
  transition: background 0.15s;
}
.ce-btn:hover { background: #a01a1f; }
.ce-btn--ghost { background: #fff; color: #8e1519; border: 1px solid #e2b8b8; }
.ce-btn--ghost:hover { background: #fbe9e9; }

.ce-note { font-size: 13px; color: #8a8079; margin: 18px 0 0; line-height: 1.5; }
</style>
