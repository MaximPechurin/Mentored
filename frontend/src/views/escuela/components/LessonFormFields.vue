<template>
  <div class="esc-lesson-fields">
    <input v-model="form.title" type="text" class="esc-input" :placeholder="st('teacher.nombreLeccion')" />
    <RichTextEditor v-model="form.content" :placeholder="st('teacher.contenidoLeccion')" />
    <input v-model="form.duration_minutes" type="number" min="0" class="esc-input esc-input--short" :placeholder="st('teacher.duracionMin')" />

    <div class="esc-video-mode">
      <label><input type="radio" v-model="form.videoMode" value="file" /> {{ st('teacher.subirVideo') }}</label>
      <label><input type="radio" v-model="form.videoMode" value="url" /> {{ st('teacher.enlaceVideo') }}</label>
    </div>

    <input
      v-if="form.videoMode === 'file'"
      type="file"
      accept="video/*"
      class="esc-file"
      @change="$emit('video-file-change', $event)"
    />
    <input
      v-else
      v-model="form.videoUrl"
      type="text"
      class="esc-input"
      placeholder="YouTube, Vimeo o Bunny (mediadelivery.net)"
    />
  </div>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

// Ленивая загрузка: Quill (~230КБ) попадает в отдельный чанк и грузится
// только когда препод открывает форму урока, а не всем подряд (студенты
// редактор не видят вовсе).
const RichTextEditor = defineAsyncComponent(() => import('./RichTextEditor.vue'))

defineProps({
  form: { type: Object, required: true },
  st: { type: Function, required: true },
})
defineEmits(['video-file-change'])
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

.esc-video-mode { display: flex; gap: 18px; margin-bottom: 12px; font-size: 14px; color: #3f3a35; }
.esc-video-mode label { display: flex; align-items: center; gap: 6px; cursor: pointer; }

.esc-file { display: block; font-size: 13.5px; color: #6b6259; margin-bottom: 12px; }
</style>
