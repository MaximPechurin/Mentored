<template>
  <section class="pd-description">
    <div class="pd-description-inner">
      <span class="pd-description-tag">Sobre este {{ product.kindWord }}</span>
      <h2 class="pd-description-title">{{ product.descHeading }}</h2>
      <p v-for="(para, index) in product.longDesc" :key="index" class="pd-description-text">
        {{ para }}
      </p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.pd-description {
  background: #ffffff;
}

.pd-description-inner {
  max-width: 780px;
  margin: 0 auto;
  padding: 80px 32px 96px;
}

.pd-description-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #8e1519;
  margin-bottom: 14px;
}

.pd-description-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.pd-description-text {
  font-size: 18px;
  line-height: 1.75;
  color: #5d544c;
  margin: 0 0 22px;
}

.pd-description-text:last-child {
  margin-bottom: 0;
}

@media (max-width: 920px) {
  .pd-description-inner {
    padding: 0 20px 88px !important;
  }
}
</style>