<template>
  <section class="c-steps-section">
    <div class="c-steps-container">
      <h2>¿Cómo funciona?</h2>
      <div class="c-steps">
        <div v-for="step in steps" :key="step.n" class="c-step">
          <div class="c-step-icon-wrapper">
            <div class="c-step-icon" v-html="step.icon"></div>
            <span class="c-step-number">{{ step.n }}</span>
          </div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.text }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    n: 1,
    icon: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
    title: 'Elige tu consulta',
    text: 'Explora las categorías y selecciona el experto que mejor se adapte a ti.'
  },
  {
    n: 2,
    icon: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 16l2 2 4-4"/></svg>`,
    title: 'Reserva tu sesión',
    text: 'Selecciona el día y la hora que prefieras y confirma tu reserva.'
  },
  {
    n: 3,
    icon: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="15" height="14" rx="2"/><polygon points="22 7 17 11 22 15 22 7"/><polygon points="8 8 12 11 8 14 8 8" fill="currentColor" stroke="none"/></svg>`,
    title: 'Conéctate',
    text: 'Recibe el enlace y prepárate tu sesión en el entorno que prefieras.'
  },
  {
    n: 4,
    icon: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V18h6v-1.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>`,
    title: 'Obtén claridad',
    text: 'Trabaja con tu experto para obtener perspectivas y soluciones personalizadas.'
  },
  {
    n: 5,
    icon: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2 0-2.8a2 2 0 0 0-3-.2z"/><path d="M12 15l-3-3a11 11 0 0 1 7-9 11 11 0 0 1 1 7 11 11 0 0 1-9 7z"/><circle cx="15" cy="9" r="1"/></svg>`,
    title: 'Toma acción',
    text: 'Recibe tu plan de acción y los siguientes pasos para avanzar con confianza.'
  }
]
</script>

<style scoped>
.c-steps-section {
  background: #ffffff;
  padding: 88px 32px;
}

.c-steps-container {
  max-width: 1320px;
  margin: 0 auto;
  text-align: center;
}

.c-steps-container h2 {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 60px;
  letter-spacing: -0.5px;
}

.c-steps {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
  text-align: center;
}

.c-step {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.c-step-icon-wrapper {
  position: relative;
  margin-bottom: 22px;
}

.c-step-icon {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: #f5ebe5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8e1519;
}

.c-step-number {
  position: absolute;
  top: -6px;
  left: -6px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.c-step h3 {
  font-family: 'Playfair Display', serif;
  font-size: 21px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 10px;
}

.c-step p {
  font-size: 15.5px;
  line-height: 1.55;
  color: #6b6259;
  margin: 0;
  max-width: 200px;
}

@media (max-width: 860px) {
  .c-steps-section { padding: 56px 20px !important; }
  .c-steps { grid-template-columns: 1fr 1fr !important; gap: 32px 18px !important; }
  .c-sec h2 { font-size: 27px !important; }
}
@media (max-width: 520px) {
  .c-steps { grid-template-columns: 1fr !important; }
}
</style>