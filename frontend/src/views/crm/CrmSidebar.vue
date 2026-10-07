<template>
  <aside class="crm-sidebar">
    <nav class="crm-nav">
      <router-link
        v-for="item in items"
        :key="item.name"
        :to="{ name: item.name }"
        class="crm-nav-link"
        :class="{ active: isActive(item) }"
      >
        <span class="crm-nav-icon" v-html="item.icon"></span>
        <span class="crm-nav-label">{{ item.label }}</span>
        <span v-if="item.badge" class="crm-nav-badge">{{ item.badge }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Иконки — простые SVG, 18×18, stroke currentColor
const items = [
  {
    name: 'CrmDashboard',
    label: 'Panel',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>`,
  },
  {
    name: 'CrmStudents',
    label: 'Alumnos',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  },
  {
    name: 'CrmCourses',
    label: 'Cursos',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m2 7 10-5 10 5-10 5z"/><path d="M6 9.5V15c0 1.5 2.7 3 6 3s6-1.5 6-3V9.5"/></svg>`,
  },
  {
    name: 'CrmTeachers',
    label: 'Profesores',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  },
  {
    name: 'CrmOrders',
    label: 'Pedidos',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>`,
  },
  {
    name: 'CrmPayments',
    label: 'Pagos',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>`,
  },
  {
    name: 'CrmContactMessages',
    label: 'Mensajes',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
  },
  {
    name: 'CrmSubmissions',
    label: 'Tareas',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>`,
  },
]

const isActive = (item) => {
  const current = route.name
  // Активный = сам пункт или его детальная страница
  if (current === item.name) return true
  // CrmStudentDetail подсвечивает CrmStudents и т.д.
  if (current && current.startsWith(item.name)) return true
  return false
}
</script>

<style scoped>
.crm-sidebar {
  flex-shrink: 0;
  width: 220px;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  padding: 12px 8px;
  position: sticky;
  top: 100px;
}

.crm-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.crm-nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #5d544c;
  font-size: 15px;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
}

.crm-nav-link:hover {
  background: #faf6f0;
  color: #15110f;
}

.crm-nav-link.active {
  background: #0e0c0c;
  color: #ffffff;
}

.crm-nav-link.active .crm-nav-icon {
  color: #c49a3f;
}

.crm-nav-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #8a8079;
  transition: color 0.2s;
}

.crm-nav-label {
  flex: 1;
}

.crm-nav-badge {
  font-size: 11px;
  font-weight: 700;
  background: #8e1519;
  color: #fff;
  padding: 2px 7px;
  border-radius: 999px;
}

@media (max-width: 980px) {
  .crm-sidebar {
    width: 100%;
    position: static;
    overflow-x: auto;
  }

  .crm-nav {
    flex-direction: row;
    gap: 4px;
  }

  .crm-nav-link {
    white-space: nowrap;
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>