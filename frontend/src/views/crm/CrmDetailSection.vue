<template>
  <section class="crm-section">
    <header class="crm-section-head">
      <h2 class="crm-section-title">{{ title }}</h2>
      <span v-if="count !== null" class="crm-section-count">{{ count }}</span>
      <slot name="actions"></slot>
    </header>
    <div class="crm-section-body">
      <slot></slot>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  count: { type: [Number, String], default: null },
})
</script>

<style scoped>
.crm-section {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  margin-bottom: 20px;
  overflow: hidden;
}

.crm-section-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 24px;
  border-bottom: 1px solid #f5f0e8;
}

.crm-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
}

.crm-section-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 22px;
  padding: 0 8px;
  background: #faf6f0;
  color: #8e1519;
  font-size: 12.5px;
  font-weight: 700;
  border-radius: 999px;
}

.crm-section-body {
  padding: 0;
}
</style>