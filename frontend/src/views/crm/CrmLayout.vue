<template>
  <div class="crm-layout">
    <CrmHeader />

    <div class="crm-body">
      <CrmSidebar />

      <main class="crm-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import CrmHeader from "./CrmHeader.vue";
import CrmSidebar from "./CrmSidebar.vue";
</script>

<style scoped>
.crm-layout {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  background: #f5eee3;
  min-height: 100vh;
}

.crm-body {
  display: flex;
  align-items: flex-start;
  max-width: 1480px;
  margin: 0 auto;
  padding: 32px;
  gap: 32px;
}

.crm-main {
  flex: 1;
  min-width: 0; /* чтобы таблицы не вылезали */
}

@media (max-width: 980px) {
  .crm-body {
    flex-direction: column;
    padding: 20px;
    gap: 20px;
  }
}
</style>