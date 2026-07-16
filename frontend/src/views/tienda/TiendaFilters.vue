<template>
  <div class="t-filters-wrapper">
    <div class="t-filters">
      <button
        v-for="filter in filters"
        :key="filter.key"
        class="t-filter-btn"
        :class="{ active: modelValue === filter.key }"
        @click="$emit('update:modelValue', filter.key)"
      >
        {{ filter.label }}
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

const filters = [
  { label: 'Todos', key: 'todos' },
  { label: 'Libros', key: 'libros' },
  { label: 'Cursos', key: 'cursos' },
  { label: 'Consultas', key: 'consultas' },
  { label: 'Comunidad', key: 'comunidad' }
]
</script>

<style scoped>
.t-filters-wrapper {
  background: #f5eee3;
  padding: 0 32px;
}

.t-filters {
  max-width: 1320px;
  margin: 0 auto;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  padding: 16px 0 0;
}

.t-filter-btn {
  font-family: inherit;
  font-size: 16px;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 999px;
  white-space: nowrap;
  cursor: pointer;
  border: 1px solid #e4d8c8;
  background: #ffffff;
  color: #3a332e;
  transition: all 0.3s;
}

.t-filter-btn:hover {
  background: #f0e8dc;
}

.t-filter-btn.active {
  background: #8e1519;
  color: #fff;
  border-color: #8e1519;
}

@media (max-width: 860px) {
  .t-filters-wrapper { padding: 0 20px; }
}
</style>
