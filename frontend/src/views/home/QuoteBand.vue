<template>
  <section class="quote-band">
    <p>«Tu bienestar no es un lujo. Es tu base para todo lo demás.»</p>
  </section>
</template>

<style scoped>
.quote-band {
  background: #f5eee3;
  padding: 52px 32px;
}

.quote-band p {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 30px;
  line-height: 1.4;
  color: #3a2f28;
  font-weight: 500;
}

@media (max-width: 860px) {
  .quote-band { padding: 40px 20px !important; }
  .quote-band p { font-size: 22px !important; }
}
</style>