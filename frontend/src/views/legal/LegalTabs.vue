<template>
  <div class="lg-tabs-wrapper">
    <div class="lg-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="lg-tab"
        :class="{ active: modelValue === tab.key }"
        @click="$emit('update:modelValue', tab.key)"
      >
        {{ tab.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'info'
  }
})

defineEmits(['update:modelValue'])

const tabs = [
  { key: 'info', label: 'Aviso legal' },
  { key: 'oferta', label: 'Oferta pública' },
  { key: 'privacidad', label: 'Política de privacidad' }
]
</script>

<style scoped>
.lg-tabs-wrapper {
  position: sticky;
  top: 84px;
  z-index: 20;
  background: #ffffff;
  border-bottom: 1px solid #ececec;
}

.lg-tabs {
  max-width: 920px;
  margin: 0 auto;
  display: flex;
  gap: 4px;
}

.lg-tab {
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 16px;
  padding: 20px 18px;
  border-bottom: 2px solid transparent;
  letter-spacing: -0.1px;
  color: #8a8079;
  font-weight: 500;
  transition: color 0.3s, border-color 0.3s;
}

.lg-tab:hover {
  color: #1c1c1c;
}

.lg-tab.active {
  color: #8e1519;
  font-weight: 600;
  border-bottom-color: #8e1519;
}

@media (max-width: 860px) {
  .lg-tabs-wrapper { padding: 0 20px !important; }
  .lg-tabs { gap: 6px !important; overflow-x: auto; }
  .lg-tab { font-size: 14px !important; padding: 16px 14px !important; white-space: nowrap; }
}
</style>