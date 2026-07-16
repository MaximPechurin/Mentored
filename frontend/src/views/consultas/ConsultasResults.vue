<template>
  <section class="c-results-section">
    <div class="c-results-container">
      <h2>Resultados que puedes <span>esperar</span></h2>
      <div class="c-results">
        <div v-for="result in results" :key="result.key" class="c-result">
          <div class="c-result-icon" v-html="result.icon"></div>
          <h3>{{ result.title }}</h3>
          <p>{{ result.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const results = [
  {
    key: 'claridad',
    icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>`,
    title: 'Claridad',
    desc: 'Visualiza con nitidez tu situación actual y tu camino a seguir.'
  },
  {
    key: 'enfoque',
    icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
    title: 'Enfoque',
    desc: 'Identifica tus prioridades y enfoca tu energía en lo que realmente importa.'
  },
  {
    key: 'plan',
    icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2h6a1 1 0 0 1 1 1v1h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2V3a1 1 0 0 1 1-1z"/><path d="M9 13l2 2 4-4"/></svg>`,
    title: 'Plan de acción',
    desc: 'Recibe pasos concretos, medibles y personalizados para avanzar.'
  },
  {
    key: 'acompanamiento',
    icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    title: 'Acompañamiento',
    desc: 'Nunca estarás solo/a. Cuenta con seguimiento continuo y apoyo real.'
  }
]
</script>

<style scoped>
.c-results-section {
  background: #0e0c0c;
  padding: 88px 32px;
}

.c-results-container {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.c-results-container h2 {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 60px;
  letter-spacing: -0.5px;
}

.c-results-container h2 span {
  color: #c49a3f;
}

.c-results {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 36px;
}

.c-result {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.c-result-icon {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: #1c1818;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c49a3f;
  margin-bottom: 24px;
}

.c-result h3 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px;
}

.c-result p {
  font-size: 16px;
  line-height: 1.55;
  color: #a59c93;
  margin: 0;
  max-width: 240px;
}

@media (max-width: 860px) {
  .c-results-section { padding: 56px 20px !important; }
  .c-results { grid-template-columns: 1fr 1fr !important; gap: 36px 18px !important; }
  .c-sec h2 { font-size: 27px !important; }
}
@media (max-width: 520px) {
  .c-results { grid-template-columns: 1fr !important; }
}
</style>