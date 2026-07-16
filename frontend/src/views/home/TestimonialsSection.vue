<template>
  <section class="msec msec-pad testimonials">
    <div class="container">
      <span class="section-tag">Testimonios reales</span>
      <h2 class="section-title">Lo que dice nuestra comunidad</h2>

      <div class="grid-3">
        <div v-for="t in testimonials" :key="t.name" class="testimonial-card">
          <span class="quote-mark">“</span>
          <p class="testimonial-quote">{{ t.quote }}</p>
          <div class="testimonial-author">
            <span class="author-initial">{{ t.initial }}</span>
            <div>
              <p class="author-name">{{ t.name }}</p>
              <p class="author-role">{{ t.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  testimonials: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.msec-pad {
  padding: 88px 32px;
}

.testimonials {
  background: #ffffff;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  text-align: center;
}

.section-tag {
  display: inline-block;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #8e1519;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #15110f;
  margin: 0 0 52px;
  letter-spacing: -0.5px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  text-align: left;
}

.testimonial-card {
  background: #faf6f0;
  border: 1px solid #eee3d6;
  border-radius: 20px;
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
}

.quote-mark {
  font-family: 'Playfair Display', serif;
  font-size: 38px;
  line-height: 0.7;
  color: #8e1519;
  height: 22px;
}

.testimonial-quote {
  font-style: italic;
  font-size: 17.5px;
  line-height: 1.65;
  color: #5d544c;
  margin: 0 0 28px;
  flex: 1;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 14px;
}

.author-initial {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: #f1e3de;
  border: 1px solid #e4d3cc;
  color: #8e1519;
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.author-name {
  font-weight: 500;
  font-size: 17px;
  color: #8e1519;
  margin: 0;
}

.author-role {
  font-size: 15px;
  color: #8a8079;
  margin: 0;
}

@media (max-width: 860px) {
  .msec-pad { padding: 56px 20px !important; }
  .section-title { font-size: 27px !important; }
  .grid-3 { grid-template-columns: 1fr !important; }
}
</style>