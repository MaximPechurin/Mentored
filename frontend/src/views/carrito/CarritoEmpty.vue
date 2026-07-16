<template>
  <section class="cr-empty">
    <div class="cr-empty-container">
      <div class="cr-empty-icon">
        <svg width="92" height="92" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <path d="M16 10a4 4 0 0 1-8 0"/>
        </svg>
      </div>
      <h2 class="cr-empty-title">Tu carrito está vacío</h2>
      <p class="cr-empty-text">Explora nuestros productos y encuentra tu camino.</p>
      <router-link to="/tienda" class="cr-empty-btn">
        Ver tienda
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"/>
          <polyline points="12 5 19 12 12 19"/>
        </svg>
      </router-link>
    </div>
  </section>
</template>

<style scoped>
.cr-empty {
  padding: 96px 32px;
}

.cr-empty-container {
  max-width: 560px;
  margin: 0 auto;
  text-align: center;
}

.cr-empty-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 28px;
  color: #cdc4b8;
}

.cr-empty-title {
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 14px;
}

.cr-empty-text {
  font-size: 19px;
  color: #8a8079;
  margin: 0 0 36px;
}

.cr-empty-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 17px;
  padding: 16px 32px;
  border-radius: 12px;
}

@media (max-width: 860px) {
  .cr-empty { padding: 64px 20px !important; }
}
</style>