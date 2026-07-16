<template>
  <section class="ct-hero">
    <div class="ct-hero-container">
      <span class="ct-hero-tag">Contacto</span>
      <h1 class="ct-hero-title">Hablemos</h1>
      <p class="ct-hero-sub">
        ¿Tienes una duda sobre un curso, una consulta o tu pedido?
        Escríbenos y te respondemos lo antes posible.
      </p>
    </div>
  </section>
</template>

<style scoped>
.ct-hero {
  background: #0e0c0c;
  padding: 88px 32px 48px;
}

.ct-hero-container {
  max-width: 1160px;
  margin: 0 auto;
}

.ct-hero-tag {
  display: inline-block;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 20px;
}

.ct-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 54px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.ct-hero-sub {
  font-size: 19px;
  line-height: 1.6;
  color: #a59c93;
  margin: 0;
  max-width: 560px;
}

@media (max-width: 920px) {
  .ct-hero { padding: 64px 20px 40px !important; }
  .ct-hero-title { font-size: 42px !important; }
}
</style>