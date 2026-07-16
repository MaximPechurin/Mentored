<template>
  <section id="destacadas" class="c-featured">
    <div class="c-featured-head">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c49a3f" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      </svg>
      <h2>Consultas destacadas</h2>
    </div>
    <div class="c-dest">
      <div v-for="c in consultas" :key="c.title" class="c-dest-card">
        <div class="c-dest-img">
          <img :src="c.img" :alt="c.title">
        </div>
        <div class="c-dest-body">
          <h3>{{ c.title }}</h3>
          <div class="c-dest-meta">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8e1519" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="9"/>
              <polyline points="12 7 12 12 15 14"/>
            </svg>
            {{ c.duration }}
          </div>
          <div class="c-dest-meta">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8e1519" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="23 7 16 12 23 17 23 7"/>
              <rect x="1" y="5" width="15" height="14" rx="2"/>
            </svg>
            Videollamada 1:1
          </div>
          <div class="c-dest-footer">
            <span class="c-dest-price">{{ c.price }}</span>
            <a href="#" class="btn-reservar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              Reservar
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const consultas = [
  { title: 'Consulta con Irina', duration: '60 minutos', price: '$297', img: '/images/consulta-card.png' },
  { title: 'Consulta psicológica', duration: '50 minutos', price: '$120', img: '/images/consulta-card.png' },
  { title: 'Consulta de coaching', duration: '60 minutos', price: '$150', img: '/images/consulta-card.png' },
  { title: 'Consulta financiera', duration: '60 minutos', price: '$130', img: '/images/consulta-card.png' }
]
</script>

<style scoped>
.c-featured {
  background: #f5eee3;
  padding: 80px 32px;
}

.c-featured-head {
  max-width: 1320px;
  margin: 0 auto 40px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.c-featured-head h2 {
  font-family: 'Playfair Display', serif;
  font-size: 38px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
  letter-spacing: -0.5px;
}

.c-dest {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.c-dest-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 44px -30px rgba(0,0,0,0.35);
  display: flex;
  flex-direction: column;
}

.c-dest-img {
  aspect-ratio: 430/284;
  overflow: hidden;
  background: #1a1212;
}

.c-dest-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.c-dest-body {
  padding: 26px 26px 28px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.c-dest-body h3 {
  font-family: 'Playfair Display', serif;
  font-size: 23px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 18px;
}

.c-dest-meta {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #6b6259;
  font-size: 15.5px;
  margin-bottom: 10px;
}

.c-dest-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: auto;
}

.c-dest-price {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 800;
  color: #8e1519;
}

.btn-reservar {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 500;
  font-size: 15px;
  padding: 12px 20px;
  border-radius: 999px;
  white-space: nowrap;
}

@media (max-width: 860px) {
  .c-featured { padding: 56px 20px !important; }
  .c-featured-head h2 { font-size: 30px !important; }
  .c-dest { grid-template-columns: 1fr 1fr !important; gap: 18px !important; }
}
@media (max-width: 520px) {
  .c-dest { grid-template-columns: 1fr !important; }
}
</style>