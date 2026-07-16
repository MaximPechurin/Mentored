<template>
  <section class="msec msec-pad pillars">
    <div class="container">
      <span class="section-tag">Nuestros pilares</span>
      <h2 class="section-title">
        Tu camino de <span class="highlight">transformación</span> empieza aquí
      </h2>

      <div class="grid-4">
        <router-link to="/tienda" class="pillar-card">
          <div class="pillar-icon icon-red">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
            </svg>
          </div>
          <h3>Cursos</h3>
          <p>Formación práctica con metodología única para transformar tu vida desde adentro.</p>
          <span class="pillar-link">
            Explorar
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </span>
        </router-link>

        <router-link to="/consultas" class="pillar-card">
          <div class="pillar-icon icon-purple">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <h3>Consultas</h3>
          <p>Acompañamiento personalizado 1:1 con Irina y su equipo de expertos.</p>
          <span class="pillar-link">
            Explorar
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </span>
        </router-link>

        <router-link to="/tienda" class="pillar-card">
          <div class="pillar-icon icon-gold">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
          </div>
          <h3>Libros y herramientas</h3>
          <p>Lecturas, guías y tarjetas de reflexión que inspiran y transforman.</p>
          <span class="pillar-link">
            Explorar
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </span>
        </router-link>

        <router-link to="/comunidad" class="pillar-card">
          <div class="pillar-icon icon-green">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <h3>Comunidad</h3>
          <p>Un espacio para crecer, conectar y evolucionar junto a personas como tú.</p>
          <span class="pillar-link">
            Explorar
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </span>
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.msec-pad {
  padding: 88px 32px;
}

.pillars {
  background: #f5eee3;
}

.container {
  max-width: 1280px;
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
  margin: 0 0 52px;
  letter-spacing: 0;
  line-height: 1.12;
}

.highlight {
  color: #8e1519;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  text-align: left;
}

.pillar-card {
  text-decoration: none;
  background: #ffffff;
  border-radius: 20px;
  padding: 34px 30px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 18px 40px -28px rgba(0,0,0,0.25);
  transition: transform 0.2s, box-shadow 0.2s;
}

.pillar-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 48px -28px rgba(0,0,0,0.35);
}

.pillar-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 22px;
}

.icon-red {
  background: #f1e3de;
  color: #8e1519;
}

.icon-purple {
  background: #f1e7f7;
  color: #8b5cc7;
}

.icon-gold {
  background: #f6edd9;
  color: #c49a3f;
}

.icon-green {
  background: #e3f1e8;
  color: #3f9d5f;
}

.pillar-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 12px;
}

.pillar-card p {
  font-size: 16px;
  line-height: 1.55;
  color: #6b6259;
  margin: 0 0 22px;
  flex: 1;
}

.pillar-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #8e1519;
  font-weight: 500;
  font-size: 16px;
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