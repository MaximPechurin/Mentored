<template>
  <div class="esc-rte">
    <div ref="editorEl"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
import { schoolApi } from '../../../api/school'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue'])

const editorEl = ref(null)
let quill = null
// Флаг, чтобы не зациклить: программная установка контента не должна
// тут же снова эмитить update и перетирать курсор пользователя.
let settingFromProp = false

const toolbar = [
  [{ header: [1, 2, 3, false] }],
  ['bold', 'italic', 'underline', 'strike'],
  [{ color: [] }, { background: [] }],
  [{ list: 'ordered' }, { list: 'bullet' }],
  [{ align: [] }],
  ['link', 'image'],
  ['clean'],
]

const imageHandler = () => {
  const input = document.createElement('input')
  input.setAttribute('type', 'file')
  input.setAttribute('accept', 'image/*')
  input.click()
  input.onchange = async () => {
    const file = input.files && input.files[0]
    if (!file) return
    const range = quill.getSelection(true)
    // временный плейсхолдер, пока грузится
    quill.insertText(range.index, '⏳', { italic: true })
    try {
      const fd = new FormData()
      fd.append('image', file)
      const { data } = await schoolApi.uploadInlineImage(fd)
      quill.deleteText(range.index, 1)
      quill.insertEmbed(range.index, 'image', data.url)
      quill.setSelection(range.index + 1)
    } catch (error) {
      quill.deleteText(range.index, 1)
      console.error('Error al subir la imagen:', error)
      alert(error.response?.data?.error || 'Error al subir la imagen.')
    }
  }
}

onMounted(() => {
  quill = new Quill(editorEl.value, {
    theme: 'snow',
    placeholder: props.placeholder,
    modules: {
      toolbar: { container: toolbar, handlers: { image: imageHandler } },
    },
  })
  if (props.modelValue) {
    settingFromProp = true
    quill.clipboard.dangerouslyPasteHTML(props.modelValue)
    settingFromProp = false
  }
  quill.on('text-change', () => {
    if (settingFromProp) return
    const html = quill.root.innerHTML
    // Quill для пустого редактора хранит '<p><br></p>' - отдаём '' наружу.
    emit('update:modelValue', html === '<p><br></p>' ? '' : html)
  })
})

// Внешняя переустановка значения (например, при открытии формы
// редактирования другого урока или сбросе формы).
watch(() => props.modelValue, (val) => {
  if (!quill) return
  const current = quill.root.innerHTML
  const normalized = current === '<p><br></p>' ? '' : current
  if (val === normalized) return
  settingFromProp = true
  quill.setContents([])
  if (val) quill.clipboard.dangerouslyPasteHTML(val)
  settingFromProp = false
})

onBeforeUnmount(() => { quill = null })
</script>

<style scoped>
.esc-rte {
  margin-bottom: 12px;
}
/* Quill snow тема - слегка подгоняем под кремовый фон форм школы. */
.esc-rte :deep(.ql-toolbar) {
  border: 1px solid #e4ddd2;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  background: #fbf9f6;
}
.esc-rte :deep(.ql-container) {
  border: 1px solid #e4ddd2;
  border-top: none;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  background: #fff;
  font-family: inherit;
  font-size: 14.5px;
}
.esc-rte :deep(.ql-editor) {
  min-height: 160px;
  color: #15110f;
}
.esc-rte :deep(.ql-editor.ql-blank::before) {
  font-style: normal;
  color: #a49a8e;
}
</style>
