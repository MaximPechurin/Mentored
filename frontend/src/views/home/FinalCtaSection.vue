<template>
  <section class="msec msec-pad final-cta">
    <div class="container">
      <h2 class="section-title">Tu nuevo comienzo puede empezar con un solo paso.</h2>
      <p class="section-subtitle">Elige tu camino y comienza hoy tu transformación.</p>
      <div class="cta-buttons">
        <router-link to="/tienda" class="btn-primary">Empezar aquí</router-link>
        <router-link to="/tienda" class="btn-secondary">Ver productos</router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.msec-pad {
  padding: 96px 32px;
}

.final-cta {
  background: linear-gradient(180deg, #8e1519 0%, #5e0d11 100%);
}

.container {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 18px;
  line-height: 1.15;
  letter-spacing: -0.5px;
}

.section-subtitle {
  font-size: 20px;
  line-height: 1.55;
  color: #f4d3d4;
  margin: 0 auto 36px;
  max-width: 560px;
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  background: #ffffff;
  color: #8e1519;
  font-weight: 500;
  font-size: 17px;
  padding: 17px 34px;
  border-radius: 999px;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  background: transparent;
  border: 1.5px solid rgba(255,255,255,0.6);
  color: #fff;
  font-weight: 500;
  font-size: 17px;
  padding: 17px 34px;
  border-radius: 999px;
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .section-title { font-size: 27px !important; }
}
</style>