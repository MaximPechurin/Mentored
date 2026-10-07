<template>
  <div class="crm-card">
    <div class="crm-card-head">
      <h2>Últimos registros</h2>
    </div>
    <div v-if="registrations.length === 0" class="crm-empty">
      Sin registros recientes.
    </div>
    <table v-else class="crm-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Email</th>
          <th class="right">Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in registrations" :key="u.id">
          <td>
            {{ u.username }}
            <span v-if="u.roles && u.roles.length" class="crm-role">
              {{ u.roles.join(', ') }}
            </span>
          </td>
          <td class="muted">{{ u.email }}</td>
          <td class="right muted">{{ formatDate(u.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  registrations: { type: Array, required: true },
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
/* Те же стили, что в CrmRecentPayments — можно вынести в общий css,
   но для скорости дублирую, чтобы файлы были независимы. */
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

.crm-role {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #8e1519;
  background: #faf6f0;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
}

.crm-empty {
  color: #a59c93;
  font-size: 15px;
  padding: 20px 0;
  text-align: center;
}
</style>