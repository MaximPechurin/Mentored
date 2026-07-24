<template>
  <div class="cuenta-page">
    <CuentaHero />
    <div class="ac-shell">
      <CuentaSidebar v-model="activeTab" @logout="handleLogout" />
      <main class="ac-main">
        <CuentaPerfil v-if="activeTab === 'perfil'" />
        <CuentaPedidos v-else-if="activeTab === 'pedidos'" />
        <!-- <CuentaCursos v-else-if="activeTab === 'cursos'" /> МБ ВЕРНУТЬ В ДАЛЬНЕЙШЕМ -->
        <CuentaConfig v-else-if="activeTab === 'config'" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import CuentaHero from './CuentaHero.vue'
import CuentaSidebar from './CuentaSidebar.vue'
import CuentaPerfil from './CuentaPerfil.vue'
import CuentaPedidos from './CuentaPedidos.vue'
//import CuentaCursos from './CuentaCursos.vue'
import CuentaConfig from './CuentaConfig.vue'

const router = useRouter()
const { user, refreshUser, logout } = useAuth()
const activeTab = ref('perfil')

const handleLogout = () => {
  logout()
  router.push('/login')
}

onMounted(() => {
  refreshUser()
})
</script>

<style scoped>
.cuenta-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f6f3ef;
  min-height: 100vh;
}

.ac-shell {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 264px 1fr;
  gap: 36px;
  padding: 48px 32px 88px;
  align-items: start;
}

.ac-main {
  min-width: 0;
}

@media (max-width: 920px) {
  .ac-shell {
    grid-template-columns: 1fr !important;
    gap: 24px !important;
    padding: 32px 20px 72px !important;
  }
}
</style>