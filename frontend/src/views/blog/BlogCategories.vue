<template>
  <div class="bl-categories">
    <div class="bl-cats-inner">
      <button
        v-for="cat in categories"
        :key="cat.key"
        class="bl-cat-btn"
        :class="{ active: modelValue === cat.key }"
        @click="$emit('update:modelValue', cat.key)"
      >
        {{ cat.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'todos'
  }
})

defineEmits(['update:modelValue'])

const categories = [
  { key: 'todos', label: 'Todos' },
  { key: 'energia', label: 'Energía' },
  { key: 'habitos', label: 'Hábitos' },
  { key: 'proposito', label: 'Propósito' },
  { key: 'carrera', label: 'Carrera' }
]
</script>

<style scoped>
.bl-categories {
  position: sticky;
  top: 84px;
  z-index: 20;
  background: #ffffff;
  border-bottom: 1px solid #ececec;
}

.bl-cats-inner {
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  gap: 4px;
  padding: 0 32px;
}

.bl-cat-btn {
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 16px;
  padding: 20px 18px;
  border-bottom: 2px solid transparent;
  letter-spacing: -0.1px;
  white-space: nowrap;
  color: #8a8079;
  font-weight: 500;
  transition: color 0.3s, border-color 0.3s;
}

.bl-cat-btn:hover {
  color: #1c1c1c;
}

.bl-cat-btn.active {
  color: #8e1519;
  font-weight: 600;
  border-bottom-color: #8e1519;
}

@media (max-width: 900px) {
  .bl-cats-inner { padding: 0 20px !important; overflow-x: auto; }
}
</style>