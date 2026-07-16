<template>
  <section class="t-hero">
    <h1 class="t-hero-title">Tienda Mentored</h1>
    <p class="t-hero-sub">
      Cursos, consultas, libros y comunidad para tu transformación personal.
    </p>
  </section>
</template>

<style scoped>
.t-hero {
  background: #0e0c0c;
  padding: 84px 32px;
  text-align: center;
}

.t-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 62px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 18px;
  letter-spacing: -0.5px;
}

.t-hero-sub {
  font-size: 20px;
  line-height: 1.55;
  color: #a59c93;
  margin: 0 auto;
  max-width: 560px;
}

@media (max-width: 860px) {
  .t-hero { padding: 60px 20px !important; }
  .t-hero-title { font-size: 40px !important; }
}

@media (max-width: 520px) {
  .t-hero-title { font-size: 33px !important; }
}
</style>