<template>
  <section class="msec msec-pad test-cta">
    <div class="container">
      <div class="test-icon">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
        </svg>
      </div>
      <h2 class="section-title">¿No sabes por dónde empezar?</h2>
      <p class="section-subtitle">Responde 5 preguntas y descubre tu punto de partida ideal para comenzar tu transformación.</p>
      <!-- <a href="#" class="btn-primary">
        Hacer el test gratis
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"/>
          <polyline points="12 5 19 12 12 19"/>
        </svg>
      </a> МБ ВЕРНУТЬ В ДАЛЬНЕЙШЕМ -->
    </div>
  </section>
</template>

<style scoped>
.msec-pad {
  padding: 96px 32px;
}

.test-cta {
  background: #0e0c0c;
}

.container {
  max-width: 760px;
  margin: 0 auto;
  text-align: center;
}

.test-icon {
  width: 66px;
  height: 66px;
  border-radius: 50%;
  border: 2px solid #c49a3f;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c49a3f;
  margin: 0 auto 30px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.section-subtitle {
  font-size: 19px;
  line-height: 1.6;
  color: #8f8780;
  margin: 0 auto 38px;
  max-width: 560px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 500;
  font-size: 17px;
  padding: 17px 36px;
  border-radius: 999px;
  box-shadow: 0 0 34px -6px rgba(142,21,25,0.75);
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .section-title { font-size: 27px !important; }
}
</style>