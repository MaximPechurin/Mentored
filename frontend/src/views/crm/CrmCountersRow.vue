<template>
  <div class="crm-counters">
    <div
      v-for="c in items"
      :key="c.key"
      class="crm-counter"
      :class="{ 'crm-counter--accent': c.accent }"
    >
      <div class="crm-counter-label">{{ c.label }}</div>
      <div class="crm-counter-value">{{ c.value }}</div>
      <div v-if="c.sub" class="crm-counter-sub">{{ c.sub }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  counters: { type: Object, required: true },
})

const items = computed(() => [
  {
    key: 'students_active',
    label: 'Alumnos activos',
    value: props.counters.students_active,
    sub: `de ${props.counters.students_total} registrados`,
  },
  {
    key: 'courses_active',
    label: 'Cursos activos',
    value: props.counters.courses_active,
  },
  {
    key: 'teachers',
    label: 'Profesores',
    value: props.counters.teachers,
  },
  {
    key: 'orders_paid_30d',
    label: 'Pagos (30 días)',
    value: props.counters.orders_paid_30d,
  },
  {
    key: 'revenue_usd_30d',
    label: 'Ventas (30 días)',
    value: `$${props.counters.revenue_usd_30d}`,
    accent: true,
  },
  {
    key: 'submissions_pending',
    label: 'Tareas por revisar',
    value: props.counters.submissions_pending,
  },
  {
    key: 'contact_messages_unread',
    label: 'Mensajes sin leer',
    value: props.counters.contact_messages_unread,
  },
])
</script>

<style scoped>
.crm-counters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.crm-counter {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.crm-counter--accent {
  background: #0e0c0c;
  border-color: #0e0c0c;
  color: #ffffff;
}

.crm-counter-label {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
}

.crm-counter--accent .crm-counter-label {
  color: #c49a3f;
}

.crm-counter-value {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  color: #15110f;
  line-height: 1.1;
}

.crm-counter--accent .crm-counter-value {
  color: #ffffff;
}

.crm-counter-sub {
  font-size: 13px;
  color: #a59c93;
}
</style>