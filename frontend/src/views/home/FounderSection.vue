<template>
  <section class="msec msec-pad founder">
    <div class="founder-grid">
      <div class="founder-image">
        <img src="/images/founder.png" alt="Irina Karbonova">
      </div>
      <div class="founder-content">
        <span class="section-tag">Sobre la fundadora</span>
        <h2 class="section-title">Irina Karbonova</h2>
        <p class="founder-role">CEO, emprendedora, psicóloga, autora y fundadora de Mentored.</p>
        <p class="founder-description">
          Acompaño a personas que quieren recuperar su voz, su claridad y su capacidad de actuar.
          Con más de 15 años de experiencia, mi misión es transformar vidas a través del desarrollo
          personal y estratégico.
        </p>

        <ul class="founder-bullets">
          <li v-for="item in bullets" :key="item.text">
            <span class="bullet-icon" v-html="item.icon"></span>
            {{ item.text }}
          </li>
        </ul>

        <div class="founder-buttons">
          <router-link to="/tienda" class="btn-primary">
            Ver programas
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </router-link>
          <router-link to="/consultas" class="btn-secondary">Reservar consulta</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  bullets: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.msec-pad {
  padding: 88px 32px;
}

.founder {
  background: #f5eee3;
}

.founder-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 0.85fr 1.15fr;
  gap: 64px;
  align-items: center;
}

.founder-image {
  aspect-ratio: 4/5;
  border-radius: 24px;
  overflow: hidden;
  background: #241b1b;
  box-shadow: 0 30px 60px -24px rgba(0,0,0,0.3);
}

.founder-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
}

.founder-content {
  display: flex;
  flex-direction: column;
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
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.founder-role {
  font-size: 18px;
  font-weight: 400;
  color: #8a8079;
  margin: 0 0 22px;
}

.founder-description {
  font-size: 18px;
  line-height: 1.65;
  color: #5d544c;
  margin: 0 0 28px;
  max-width: 620px;
}

.founder-bullets {
  list-style: none;
  margin: 0 0 32px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.founder-bullets li {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 17px;
  color: #3a332e;
}

.bullet-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f1e3de;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8e1519;
  flex-shrink: 0;
}

.founder-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 500;
  font-size: 16px;
  padding: 15px 28px;
  border-radius: 999px;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  background: transparent;
  border: 1.5px solid #d6cabb;
  color: #15110f;
  font-weight: 500;
  font-size: 16px;
  padding: 15px 28px;
  border-radius: 999px;
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .founder-grid { grid-template-columns: 1fr !important; gap: 36px !important; }
  .section-title { font-size: 27px !important; }
}
</style>