<template>
  <footer class="ft-wrap">
    <div class="ft-grid">
      <!-- Бренд -->
      <div class="ft-brand">
        <div class="brand-logo">
          <img src="/images/logo.png" alt="Mentored">
        </div>
        <p class="brand-desc">Crecimiento personal y profesional con propósito.</p>
        <div class="social-links">
          <a href="https://instagram.com/mentored" aria-label="Instagram">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="2" y="2" width="20" height="20" rx="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>
            </svg>
          </a>
          <a href="https://facebook.com/mentored" aria-label="Facebook">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
          </a>
          <a href="https://youtube.com/mentored" aria-label="YouTube">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">
              <path d="M22.5 6.4a2.8 2.8 0 0 0-1.9-2C18.9 4 12 4 12 4s-6.9 0-8.6.4a2.8 2.8 0 0 0-1.9 2A29 29 0 0 0 1.1 12a29 29 0 0 0 .4 5.6 2.8 2.8 0 0 0 1.9 2C5.1 20 12 20 12 20s6.9 0 8.6-.4a2.8 2.8 0 0 0 1.9-2 29 29 0 0 0 .4-5.6 29 29 0 0 0-.4-5.6z"/>
              <polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="currentColor"/>
            </svg>
          </a>
          <a href="https://linkedin.com/company/mentored" aria-label="LinkedIn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM10 9h3.8v1.7h.05a4.2 4.2 0 0 1 3.75-2c4 0 4.75 2.6 4.75 6V21h-4v-5.3c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V21h-4z"/>
            </svg>
          </a>
        </div>
      </div>

      <!-- Навигация -->
      <div>
        <h4>Navegación</h4>
        <ul>
          <li><router-link to="/cursos">Cursos</router-link></li>
          <li><router-link to="/consultas">Consultas</router-link></li>
          <li><router-link to="/expertos">Expertos</router-link></li>
          <li><router-link to="/tienda">Tienda</router-link></li>
          <li><router-link to="/comunidad">Comunidad</router-link></li>
        </ul>
      </div>

      <!-- Ресурсы -->
      <div>
        <h4>Recursos</h4>
        <ul>
          <li><router-link to="/gratis">Gratis</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li><router-link to="/cuenta">Mi cuenta</router-link></li>
          <li><a href="#">Test gratuito</a></li>
          <li><a href="#">Eventos</a></li>
        </ul>
      </div>

      <!-- Контакты -->
      <div>
        <h4>Contacto</h4>
        <ul>
          <li>
            <a href="https://wa.me/0000000000" class="contact-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
              WhatsApp
            </a>
          </li>
          <li>
            <a href="mailto:hola@mentored.com" class="contact-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-10 6L2 7"/>
              </svg>
              hola@mentored.com
            </a>
          </li>
          <li><router-link to="/contacto">Formulario de contacto</router-link></li>
          <li><router-link to="/ayuda">Ayuda y devoluciones</router-link></li>
        </ul>
      </div>

      <!-- Подписка -->
      <div>
        <h4>Suscríbete</h4>
        <p class="subscribe-text">Recibe inspiración, recursos y novedades en tu correo.</p>
        <form @submit.prevent="handleSubscribe" class="subscribe-form">
          <input type="email" placeholder="Tu correo electrónico" required>
          <button type="submit" aria-label="Suscribirse">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </button>
        </form>
      </div>
    </div>

    <!-- Нижняя часть -->
    <div class="ft-bottom">
      <p>© 2026 Mentored. Todos los derechos reservados.</p>
      <nav>
        <router-link to="/legal">Aviso legal y privacidad</router-link>
        <router-link to="/compras">Condiciones de compra</router-link>
      </nav>
    </div>
  </footer>
</template>

<script setup>
const handleSubscribe = () => {
  alert('¡Gracias por suscribirte! Pronto recibirás novedades.')
}
</script>

<style scoped>

.ft-wrap {
  background: #0e0c0c;
  color: #cfc9c4;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  padding: 72px 32px 36px;
  width: 100%;
}

.ft-grid {
  max-width: 1480px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr 1fr 1.3fr;
  gap: 40px;
}

.ft-brand {
  display: flex;
  flex-direction: column;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 20px;
}

.brand-logo img {
  display: block;
  flex-shrink: 0;
  height: 34px;
  width: auto;
}

.brand-desc {
  font-size: 16px;
  line-height: 1.6;
  color: #9a938d;
  max-width: 240px;
  margin: 0 0 24px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-links a {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #211d1d;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cfc9c4;
  text-decoration: none;
  transition: background 0.3s;
}

.social-links a:hover {
  background: #322d2d;
}

.ft-grid h4 {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #ffffff;
  margin: 0 0 22px;
}

.ft-grid ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ft-grid ul li a {
  text-decoration: none;
  color: #9a938d;
  font-size: 16px;
  transition: color 0.3s;
}

.ft-grid ul li a:hover {
  color: #ffffff;
}

.contact-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #9a938d;
  font-size: 16px;
}

.contact-link svg {
  flex-shrink: 0;
  color: #8e1519;
}

.subscribe-text {
  font-size: 16px;
  line-height: 1.6;
  color: #9a938d;
  margin: 0 0 18px;
}

.subscribe-form {
  display: flex;
  align-items: stretch;
  background: #211d1d;
  border-radius: 12px;
  overflow: hidden;
  max-width: 320px;
}

.subscribe-form input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  color: #fff;
  font-size: 15px;
  padding: 14px 16px;
  font-family: inherit;
}

.subscribe-form input::placeholder {
  color: #6f6862;
}

.subscribe-form button {
  border: none;
  background: #8e1519;
  color: #fff;
  padding: 0 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.subscribe-form button:hover {
  background: #a01a1f;
}

.ft-bottom {
  max-width: 1480px;
  margin: 56px auto 0;
  border-top: 1px solid #211d1d;
  padding-top: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
}

.ft-bottom p {
  font-size: 15px;
  color: #6f6862;
  margin: 0;
}

.ft-bottom nav {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.ft-bottom nav a {
  text-decoration: none;
  color: #8a837d;
  font-size: 14.5px;
  transition: color 0.3s;
}

.ft-bottom nav a:hover {
  color: #ffffff;
}

@media (max-width: 900px) {
  .ft-wrap { padding: 52px 20px 32px !important; }
  .ft-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 32px 24px !important;
  }
  .ft-brand { grid-column: 1 / -1 !important; }
  .ft-bottom { margin-top: 40px !important; }
}

@media (max-width: 540px) {
  .ft-grid { grid-template-columns: 1fr !important; }
}
</style>