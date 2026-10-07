<template>
  <div class="crm-progress">
    <div class="crm-progress-bar">
      <div
        class="crm-progress-fill"
        :class="fillClass"
        :style="{ width: percent + '%' }"
      ></div>
    </div>
    <span class="crm-progress-label">{{ percent }}%</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  percent: { type: Number, default: 0 },
})

const fillClass = computed(() => {
  if (props.percent >= 100) return 'fill-success'
  if (props.percent >= 50) return 'fill-mid'
  return 'fill-low'
})
</script>

<style scoped>
.crm-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.crm-progress-bar {
  flex: 1;
  height: 8px;
  background: #f0ede8;
  border-radius: 999px;
  overflow: hidden;
}

.crm-progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s;
}

.fill-low { background: #8e1519; }
.fill-mid { background: #c49a3f; }
.fill-success { background: #1f7a3d; }

.crm-progress-label {
  font-size: 13px;
  font-weight: 600;
  color: #15110f;
  min-width: 36px;
  text-align: right;
}
</style>