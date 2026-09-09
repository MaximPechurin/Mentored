<template>
  <div class="esc-assignment-fields">
    <input v-model="form.title" type="text" class="esc-input" :placeholder="st('teacher.nombreTarea')" />
    <textarea v-model="form.description" rows="3" class="esc-textarea" :placeholder="st('teacher.descripcionTarea')"></textarea>
    <input v-model="form.max_score" type="number" min="0" class="esc-input esc-input--short" :placeholder="st('teacher.puntosMax')" />
    <label class="esc-required-toggle">
      <input type="checkbox" v-model="form.is_required" /> {{ st('teacher.obligatoriaLabel') }}
    </label>
  </div>
</template>

<script setup>
defineProps({
  form: { type: Object, required: true },
  st: { type: Function, required: true },
})
</script>

<style scoped>
.esc-input, .esc-textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e4ddd2;
  border-radius: 10px;
  padding: 12px;
  font-family: inherit;
  font-size: 14.5px;
  color: #15110f;
  background: #fbf9f6;
  outline: none;
  margin-bottom: 12px;
}
.esc-input--short { width: 160px; }
.esc-textarea { resize: vertical; }
.esc-input:focus, .esc-textarea:focus { border-color: #8e1519; }

.esc-required-toggle { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #3f3a35; margin-bottom: 12px; }
</style>
