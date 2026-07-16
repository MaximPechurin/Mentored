<template>
  <div>
    <h2 class="ac-section-title">Mis cursos</h2>
    <div class="ac-courses">
      <div v-for="course in courses" :key="course.title" class="ac-course">
        <div class="ac-course-img">
          <span class="ac-course-category">{{ course.category }}</span>
        </div>
        <div class="ac-course-body">
          <h3 class="ac-course-title">{{ course.title }}</h3>
          <div class="ac-course-progress">
            <span>Progreso</span>
            <span class="ac-course-progress-value">{{ course.progress }}%</span>
          </div>
          <div class="ac-course-bar">
            <div class="ac-course-bar-fill" :style="{ width: course.progressWidth }"></div>
          </div>
          <router-link to="#" class="ac-course-btn">{{ course.cta }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const courses = [
  { category: 'Cursos', title: 'Recupera tu Energía', progress: 72, progressWidth: '72%', cta: 'Continuar' },
  { category: 'Cursos', title: 'El Camino del Propósito', progress: 30, progressWidth: '30%', cta: 'Continuar' },
  { category: 'Comunidad', title: 'Hábitos que Transforman', progress: 100, progressWidth: '100%', cta: 'Repasar' }
]
</script>

<style scoped>
.ac-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.ac-courses {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.ac-course {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 18px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.ac-course-img {
  height: 120px;
  background: #1a1212;
  position: relative;
}

.ac-course-img::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(135deg, #241818 0 10px, #1a1212 10px 20px);
}

.ac-course-category {
  position: absolute;
  left: 18px;
  bottom: 14px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #c49a3f;
  z-index: 1;
}

.ac-course-body {
  padding: 22px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ac-course-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 16px;
  line-height: 1.25;
}

.ac-course-progress {
  display: flex;
  justify-content: space-between;
  font-size: 13.5px;
  color: #8a8079;
  margin-bottom: 8px;
}

.ac-course-progress-value {
  font-weight: 600;
  color: #8e1519;
}

.ac-course-bar {
  height: 7px;
  border-radius: 4px;
  background: #f0ebe5;
  overflow: hidden;
  margin-bottom: 18px;
}

.ac-course-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: #8e1519;
  transition: width 0.3s;
}

.ac-course-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  text-decoration: none;
  background: #0e0c0c;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  padding: 12px;
  border-radius: 999px;
  transition: background 0.3s;
}

.ac-course-btn:hover {
  background: #2a2525;
}

@media (max-width: 920px) {
  .ac-courses { grid-template-columns: 1fr !important; }
}
</style>