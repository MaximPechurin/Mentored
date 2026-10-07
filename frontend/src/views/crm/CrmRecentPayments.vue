<template>
  <div class="crm-card">
    <div class="crm-card-head">
      <h2>Últimos pagos</h2>
    </div>
    <div v-if="payments.length === 0" class="crm-empty">
      Sin pagos recientes.
    </div>
    <table v-else class="crm-table">
      <thead>
        <tr>
          <th>Pedido</th>
          <th>Cliente</th>
          <th class="right">Monto</th>
          <th class="right">Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in payments" :key="p.id">
          <td class="mono">{{ p.order_number }}</td>
          <td>{{ p.user_name }}</td>
          <td class="right">${{ p.amount }}</td>
          <td class="right muted">{{ formatDate(p.paid_at || p.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  payments: { type: Array, required: true },
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

.crm-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14.5px;
}

.crm-table th {
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
  padding: 8px 4px;
  border-bottom: 1px solid #ece7e1;
}

.crm-table td {
  padding: 12px 4px;
  border-bottom: 1px solid #f5f0e8;
  color: #3a342e;
}

.crm-table tr:last-child td {
  border-bottom: none;
}

.crm-table .right { text-align: right; }
.crm-table .muted { color: #a59c93; font-size: 13.5px; }
.crm-table .mono {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 13px;
  color: #8e1519;
}

.crm-empty {
  color: #a59c93;
  font-size: 15px;
  padding: 20px 0;
  text-align: center;
}
</style>