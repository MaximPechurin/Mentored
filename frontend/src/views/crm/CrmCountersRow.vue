<template>
  <div class="crm-counters">
    <router-link
      v-for="c in items"
      :key="c.key"
      :to="c.to"
      class="crm-counter"
      :class="{ 'crm-counter--accent': c.accent }"
    >
      <div class="crm-counter-label">{{ c.label }}</div>
      <div class="crm-counter-value">{{ c.value }}</div>
      <div v-if="c.sub" class="crm-counter-sub">{{ c.sub }}</div>
      <span class="crm-counter-arrow">→</span>
    </router-link>
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
    to: { name: 'CrmStudents', query: { access: 'active' } },
  },
  {
    key: 'courses_active',
    label: 'Cursos activos',
    value: props.counters.courses_active,
    to: { name: 'CrmCourses', query: { status: 'active' } },
  },
  {
    key: 'teachers',
    label: 'Profesores',
    value: props.counters.teachers,
    to: { name: 'CrmTeachers' },
  },
  {
    key: 'orders_paid_30d',
    label: 'Pagos (30 días)',
    value: props.counters.orders_paid_30d,
    to: { name: 'CrmOrders', query: { status: 'paid' } },
  },
  {
    key: 'revenue_usd_30d',
    label: 'Ventas (30 días)',
    value: `$${props.counters.revenue_usd_30d}`,
    accent: true,
    to: { name: 'CrmOrders', query: { status: 'paid' } },
  },
  {
    key: 'submissions_pending',
    label: 'Tareas por revisar',
    value: props.counters.submissions_pending,
    to: { name: 'CrmSubmissions', query: { status: 'submitted' } },
  },
  {
    key: 'contact_messages_unread',
    label: 'Mensajes sin leer',
    value: props.counters.contact_messages_unread,
    to: { name: 'CrmContactMessages', query: { is_read: 'false' } },
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
  position: relative;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  cursor: pointer;
}

.crm-counter:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px -18px rgba(0,0,0,0.25);
  border-color: #d9cfc0;
}

.crm-counter--accent {
  background: #0e0c0c;
  border-color: #0e0c0c;
  color: #ffffff;
}

.crm-counter--accent:hover {
  border-color: #c49a3f;
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

.crm-counter-arrow {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 16px;
  color: #c9bca6;
  opacity: 0;
  transition: opacity 0.2s, transform 0.2s;
}

.crm-counter:hover .crm-counter-arrow {
  opacity: 1;
  transform: translateX(2px);
}

.crm-counter--accent .crm-counter-arrow {
  color: #c49a3f;
}
</style>