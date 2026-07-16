<template>
  <section class="bl-hero">
    <span class="bl-hero-tag">El blog de Mentored</span>
    <h1 class="bl-hero-title">Ideas para crecer con propósito</h1>
    <p class="bl-hero-sub">
      Reflexiones, herramientas y prácticas sobre energía, hábitos, claridad y crecimiento personal y profesional.
    </p>
  </section>
</template>

<style scoped>
.bl-hero {
  background: #0e0c0c;
  padding: 88px 32px 48px;
  text-align: center;
}

.bl-hero-tag {
  display: inline-block;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 20px;
}

.bl-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 54px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.bl-hero-sub {
  font-size: 19px;
  line-height: 1.6;
  color: #a59c93;
  margin: 0 auto;
  max-width: 600px;
}

@media (max-width: 900px) {
  .bl-hero { padding: 64px 20px 40px !important; }
  .bl-hero-title { font-size: 42px !important; }
}
</style>