<template>
  <div>
    <h2 class="ac-section-title">Perfil</h2>

    <!-- Данные профиля -->
    <div class="ac-card">
      <div class="ac-grid2" v-if="user">
        <div>
          <span class="ac-label">Nombre completo</span>
          <span class="ac-value">{{ user.full_name || user.username || 'No especificado' }}</span>
        </div>
        <div>
          <span class="ac-label">Correo electrónico</span>
          <span class="ac-value">{{ user.email || 'No especificado' }}</span>
        </div>
        <div>
          <span class="ac-label">WhatsApp</span>
          <span class="ac-value">{{ user.phone || 'No especificado' }}</span>
        </div>
        <div>
          <span class="ac-label">Miembro desde</span>
          <span class="ac-value">{{ formatDate(user.date_joined) }}</span>
        </div>
      </div>
      <div v-else class="ac-loading">
        <p>Cargando datos del perfil...</p>
      </div>
    </div>

    <!-- Статистика -->
    <div class="ac-grid3">
      <div class="ac-stat-card">
        <span class="ac-stat-number">{{ stats.cursos || 0 }}</span>
        <span class="ac-stat-label">Cursos activos</span>
      </div>
      <div class="ac-stat-card">
        <span class="ac-stat-number">{{ stats.pedidos || 0 }}</span>
        <span class="ac-stat-label">Pedidos realizados</span>
      </div>
      <div class="ac-stat-card">
        <span class="ac-stat-number">{{ stats.consultas || 0 }}</span>
        <span class="ac-stat-label">Consultas reservadas</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuth } from '../../composables/useAuth'

const { user, refreshUser } = useAuth()
const stats = ref({
  cursos: 0,
  pedidos: 0,
  consultas: 0,
})

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

// Загружаем статистику (позже заменим на реальные данные с бэка)
const loadStats = async () => {
  try {
    // TODO: заменить на реальные API запросы
    // const response = await userApi.getStats()
    // stats.value = response.data
    stats.value = {
      cursos: 3,
      pedidos: 7,
      consultas: 2,
    }
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
  }
}

onMounted(() => {
  refreshUser()
  loadStats()
})
</script>

<style scoped>
/* стили без изменений */
.ac-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}
.ac-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 32px;
  margin-bottom: 24px;
}
.ac-grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px 32px;
}
.ac-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #a59c93;
  margin-bottom: 7px;
}
.ac-value {
  font-size: 18px;
  color: #15110f;
  font-weight: 400;
}
.ac-grid3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.ac-stat-card {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 24px;
}
.ac-stat-number {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  font-weight: 600;
  color: #8e1519;
  line-height: 1;
  margin-bottom: 8px;
}
.ac-stat-label {
  font-size: 15px;
  color: #6f655c;
}
.ac-loading {
  padding: 20px;
  text-align: center;
  color: #8a8079;
}
@media (max-width: 920px) {
  .ac-grid2 { grid-template-columns: 1fr !important; }
  .ac-grid3 { grid-template-columns: 1fr !important; }
}
</style>