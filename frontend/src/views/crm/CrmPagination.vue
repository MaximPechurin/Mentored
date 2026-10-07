<template>
  <div class="crm-pagination" v-if="pages > 1 || pageSizeSelector">
    <div class="crm-page-size">
      <label>Por página:</label>
      <select :value="pageSize" @change="onPageSizeChange($event.target.value)">
        <option :value="20">20</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>
    </div>

    <div class="crm-page-nav" v-if="pages > 1">
      <button
        class="crm-page-btn"
        :disabled="page <= 1"
        @click="$emit('change', page - 1)"
      >
        ← Anterior
      </button>

      <div class="crm-page-numbers">
        <template v-for="p in visiblePages" :key="p">
          <span v-if="p === '...'" class="crm-page-ellipsis">...</span>
          <button
            v-else
            class="crm-page-num"
            :class="{ active: p === page }"
            @click="$emit('change', p)"
          >
            {{ p }}
          </button>
        </template>
      </div>

      <button
        class="crm-page-btn"
        :disabled="page >= pages"
        @click="$emit('change', page + 1)"
      >
        Siguiente →
      </button>
    </div>

    <div class="crm-page-info">
      Página {{ page }} de {{ pages }} · {{ count }} registros
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  pages: { type: Number, required: true },
  count: { type: Number, required: true },
  pageSize: { type: Number, default: 20 },
})

const emit = defineEmits(['change', 'update:pageSize'])

const pageSizeSelector = true

const visiblePages = computed(() => {
  const total = props.pages
  const current = props.page
  const delta = 2

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages = []
  const left = Math.max(2, current - delta)
  const right = Math.min(total - 1, current + delta)

  pages.push(1)
  if (left > 2) pages.push('...')
  for (let i = left; i <= right; i++) pages.push(i)
  if (right < total - 1) pages.push('...')
  pages.push(total)

  return pages
})

const onPageSizeChange = (value) => {
  emit('update:pageSize', Number(value))
}
</script>

<style scoped>
.crm-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 12px;
  padding: 14px 20px;
  margin-top: 16px;
  font-size: 14px;
  color: #5d544c;
}

.crm-page-size {
  display: flex;
  align-items: center;
  gap: 8px;
}

.crm-page-size select {
  border: 1px solid #ece7e1;
  border-radius: 8px;
  padding: 6px 10px;
  font-family: inherit;
  font-size: 14px;
  color: #15110f;
  background: #faf6f0;
  cursor: pointer;
}

.crm-page-nav {
  display: flex;
  align-items: center;
  gap: 10px;
}

.crm-page-btn {
  border: 1px solid #ece7e1;
  background: #ffffff;
  color: #5d544c;
  font-family: inherit;
  font-size: 14px;
  padding: 7px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.crm-page-btn:hover:not(:disabled) {
  border-color: #8e1519;
  color: #8e1519;
}

.crm-page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.crm-page-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
}

.crm-page-num {
  border: 1px solid transparent;
  background: transparent;
  color: #5d544c;
  font-family: inherit;
  font-size: 14px;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.crm-page-num:hover {
  background: #faf6f0;
}

.crm-page-num.active {
  background: #0e0c0c;
  color: #ffffff;
  font-weight: 600;
}

.crm-page-ellipsis {
  color: #a59c93;
  padding: 0 4px;
}

.crm-page-info {
  color: #8a8079;
  font-size: 13px;
}

@media (max-width: 700px) {
  .crm-pagination {
    flex-direction: column;
    align-items: stretch;
  }

  .crm-page-nav {
    justify-content: center;
  }
}
</style>