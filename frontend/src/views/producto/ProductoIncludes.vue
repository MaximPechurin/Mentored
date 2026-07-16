<template>
  <div class="pd-includes" v-if="product && product.includes && product.includes.length">
    <h3 class="pd-includes-title">Qué incluye</h3>
    <ul class="pd-includes-list">
      <li v-for="item in product.includes" :key="item" class="pd-includes-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#8e1519" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        {{ item }}
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    default: null,
  },
})
</script>

<style scoped>
.pd-includes {
  background: #ffffff;
  border-radius: 18px;
  padding: 26px 28px;
  box-shadow: 0 18px 44px -34px rgba(0,0,0,0.4);
  margin-bottom: 24px;
}

.pd-includes-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 16px;
}

.pd-includes-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 13px;
}

.pd-includes-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 16px;
  line-height: 1.5;
  color: #3a342e;
}

.pd-includes-item svg {
  flex-shrink: 0;
  margin-top: 1px;
}
</style>