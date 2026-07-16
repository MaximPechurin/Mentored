<template>
  <section class="c-cta">
    <div class="c-cta-container">
      <h2>Tu próximo paso puede cambiarlo todo.</h2>
      <p>Reserva tu consulta hoy y comienza tu transformación con el acompañamiento que mereces.</p>
      <a href="#destacadas" class="btn-cta">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        Reservar ahora
      </a>
    </div>
  </section>
</template>

<style scoped>
.c-cta {
  background: linear-gradient(180deg, #8e1519 0%, #5e0d11 100%);
  padding: 90px 32px;
}

.c-cta-container {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.c-cta-container h2 {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 18px;
  line-height: 1.15;
  letter-spacing: -0.5px;
}

.c-cta-container p {
  font-size: 19px;
  line-height: 1.55;
  color: #f4d3d4;
  margin: 0 auto 36px;
  max-width: 560px;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  background: #ffffff;
  color: #8e1519;
  font-weight: 500;
  font-size: 17px;
  padding: 17px 34px;
  border-radius: 999px;
}

@media (max-width: 860px) {
  .c-cta { padding: 56px 20px !important; }
  .c-cta-container h2 { font-size: 27px !important; }
}
</style>