<template>
  <div v-if="product" class="pd-breadcrumb">
    <div class="pd-breadcrumb-inner">
      <router-link to="/tienda" class="pd-breadcrumb-link">Tienda</router-link>
      <span class="pd-breadcrumb-sep">/</span>
      <span class="pd-breadcrumb-category">{{ product.category }}</span>
      <span class="pd-breadcrumb-sep">/</span>
      <span class="pd-breadcrumb-current">{{ product.title }}</span>
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
.pd-breadcrumb {
  background: #f5eee3;
  border-bottom: 1px solid #e6dccb;
}

.pd-breadcrumb-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 32px;
  font-size: 14.5px;
  color: #8a8079;
}

.pd-breadcrumb-link {
  color: #8a8079;
  text-decoration: none;
}

.pd-breadcrumb-link:hover {
  color: #8e1519;
}

.pd-breadcrumb-sep {
  margin: 0 8px;
  color: #c9bca6;
}

.pd-breadcrumb-category {
  color: #5d544c;
}

.pd-breadcrumb-current {
  color: #15110f;
}

@media (max-width: 920px) {
  .pd-breadcrumb-inner {
    padding: 18px 20px;
    font-size: 13px;
  }
}
</style>