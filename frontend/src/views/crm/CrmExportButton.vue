<template>
  <button
    class="crm-export-btn"
    :disabled="loading"
    @click="handleExport"
  >
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
      <polyline points="7 10 12 15 17 10"/>
      <line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
    {{ loading ? 'Exportando…' : 'Exportar XLSX' }}
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { crmApi } from '../../api/crm'

const props = defineProps({
  url: { type: String, required: true },
  params: { type: Object, default: () => ({}) },
})

const loading = ref(false)

const handleExport = async () => {
  loading.value = true
  try {
    await crmApi.downloadExport(props.url, props.params)
  } catch (e) {
    console.error('Export error:', e)
    alert('No se pudo generar el archivo. Inténtalo de nuevo.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.crm-export-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #0e0c0c;
  color: #ffffff;
  border: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.crm-export-btn:hover:not(:disabled) {
  background: #2a1a1a;
}

.crm-export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>