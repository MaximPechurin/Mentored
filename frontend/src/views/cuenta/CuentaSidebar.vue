<template>
  <aside class="ac-side">
    <nav class="ac-sidenav">
      <button
        v-for="item in navItems"
        :key="item.key"
        class="ac-navitem"
        :class="{ active: modelValue === item.key }"
        @click="$emit('update:modelValue', item.key)"
      >
        <span class="ac-navicon" v-html="item.icon"></span>
        {{ item.label }}
      </button>
      <div class="ac-divider"></div>
      <button class="ac-navitem ac-logout" @click="$emit('logout')">
        <span class="ac-navicon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </span>
        Cerrar sesión
      </button>
    </nav>
  </aside>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'perfil'
  }
})

defineEmits(['update:modelValue', 'logout'])

const navItems = [
  {
    key: 'perfil',
    label: 'Perfil',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 12 0v1"/><path d="M16 21v-1a6 6 0 0 0-3-5.2"/></svg>`
  },
  {
    key: 'pedidos',
    label: 'Mis pedidos',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>`
  },
  {
    key: 'cursos',
    label: 'Mis cursos',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m2 7 10-5 10 5-10 5z"/><path d="M6 9.5V15c0 1.5 2.7 3 6 3s6-1.5 6-3V9.5"/></svg>`
  },
  {
    key: 'config',
    label: 'Configuración',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`
  }
]
</script>

<style scoped>
.ac-side {
  position: sticky;
  top: 104px;
}

.ac-sidenav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 12px;
}

.ac-navitem {
  display: flex;
  align-items: center;
  gap: 12px;
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 16px;
  padding: 13px 16px;
  border-radius: 12px;
  text-align: left;
  width: 100%;
  color: #5d544c;
  font-weight: 500;
  transition: all 0.3s;
}

.ac-navitem:hover {
  background: #f6f3ef;
}

.ac-navitem.active {
  background: #0e0c0c;
  color: #ffffff;
  font-weight: 600;
}

.ac-navicon {
  display: inline-flex;
  flex-shrink: 0;
}

.ac-divider {
  height: 1px;
  background: #f0ebe5;
  margin: 8px 4px;
}

.ac-logout {
  color: #8a8079;
  text-decoration: none;
}

.ac-logout:hover {
  background: #f6f3ef;
}

@media (max-width: 920px) {
  .ac-side { position: static !important; }
  .ac-sidenav { flex-direction: row !important; overflow-x: auto; gap: 6px !important; }
  .ac-navitem { white-space: nowrap; }
}
</style>