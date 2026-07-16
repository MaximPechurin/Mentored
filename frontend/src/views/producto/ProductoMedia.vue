<template>
  <div v-if="product" class="pd-media">
    <div class="pd-media-image">
      <img :src="product.img" :alt="product.title">
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
.pd-media {
  position: sticky;
  top: 104px;
  max-width: 100%; /* 👈 НЕ ДАЁТ РАСТЯНУТЬСЯ */
}

.pd-media-image {
  background: #1a1212;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 30px 64px -36px rgba(0,0,0,0.5);
  aspect-ratio: 545/420; /* 👈 СООТНОШЕНИЕ СТОРОН КАК В ЭТАЛОНЕ */
  max-width: 100%;
}

.pd-media-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

@media (max-width: 920px) {
  .pd-media {
    position: static !important;
  }
}
</style>