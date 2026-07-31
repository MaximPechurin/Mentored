<template>
  <div v-if="checking" class="esc-checking">Cargando...</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <span class="esc-hero-avatar">{{ userInitials }}</span>
        <div>
          <span class="esc-hero-tag">Panel de profesor</span>
          <h1 class="esc-hero-title">Hola, {{ userDisplayName }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <section class="esc-block">
        <h2 class="esc-section-title">Mis cursos</h2>

        <!--
          Todavía no hay API de la escuela (school/) para traer los
          cursos reales asignados via CourseTeacher - eso es la Semana 2
          del plan (ver PLAN_ETAP2.md). Por ahora mostramos el estado
          vacío, ya conectado al control de acceso por rol real.
        -->
        <div v-if="courses.length === 0" class="esc-empty">
          <p class="esc-empty-text">Todavía no tienes cursos asignados.</p>
        </div>

        <div v-else class="esc-courses">
          <div v-for="course in courses" :key="course.id" class="esc-course">
            <h3 class="esc-course-title">{{ course.title }}</h3>
          </div>
        </div>
      </section>

      <section class="esc-block">
        <h2 class="esc-section-title">Tareas por revisar</h2>

        <div v-if="submissions.length === 0" class="esc-empty">
          <p class="esc-empty-text">No hay tareas pendientes de revisión.</p>
        </div>

        <div v-else class="esc-courses">
          <div v-for="s in submissions" :key="s.id" class="esc-course">
            <h3 class="esc-course-title">{{ s.title }}</h3>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'

const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()

const checking = ref(true)
// Реальные данные появятся с school API (Неделя 2 плана: CourseTeacher
// -> список курсов, Submission со статусом 'submitted' -> очередь на
// проверку). Пока пусто, структура страницы уже готова под это.
const courses = ref([])
const submissions = ref([])

const userDisplayName = computed(() => {
  if (!user.value) return 'Invitado'
  return user.value.full_name || user.value.username || user.value.email || 'Invitado'
})

const userInitials = computed(() => {
  const name = userDisplayName.value
  return name ? name.charAt(0).toUpperCase() : '?'
})

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.replace('/login')
    return
  }

  // Роли могут быть устаревшими в localStorage (например, только что
  // назначены из админки) - подтягиваем свежий профиль перед проверкой.
  const fresh = await refreshUser()
  const roles = fresh?.roles ?? user.value?.roles ?? []

  if (!roles.includes('teacher')) {
    router.replace('/cuenta')
    return
  }

  checking.value = false
})
</script>

<style scoped>
.esc-checking {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  color: #6b6259;
}

.esc-page {
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
  font-weight: 300;
  color: #1c1c1c;
  background: #f6f3ef;
  min-height: 100vh;
}

.esc-hero {
  background: #0e0c0c;
  padding: 52px 32px;
}

.esc-hero-container {
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 22px;
}

.esc-hero-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  flex-shrink: 0;
}

.esc-hero-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 8px;
}

.esc-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.3px;
}

.esc-shell {
  max-width: 1180px;
  margin: 0 auto;
  padding: 48px 32px 88px;
}

.esc-block + .esc-block {
  margin-top: 40px;
}

.esc-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.esc-empty {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 48px 32px;
  text-align: center;
}

.esc-empty-text {
  font-size: 16px;
  color: #6b6259;
  margin: 0;
}

.esc-courses {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.esc-course {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  padding: 22px;
}

.esc-course-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0;
}

@media (max-width: 920px) {
  .esc-hero { padding: 40px 20px !important; }
  .esc-shell { padding: 32px 20px 72px !important; }
}
</style>
