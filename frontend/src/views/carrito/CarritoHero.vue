<template>
  <section class="cr-hero">
    <div class="cr-hero-container">
      <h1 class="cr-hero-title">Tu Carrito</h1>
    </div>
  </section>
</template>

<style scoped>
.cr-hero {
  background: #0e0c0c;
  padding: 64px 32px;
}

.cr-hero-container {
  max-width: 1320px;
  margin: 0 auto;
}

.cr-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 54px;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.5px;
}

@media (max-width: 860px) {
  .cr-hero { padding: 48px 20px !important; }
  .cr-hero-title { font-size: 38px !important; }
}
</style>