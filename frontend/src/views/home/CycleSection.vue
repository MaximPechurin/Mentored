<template>
  <section class="msec msec-pad cycle">
    <div class="container">
      <h2 class="section-title">Así se vive Mentored mes a mes</h2>
      <p class="section-subtitle">Un ciclo mensual diseñado para acompañarte en todas las áreas de tu vida.</p>

      <div class="grid-4">
        <div v-for="item in cycle" :key="item.week" class="cycle-card">
          <span class="cycle-week">{{ item.week }}</span>
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  cycle: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.msec-pad {
  padding: 88px 32px;
}

.cycle {
  background: #0e0c0c;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 14px;
  letter-spacing: -0.5px;
}

.section-subtitle {
  font-size: 19px;
  color: #a59c93;
  margin: 0 auto 56px;
  max-width: 680px;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 22px;
  text-align: left;
}

.cycle-card {
  background: #181414;
  border: 1px solid #262020;
  border-radius: 18px;
  padding: 32px 28px;
}

.cycle-week {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 16px;
}

.cycle-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 10px;
}

.cycle-card p {
  font-size: 16px;
  line-height: 1.55;
  color: #a59c93;
  margin: 0;
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .section-title { font-size: 27px !important; }
  .grid-4 { grid-template-columns: 1fr 1fr !important; }
}

@media (max-width: 520px) {
  .grid-4 { grid-template-columns: 1fr !important; }
}
</style>