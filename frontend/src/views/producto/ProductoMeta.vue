<template>
  <div class="pd-meta" v-if="product && product.meta && product.meta.length">
    <div v-for="item in product.meta" :key="item.label" class="pd-meta-item">
      <span class="pd-meta-label">{{ item.label }}</span>
      <span class="pd-meta-value">{{ item.value }}</span>
    </div>
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
.pd-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px 40px;
  padding: 4px 4px 0;
}

.pd-meta-item {
  flex: 1 0 auto;
}

.pd-meta-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #a59c93;
  margin-bottom: 5px;
}

.pd-meta-value {
  font-size: 16px;
  color: #15110f;
  font-weight: 400;
}
</style>