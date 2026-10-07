<template>
  <div class="crm-card">
    <div class="crm-card-head">
      <h2>Solicitudes de contacto</h2>
    </div>
    <div v-if="messages.length === 0" class="crm-empty">
      Sin mensajes recientes.
    </div>
    <ul v-else class="crm-msg-list">
      <li v-for="m in messages" :key="m.id" class="crm-msg">
        <div class="crm-msg-head">
          <span class="crm-msg-name">{{ m.name }}</span>
          <span class="crm-msg-motivo">{{ m.motivo }}</span>
          <span class="crm-msg-date">{{ formatDate(m.created_at) }}</span>
        </div>
        <p class="crm-msg-text">{{ m.message_preview }}</p>
        <div class="crm-msg-email">{{ m.email }}</div>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  messages: { type: Array, required: true },
})

const formatDate = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-ES', {
    day: '2-digit', month: '2-digit', year: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}
</script>

<style scoped>
.crm-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 24px;
}

.crm-card-head {
  margin-bottom: 16px;
}

.crm-card-head h2 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
}

.crm-msg-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.crm-msg {
  padding: 14px 16px;
  background: #faf6f0;
  border-radius: 12px;
}

.crm-msg-head {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.crm-msg-name {
  font-weight: 600;
  color: #15110f;
  font-size: 15px;
}

.crm-msg-motivo {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8e1519;
  background: #ffffff;
  padding: 2px 8px;
  border-radius: 999px;
}

.crm-msg-date {
  margin-left: auto;
  font-size: 13px;
  color: #a59c93;
}

.crm-msg-text {
  font-size: 14.5px;
  line-height: 1.5;
  color: #5d544c;
  margin: 0 0 6px;
}

.crm-msg-email {
  font-size: 13px;
  color: #8a8079;
}

.crm-empty {
  color: #a59c93;
  font-size: 15px;
  padding: 20px 0;
  text-align: center;
}
</style>