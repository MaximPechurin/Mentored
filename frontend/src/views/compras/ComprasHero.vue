<template>
  <section class="cp-hero">
    <div class="cp-hero-container">
      <span class="cp-hero-tag">Compras seguras</span>
      <h1 class="cp-hero-title">Condiciones de compra y devoluciones</h1>
      <p class="cp-hero-sub">
        Todo lo que necesitas saber antes y después de comprar en Mentored: cómo se realiza el pedido, los pagos y cuándo puedes solicitar un reembolso.
      </p>
    </div>
  </section>
</template>

<style scoped>
.cp-hero {
  background: #0e0c0c;
  padding: 88px 32px 52px;
}

.cp-hero-container {
  max-width: 920px;
  margin: 0 auto;
}

.cp-hero-tag {
  display: inline-block;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 20px;
}

.cp-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 52px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.cp-hero-sub {
  font-size: 18px;
  line-height: 1.6;
  color: #a59c93;
  margin: 0;
  max-width: 580px;
}

@media (max-width: 860px) {
  .cp-hero { padding: 64px 20px 40px !important; }
  .cp-hero-title { font-size: 40px !important; }
}
</style>