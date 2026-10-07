<template>
  <header class="crm-header">
    <div class="crm-header-inner">
      <div class="crm-header-left">
        <span class="crm-badge">MENTORED · CRM</span>
        <h1 class="crm-title">Panel del director</h1>
      </div>
      <div class="crm-header-right">
        <span class="crm-user">{{ userName }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from "../../composables/useAuth.js";

const { user } = useAuth()
const userName = computed(() => user.value?.username || user.value?.email || '')
</script>

<style scoped>
.crm-header {
  background: #0e0c0c;
  color: #fff;
  border-bottom: 1px solid #211d1d;
}

.crm-header-inner {
  max-width: 1480px;
  margin: 0 auto;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.crm-badge {
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #c49a3f;
  text-transform: uppercase;
}

.crm-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  margin: 6px 0 0;
  letter-spacing: -0.3px;
}

.crm-header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 15px;
}

.crm-user {
  color: #a59c93;
}

.crm-admin-link {
  color: #c49a3f;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.crm-admin-link:hover {
  color: #ffffff;
}

@media (max-width: 700px) {
  .crm-header-inner { padding: 20px; }
  .crm-title { font-size: 22px; }
}
</style>