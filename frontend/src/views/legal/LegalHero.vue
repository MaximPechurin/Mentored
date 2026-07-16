<template>
  <section class="lg-hero">
    <div class="lg-hero-container">
      <span class="lg-hero-tag">Información legal</span>
      <h1 class="lg-hero-title">Aviso legal y privacidad</h1>
      <p class="lg-hero-sub">
        Transparencia sobre quiénes somos, las condiciones de nuestros servicios y cómo tratamos tus datos.
      </p>
    </div>
  </section>
</template>

<style scoped>
.lg-hero {
  background: #0e0c0c;
  padding: 88px 32px 48px;
}

.lg-hero-container {
  max-width: 920px;
  margin: 0 auto;
}

.lg-hero-tag {
  display: inline-block;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 20px;
}

.lg-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 52px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.lg-hero-sub {
  font-size: 18px;
  line-height: 1.6;
  color: #a59c93;
  margin: 0;
  max-width: 560px;
}

@media (max-width: 860px) {
  .lg-hero { padding: 64px 20px 36px !important; }
  .lg-hero-title { font-size: 40px !important; }
}
</style>