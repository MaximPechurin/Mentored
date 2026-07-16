<template>
  <section class="c-hero">
    <div class="c-hero-grid">
      <div class="c-hero-txt">
        <span class="c-hero-tag">Consultas individuales</span>
        <h1 class="c-hero-title">
          Consultas individuales con expertos <span class="highlight-red">Mentored</span>
        </h1>
        <p class="c-hero-sub">
          Cuando necesitas una mirada personal, claridad y un plan hecho para tu momento actual.
        </p>
        <div class="c-hero-buttons">
          <a href="#categorias" class="btn-primary">
            Elegir experto
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </a>
          <a href="#destacadas" class="btn-secondary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Reservar
          </a>
        </div>
      </div>
      <div class="c-hero-img">
        <img src="/images/hero.png" alt="Irina Karbonova — Fundadora de Mentored">
        <div class="c-hero-img-overlay"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.c-hero {
  background: #0e0c0c;
}

.c-hero-grid {
  max-width: 1480px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: stretch;
  gap: 0;
}

.c-hero-txt {
  padding: 96px 48px 96px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}

.c-hero-tag {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #8e1519;
  margin-bottom: 22px;
}

.c-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 54px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 24px;
  letter-spacing: -0.5px;
}

.highlight-red { color: #8e1519; }

.c-hero-sub {
  font-size: 20px;
  line-height: 1.55;
  color: #a59c93;
  margin: 0 0 36px;
  max-width: 480px;
}

.c-hero-buttons {
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
  font-size: 17px;
  padding: 16px 30px;
  border-radius: 999px;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  background: transparent;
  border: 1.5px solid rgba(255,255,255,0.5);
  color: #fff;
  font-weight: 500;
  font-size: 17px;
  padding: 16px 30px;
  border-radius: 999px;
}

.c-hero-img {
  position: relative;
  min-height: 520px;
  background: #1a1212;
  overflow: hidden;
}

.c-hero-img img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  display: block;
}

.c-hero-img-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #0e0c0c 0%, rgba(14,12,12,0.55) 12%, rgba(14,12,12,0) 30%);
}

@media (max-width: 860px) {
  .c-hero-grid { grid-template-columns: 1fr !important; }
  .c-hero-txt { padding: 56px 20px !important; }
  .c-hero-txt h1 { font-size: 38px !important; }
  .c-hero-img { min-height: 280px !important; order: -1; }
  .c-hero-img-overlay { background: linear-gradient(180deg, rgba(14,12,12,0.15) 0%, rgba(14,12,12,0.55) 100%) !important; }
}
</style>