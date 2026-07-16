<template>
  <section class="msec msec-pad feelings">
    <div class="container">
      <span class="section-tag">Quizás te identificas</span>
      <h2 class="section-title">¿Cómo te sientes hoy?</h2>
      <p class="section-subtitle">Si algo de esto resuena contigo, estás en el lugar correcto.</p>

      <div class="grid-3">
        <div v-for="feeling in feelings" :key="feeling.title" class="feeling-card">
          <div class="feeling-icon" v-html="feeling.icon"></div>
          <h3>{{ feeling.title }}</h3>
          <p>{{ feeling.text }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  feelings: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.msec-pad {
  padding: 88px 32px;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  text-align: center;
}

.section-tag {
  display: inline-block;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #8e1519;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 14px;
  letter-spacing: -0.5px;
}

.section-subtitle {
  font-size: 19px;
  color: #6b6259;
  margin: 0 auto 52px;
  max-width: 620px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  text-align: left;
}

.feeling-card {
  background: #faf6f0;
  border: 1px solid #eee3d6;
  border-radius: 18px;
  padding: 32px 30px;
}

.feeling-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: #f1e3de;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8e1519;
  margin-bottom: 20px;
}

.feeling-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 23px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 8px;
}

.feeling-card p {
  font-size: 16.5px;
  line-height: 1.55;
  color: #6b6259;
  margin: 0;
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .section-title { font-size: 27px !important; }
  .grid-3 { grid-template-columns: 1fr !important; }
}
</style>