<template>
  <section class="hero">
    <div class="hero-img">
      <img src="/images/hero.png" alt="Irina Karbonova — Fundadora de Mentored">
      <div class="hero-grad"></div>
    </div>
    <div class="hero-inner">
      <div class="hero-content">
        <span class="hero-tag">{{ t('hero.tag') }}</span>
        <h1 class="hero-h1">
          {{ t('hero.title.part1') }}
          <span class="highlight-red">{{ t('hero.title.part2') }}</span>,
          <span class="highlight-gold">{{ t('hero.title.part3') }}</span>
          {{ t('hero.title.part4') }}
        </h1>
        <p class="hero-sub">
          {{ t('hero.sub') }}
        </p>
        <p class="hero-quote">
          {{ t('hero.quote') }}
        </p>
        <div class="hero-buttons">
          <router-link to="/tienda" class="btn-primary">
            {{ t('hero.btnPrimary') }}
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </router-link>
          <a href="#" class="btn-secondary">{{ t('hero.btnSecondary') }}</a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useLanguage } from '../../composables/useLanguage.js'

const { t } = useLanguage()
</script>

<style scoped>
.hero {
  position: relative;
  background: #0e0c0c;
  overflow: hidden;
}

.hero-img {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 62%;
}

.hero-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  display: block;
}

.hero-grad {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #0e0c0c 0%, rgba(14,12,12,0.72) 13%, rgba(14,12,12,0) 36%);
}

.hero-inner {
  position: relative;
  max-width: 1480px;
  margin: 0 auto;
  padding: 84px 32px;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-content {
  max-width: 560px;
}

.hero-tag {
  display: inline-block;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 22px;
}

.hero-h1 {
  font-family: 'Playfair Display', serif;
  font-size: 44px;
  line-height: 1.16;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 22px;
  letter-spacing: -0.3px;
  text-shadow: 0 2px 24px rgba(0,0,0,0.5);
}

.highlight-red { color: #8e1519; }
.highlight-gold { color: #c49a3f; }

.hero-sub {
  font-size: 19px;
  font-weight: 300;
  line-height: 1.6;
  color: #cfc7be;
  margin: 0 0 22px;
  max-width: 430px;
  text-shadow: 0 2px 16px rgba(0,0,0,0.5);
}

.hero-quote {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 19px;
  line-height: 1.5;
  color: #9a9088;
  margin: 0 0 36px;
  max-width: 440px;
}

.hero-buttons {
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
  text-decoration: none;
  background: transparent;
  border: 1.5px solid rgba(255,255,255,0.5);
  color: #fff;
  font-weight: 500;
  font-size: 17px;
  padding: 16px 30px;
  border-radius: 999px;
}

@media (max-width: 860px) {
  .hero-img { width: 100% !important; }
  .hero-grad { background: linear-gradient(180deg, rgba(14,12,12,0.4) 0%, rgba(14,12,12,0.8) 52%, #0e0c0c 100%) !important; }
  .hero-inner { padding: 60px 20px !important; min-height: 0 !important; }
  .hero-h1 { font-size: 33px !important; }
  .hero-sub { font-size: 17px !important; }
}
</style>