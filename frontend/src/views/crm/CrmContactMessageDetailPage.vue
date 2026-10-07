<template>
  <div class="crm-message">
    <div v-if="loading" class="crm-loading">
      <div class="crm-loading-spinner"></div>
      <p>Cargando mensaje...</p>
    </div>

    <div v-else-if="error" class="crm-error">
      <h2>Error</h2>
      <p>{{ error }}</p>
      <router-link :to="{ name: 'CrmContactMessages' }" class="crm-btn crm-btn-outline">
        ← Volver a la lista
      </router-link>
    </div>

    <template v-else-if="message">
      <nav class="crm-breadcrumb">
        <router-link :to="{ name: 'CrmContactMessages' }">Mensajes</router-link>
        <span class="crm-breadcrumb-sep">/</span>
        <span class="crm-breadcrumb-current">{{ message.name }}</span>
      </nav>

      <header class="crm-header-card">
        <div>
          <h1 class="crm-header-name">{{ message.name }}</h1>
          <div class="crm-header-meta">
            <a :href="`mailto:${message.email}`" class="crm-meta-item">
              ✉ {{ message.email }}
            </a>
            <span class="crm-meta-item">📅 {{ formatDateTime(message.created_at) }}</span>
            <span class="motivo-tag">{{ message.motivo }}</span>
            <span class="badge" :class="message.is_read ? 'badge-muted' : 'badge-danger'">
              {{ message.is_read ? 'Leído' : 'Nuevo' }}
            </span>
          </div>
        </div>
        <div class="crm-header-actions">
          <button
            v-if="!message.is_read"
            class="crm-btn crm-btn-outline"
            @click="markRead"
          >
            Marcar como leído
          </button>
          <a :href="`mailto:${message.email}?subject=Re: ${message.motivo}`" class="crm-btn crm-btn-outline">
            ✉ Responder
          </a>
          <button class="crm-btn crm-btn-danger" @click="deleteMessage">
            Eliminar
          </button>
        </div>
      </header>

      <CrmDetailSection title="Mensaje">
        <div class="crm-message-body">{{ message.message }}</div>
      </CrmDetailSection>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { crmApi } from '../../api/crm'
import CrmDetailSection from './CrmDetailSection.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const message = ref(null)

const loadMessage = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await crmApi.getContactMessage(route.params.id)
    message.value = res.data
  } catch (e) {
    console.error('Error loading message:', e)
    error.value = e.response?.data?.detail || 'No se pudo cargar el mensaje.'
  } finally {
    loading.value = false
  }
}

const markRead = async () => {
  try {
    await crmApi.updateContactMessage(message.value.id, { is_read: true })
    message.value.is_read = true
  } catch (e) {
    console.error('Error marking read:', e)
  }
}

const deleteMessage = async () => {
  if (!confirm('¿Eliminar este mensaje?')) return
  try {
    await crmApi.deleteContactMessage(message.value.id)
    router.push({ name: 'CrmContactMessages' })
  } catch (e) {
    console.error('Error deleting:', e)
    alert('No se pudo eliminar el mensaje')
  }
}

const formatDateTime = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

onMounted(loadMessage)
</script>

<style scoped>
.crm-loading,
.crm-error {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; min-height: 300px;
  color: #8a8079; text-align: center;
}
.crm-loading-spinner {
  width: 48px; height: 48px;
  border: 4px solid #e4ddd2; border-top: 4px solid #8e1519;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.crm-error h2 { font-family: 'Playfair Display', serif; color: #15110f; }

.crm-breadcrumb { font-size: 14px; color: #8a8079; margin-bottom: 12px; }
.crm-breadcrumb a { color: #8e1519; text-decoration: none; }
.crm-breadcrumb-sep { margin: 0 8px; color: #c9bca6; }
.crm-breadcrumb-current { color: #15110f; }

.crm-header-card {
  display: flex; justify-content: space-between; gap: 24px; flex-wrap: wrap;
  background: #fff; border: 1px solid #ece7e1; border-radius: 16px;
  padding: 24px; margin-bottom: 20px;
}
.crm-header-name {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600; color: #15110f; margin: 0 0 12px;
}
.crm-header-meta {
  display: flex; gap: 14px; flex-wrap: wrap;
  font-size: 14px; color: #6f655c; align-items: center;
}
.crm-meta-item { color: #6f655c; text-decoration: none; }
a.crm-meta-item:hover { color: #8e1519; }
.crm-header-actions { display: flex; gap: 10px; flex-wrap: wrap; }

.crm-btn {
  display: inline-flex; align-items: center; gap: 6px;
  text-decoration: none; font-family: inherit; font-size: 14px;
  font-weight: 600; padding: 9px 16px; border-radius: 999px;
  cursor: pointer; transition: all 0.2s;
  border: 1.5px solid transparent;
}
.crm-btn-outline {
  background: #fff; border-color: #ece7e1; color: #5d544c;
}
.crm-btn-outline:hover { border-color: #8e1519; color: #8e1519; }
.crm-btn-danger {
  background: #8e1519; border-color: #8e1519; color: #fff;
}
.crm-btn-danger:hover { background: #a01a1f; border-color: #a01a1f; }

.crm-message-body {
  padding: 24px;
  font-size: 15.5px; line-height: 1.7;
  color: #3a342e;
  white-space: pre-line;
}

.motivo-tag {
  font-size: 11.5px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.5px; color: #8e1519;
  background: #faf6f0; padding: 3px 10px; border-radius: 999px;
}
.badge {
  display: inline-block; font-size: 11.5px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  padding: 4px 10px; border-radius: 999px;
}
.badge-danger { background: #fbeaea; color: #8e1519; }
.badge-muted { background: #f0ede8; color: #8a8079; }
</style>