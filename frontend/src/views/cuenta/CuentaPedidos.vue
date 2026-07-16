<template>
  <div>
    <h2 class="ac-section-title">Mis pedidos</h2>
    <div class="ac-orders">
      <div v-for="order in orders" :key="order.id" class="ac-order">
        <div>
          <div class="ac-order-header">
            <span class="ac-order-id">{{ order.id }}</span>
            <span class="ac-order-status" :style="order.badgeStyle">{{ order.status }}</span>
          </div>
          <div class="ac-order-title">{{ order.title }}</div>
          <div class="ac-order-date">{{ order.date }}</div>
        </div>
        <div class="ac-order-total">{{ order.total }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const orders = [
  {
    id: '#MEN-1047',
    title: 'Curso: Recupera tu Energía',
    date: '12 de mayo de 2026',
    total: '$97.00',
    status: 'Completado',
    badgeStyle: 'display:inline-block;font-size:12px;font-weight:600;letter-spacing:0.4px;padding:3px 10px;border-radius:999px;color:#1f7a44;background:#e7f4ec;'
  },
  {
    id: '#MEN-1031',
    title: 'Consulta 1:1 con Irina Karbonova',
    date: '28 de abril de 2026',
    total: '$120.00',
    status: 'Programado',
    badgeStyle: 'display:inline-block;font-size:12px;font-weight:600;letter-spacing:0.4px;padding:3px 10px;border-radius:999px;color:#8a5a00;background:#fbf0d9;'
  },
  {
    id: '#MEN-0998',
    title: 'Membresía Comunidad — Premium',
    date: '1 de abril de 2026',
    total: '$49.00',
    status: 'Activo',
    badgeStyle: 'display:inline-block;font-size:12px;font-weight:600;letter-spacing:0.4px;padding:3px 10px;border-radius:999px;color:#8e1519;background:#f7e3e3;'
  }
]
</script>

<style scoped>
.ac-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.ac-orders {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ac-order {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 24px 26px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.ac-order-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}

.ac-order-id {
  font-size: 14px;
  font-weight: 600;
  color: #15110f;
}

.ac-order-status {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.4px;
  padding: 3px 10px;
  border-radius: 999px;
}

.ac-order-title {
  font-size: 16px;
  color: #15110f;
  font-weight: 400;
  margin-bottom: 3px;
}

.ac-order-date {
  font-size: 14px;
  color: #a59c93;
}

.ac-order-total {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #15110f;
  text-align: right;
}

@media (max-width: 920px) {
  .ac-order { flex-wrap: wrap !important; }
}
</style>