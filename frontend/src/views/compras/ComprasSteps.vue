<template>
  <div class="cp-steps-wrapper">
    <div class="cp-steps">
      <div v-for="step in steps" :key="step.number" class="cp-step">
        <span class="cp-step-number">{{ step.number }}</span>
        <h3 class="cp-step-title">{{ step.title }}</h3>
        <p class="cp-step-text">{{ step.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const steps = [
  {
    number: 1,
    title: 'Elige tu producto',
    text: 'Añade cursos, libros o consultas al carrito desde la tienda.'
  },
  {
    number: 2,
    title: 'Realiza el pago',
    text: 'Completa el checkout con un medio de pago seguro.'
  },
  {
    number: 3,
    title: 'Accede al instante',
    text: 'Recibe el acceso en tu cuenta y por correo electrónico.'
  }
]
</script>

<style scoped>
.cp-steps-wrapper {
  max-width: 920px;
  margin: 0 auto;
  padding: 32px 32px 0;
}

.cp-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  margin-bottom: 40px;
}

.cp-step {
  background: #faf7f3;
  border-radius: 16px;
  padding: 26px;
}

.cp-step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 17px;
  margin-bottom: 16px;
}

.cp-step-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 8px;
}

.cp-step-text {
  font-size: 15.5px;
  line-height: 1.6;
  color: #6f655c;
  margin: 0;
}

@media (max-width: 860px) {
  .cp-steps-wrapper { padding: 0 20px; }
  .cp-steps { grid-template-columns: 1fr !important; }
}
</style>