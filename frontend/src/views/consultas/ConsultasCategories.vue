<template>
  <section id="categorias" class="c-categories">
    <div class="c-cats">
      <div v-for="cat in categories" :key="cat.key" class="c-cat-card">
        <div class="c-cat-icon" :class="cat.iconClass" v-html="cat.icon"></div>
        <h3>{{ cat.title }}</h3>
        <p>{{ cat.desc }}</p>
        <a href="#destacadas" class="c-cat-link">Ver consultas →</a>
      </div>
    </div>
  </section>
</template>

<script setup>
const categories = [
  {
    key: 'irina',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>`,
    iconClass: 'icon-red',
    title: 'Con Irina',
    desc: 'Sesiones 1:1 con Irina Karbonova para claridad, estrategia y dirección.'
  },
  {
    key: 'psicologia',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A4.5 4.5 0 0 0 5 6.5c0 1 .3 1.5-.5 2.5S3 11 3 12.5 4 15 5 15.5c0 2 1.5 3.5 3.5 3.5a3 3 0 0 0 3-3V4.5A2.5 2.5 0 0 0 9.5 2z"/><path d="M14.5 2A4.5 4.5 0 0 1 19 6.5c0 1-.3 1.5.5 2.5s1.5 2 1.5 3.5-1 2.5-2 3c0 2-1.5 3.5-3.5 3.5a3 3 0 0 1-3-3V4.5A2.5 2.5 0 0 1 14.5 2z"/></svg>`,
    iconClass: 'icon-purple',
    title: 'Psicología',
    desc: 'Bienestar emocional, mente y relaciones.'
  },
  {
    key: 'coaching',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1z"/><path d="M8 11l2.5 2.5L16 8"/></svg>`,
    iconClass: 'icon-gold',
    title: 'Coaching',
    desc: 'Desarrollo personal y liderazgo.'
  },
  {
    key: 'finanzas',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`,
    iconClass: 'icon-green',
    title: 'Finanzas',
    desc: 'Educación financiera y abundancia.'
  },
  {
    key: 'carrera',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
    iconClass: 'icon-blue',
    title: 'Carrera',
    desc: 'Evolución profesional y propósito.'
  },
  {
    key: 'negocios',
    icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/><line x1="9" y1="15" x2="13" y2="15"/></svg>`,
    iconClass: 'icon-orange',
    title: 'Negocios',
    desc: 'Estrategia y crecimiento de tu emprendimiento.'
  }
]
</script>

<style scoped>
.c-categories {
  background: #ffffff;
  padding: 80px 32px;
}

.c-cats {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}

.c-cat-card {
  background: #ffffff;
  border: 1px solid #eee;
  border-radius: 18px;
  padding: 30px 22px;
  text-align: center;
  box-shadow: 0 14px 36px -28px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.c-cat-icon {
  width: 66px;
  height: 66px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}

.icon-red { background: #f1e3de; color: #8e1519; }
.icon-purple { background: #f1e7f7; color: #8b5cc7; }
.icon-gold { background: #f6edd9; color: #c49a3f; }
.icon-green { background: #e3f1e8; color: #3f9d5f; }
.icon-blue { background: #e3ecf9; color: #3a6fc4; }
.icon-orange { background: #fbeede; color: #d97a23; }

.c-cat-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 21px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 10px;
}

.c-cat-card p {
  font-size: 15px;
  line-height: 1.5;
  color: #6b6259;
  margin: 0 0 18px;
}

.c-cat-link {
  margin-top: auto;
  text-decoration: none;
  color: #8e1519;
  font-weight: 500;
  font-size: 15px;
}

@media (max-width: 860px) {
  .c-categories { padding: 56px 20px !important; }
  .c-cats { grid-template-columns: 1fr 1fr !important; gap: 16px !important; }
}
@media (max-width: 520px) {
  .c-cats { grid-template-columns: 1fr !important; }
}
</style>