<template>
  <div class="crm-dashboard">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando panel...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error al cargar el panel</h2>
      <p>{{ error }}</p>
      <button @click="loadDashboard">Reintentar</button>
    </div>

    <div v-else>
      <CrmCountersRow :counters="data.counters" />

      <div class="crm-grid-2">
        <CrmRecentPayments :payments="data.recent_payments" />
        <CrmRecentRegistrations :registrations="data.recent_registrations" />
      </div>

      <CrmRecentMessages :messages="data.recent_contact_messages" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { crmApi } from '../../api/crm'
import CrmCountersRow from './components/CrmCountersRow.vue'
import CrmRecentPayments from './components/CrmRecentPayments.vue'
import CrmRecentRegistrations from './components/CrmRecentRegistrations.vue'
import CrmRecentMessages from './components/CrmRecentMessages.vue'

const loading = ref(true)
const error = ref(null)
const data = ref(null)

const loadDashboard = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getDashboard()
    data.value = res.data
  } catch (e) {
    console.error('CRM dashboard error:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar la información.'
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<style scoped>
.crm-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin: 24px 0;
}

.crm-loading,
.crm-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: #8a8079;
  text-align: center;
}

.crm-loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e4ddd2;
  border-top: 4px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.crm-error h2 {
  font-family: 'Playfair Display', serif;
  color: #15110f;
  margin-bottom: 12px;
}

.crm-error button {
  margin-top: 16px;
  background: #8e1519;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 999px;
  cursor: pointer;
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
}

@media (max-width: 900px) {
  .crm-grid-2 { grid-template-columns: 1fr; }
}
</style>