<template>
  <div class="pd-info" v-if="product">
    <span class="pd-category">{{ product.category }}</span>
    <h1 class="pd-title">{{ product.title }}</h1>
    <p class="pd-desc">{{ product.desc }}</p>

    <div class="pd-price">
      <span class="pd-price-current">{{ product.price }}</span>
      <span v-if="product.hasOld" class="pd-price-old">{{ product.oldPrice }}</span>
    </div>

    <div class="pd-actions">
      <button
        class="pd-btn-add"
        :class="{ added: isAdded }"
        @click="handleAddToCart"
      >
        <template v-if="isAdded">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Agregado al carrito
        </template>
        <template v-else>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"/>
            <circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
          </svg>
          Agregar al carrito
        </template>
      </button>
      <button class="pd-btn-buy" @click="$emit('buy-now')">
        Comprar ahora
      </button>
    </div>

    <ProductoIncludes :product="product" />
    <ProductoMeta :product="product" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductoIncludes from './ProductoIncludes.vue'
import ProductoMeta from './ProductoMeta.vue'

const props = defineProps({
  product: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['add-to-cart', 'buy-now'])

const isAdded = ref(false)

const handleAddToCart = () => {
  isAdded.value = true
  emit('add-to-cart')
  setTimeout(() => {
    isAdded.value = false
  }, 1500)
}
</script>

<style scoped>
.pd-category {
  display: inline-block;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: #c49a3f;
  margin-bottom: 14px;
}

.pd-title {
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  line-height: 1.12;
  font-weight: 700;
  color: #15110f;
  margin: 0 0 18px;
  letter-spacing: -0.5px;
}

.pd-desc {
  font-size: 18px;
  line-height: 1.6;
  color: #5d544c;
  margin: 0 0 26px;
}

.pd-price {
  display: flex;
  align-items: baseline;
  gap: 14px;
  margin-bottom: 28px;
}

.pd-price-current {
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  font-weight: 800;
  color: #8e1519;
  line-height: 1;
}

.pd-price-old {
  font-size: 20px;
  color: #a59c93;
  text-decoration: line-through;
}

.pd-actions {
  display: flex;
  gap: 14px;
  margin-bottom: 32px;
}

.pd-btn-add {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: none;
  cursor: pointer;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  padding: 16px 30px;
  border-radius: 12px;
  font-family: inherit;
  background: #8e1519;
  flex: 1;
  transition: background 0.3s;
}

.pd-btn-add:hover {
  background: #a01a1f;
}

.pd-btn-add.added {
  background: #1f7a3d;
}

.pd-btn-buy {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border: 1.5px solid #0e0c0c;
  background: none;
  cursor: pointer;
  color: #0e0c0c;
  font-weight: 600;
  font-size: 16px;
  padding: 15px 26px;
  border-radius: 12px;
  font-family: inherit;
  transition: all 0.3s;
}

.pd-btn-buy:hover {
  background: #0e0c0c;
  color: #fff;
}

@media (max-width: 920px) {
  .pd-title { font-size: 34px !important; }
  .pd-actions { flex-direction: column !important; }
  .pd-actions > * { width: 100% !important; }
}
</style>