<template>
  <section class="ct-faq">
    <h2 class="ct-faq-title">Preguntas frecuentes</h2>
    <div class="ct-faq-list">
      <div
        v-for="(faq, index) in faqs"
        :key="index"
        class="ct-faq-item"
        :class="{ open: faq.open }"
      >
        <button @click="toggleFaq(index)" class="ct-faq-btn">
          <span>{{ faq.q }}</span>
          <span class="ct-faq-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </span>
        </button>
        <div v-if="faq.open" class="ct-faq-answer">
          <p>{{ faq.a }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const faqsData = [
  {
    q: '¿Cómo accedo a un curso después de comprarlo?',
    a: 'El acceso se activa de inmediato en tu cuenta tras confirmar el pago, y también recibes un correo con el enlace.'
  },
  {
    q: '¿Puedo reprogramar mi consulta 1:1?',
    a: 'Sí. Puedes reprogramar o cancelar con reembolso hasta 48 horas antes de la sesión escribiéndonos por WhatsApp o email.'
  },
  {
    q: '¿Tienen política de devoluciones?',
    a: 'Los cursos y libros digitales tienen 14 días de garantía si no has consumido más del 30% del contenido. Consulta los detalles en Condiciones de compra.'
  },
  {
    q: '¿Qué métodos de pago aceptan?',
    a: 'Aceptamos pagos con Mercado Pago y Culqi, que admiten tarjeta de crédito, débito y otros medios.'
  }
]

const openIndex = ref(-1)

const faqs = ref(faqsData.map((item, index) => ({
  ...item,
  open: index === 0
})))

const toggleFaq = (index) => {
  openIndex.value = openIndex.value === index ? -1 : index
  faqs.value = faqsData.map((item, i) => ({
    ...item,
    open: i === openIndex.value
  }))
}
</script>

<style scoped>
.ct-faq {
  max-width: 1160px;
  margin: 0 auto;
  padding: 32px 32px 96px;
}

.ct-faq-title {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 24px;
  letter-spacing: -0.3px;
}

.ct-faq-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ct-faq-item {
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 14px 36px -34px rgba(0,0,0,0.4);
  transition: box-shadow 0.3s;
}

.ct-faq-item.open {
  box-shadow: 0 18px 40px -34px rgba(0,0,0,0.5);
}

.ct-faq-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  padding: 22px 26px;
}

.ct-faq-btn span:first-child {
  font-size: 17.5px;
  font-weight: 500;
  color: #15110f;
}

.ct-faq-icon {
  display: inline-flex;
  color: #a89f93;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.ct-faq-item.open .ct-faq-icon {
  color: #8e1519;
  transform: rotate(180deg);
}

.ct-faq-answer {
  padding: 0 26px 24px;
}

.ct-faq-answer p {
  margin: 0;
  font-size: 16px;
  line-height: 1.65;
  color: #5d544c;
}

@media (max-width: 920px) {
  .ct-faq {
    padding: 24px 20px 80px !important;
  }
}
</style>