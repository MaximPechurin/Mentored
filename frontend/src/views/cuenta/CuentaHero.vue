<template>
  <section class="ac-hero">
    <div class="ac-hero-container">
      <span class="ac-hero-avatar">{{ userInitials }}</span>
      <div>
        <span class="ac-hero-tag">Mi cuenta</span>
        <h1 class="ac-hero-title">Hola, {{ userDisplayName }}</h1>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from '../../composables/useAuth'

const { user } = useAuth()

const userDisplayName = computed(() => {
  if (!user.value) return 'Invitado'
  return user.value.full_name || user.value.username || user.value.email || 'Invitado'
})

const userInitials = computed(() => {
  if (!user.value) return '?'
  const name = user.value.full_name || user.value.username || user.value.email || 'U'
  return name.charAt(0).toUpperCase()
})
</script>

<style scoped>
/* стили без изменений */
.ac-hero {
  background: #0e0c0c;
  padding: 52px 32px;
}
.ac-hero-container {
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 22px;
}
.ac-hero-avatar {
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
.ac-hero-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 8px;
}
.ac-hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  line-height: 1.1;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.3px;
}
@media (max-width: 920px) {
  .ac-hero { padding: 40px 20px !important; }
}
</style>