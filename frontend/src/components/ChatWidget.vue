<template>
  <div class="chat-widget">
    <!-- Плавающая кнопка -->
    <button v-if="!open" class="chat-fab" @click="openWidget">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
      </svg>
      <span v-if="directory.total_unread" class="chat-dot chat-dot--fab"></span>
    </button>

    <!-- Панель -->
    <div v-else class="chat-panel">
      <div class="chat-head">
        <button v-if="view !== 'list'" class="chat-back" @click="goBack">{{ st('chat.back') }}</button>
        <span class="chat-title">{{ headerTitle }}</span>
        <button class="chat-close" @click="open = false">✕</button>
      </div>

      <div class="chat-body">
        <!-- Список курсов -->
        <template v-if="view === 'list'">
          <p v-if="directory.courses.length === 0" class="chat-empty">{{ st('chat.noChats') }}</p>
          <button
            v-for="c in directory.courses"
            :key="c.id"
            class="chat-row"
            @click="openCourse(c)"
          >
            <span class="chat-row-ic">📁</span>
            <span class="chat-row-name">{{ c.title }}</span>
            <span v-if="c.unread" class="chat-dot"></span>
          </button>
        </template>

        <!-- Собеседники в курсе -->
        <template v-else-if="view === 'people'">
          <p v-if="selectedCourse.people.length === 0" class="chat-empty">{{ st('chat.noChats') }}</p>
          <button
            v-for="p in selectedCourse.people"
            :key="p.user_id"
            class="chat-row"
            @click="openThread(p)"
          >
            <span class="chat-row-ic">👤</span>
            <span class="chat-row-name">{{ p.name }}</span>
            <span v-if="p.unread" class="chat-dot"></span>
          </button>
        </template>

        <!-- Переписка -->
        <template v-else-if="view === 'thread'">
          <div ref="msgBox" class="chat-messages">
            <p v-if="messages.length === 0" class="chat-empty">{{ st('chat.empty') }}</p>
            <div
              v-for="m in messages"
              :key="m.id"
              class="chat-msg"
              :class="{ mine: m.is_mine }"
            >
              {{ m.content }}
            </div>
          </div>
          <form class="chat-input" @submit.prevent="send">
            <input v-model="draft" :placeholder="st('chat.placeholder')" />
            <button type="submit" :disabled="!draft.trim()">{{ st('chat.send') }}</button>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { schoolApi } from '../api/school'
import { useSchoolLang } from '../composables/useSchoolLang'

const { st } = useSchoolLang()

const open = ref(false)
const view = ref('list') // list | people | thread
const directory = reactive({ role: '', total_unread: 0, courses: [] })
const selectedCourse = ref({ people: [] })
const selectedPerson = ref(null)
const messages = ref([])
const draft = ref('')
const msgBox = ref(null)
let poll = null

const headerTitle = computed(() => {
  if (view.value === 'thread') return selectedPerson.value?.name || st('chat.title')
  if (view.value === 'people') return selectedCourse.value?.title || st('chat.title')
  return st('chat.title')
})

const loadDirectory = async () => {
  try {
    const { data } = await schoolApi.chatDirectory()
    directory.role = data.role
    directory.total_unread = data.total_unread
    directory.courses = data.courses
    // если открыт список курса - обновим его данные (счётчики)
    if (view.value === 'people' && selectedCourse.value) {
      const fresh = data.courses.find((c) => c.id === selectedCourse.value.id)
      if (fresh) selectedCourse.value = fresh
    }
  } catch (e) { /* тихо: чат не критичен */ }
}

const openWidget = () => {
  open.value = true
  loadDirectory()
}

const openCourse = (c) => {
  selectedCourse.value = c
  view.value = 'people'
}

const openThread = async (p) => {
  selectedPerson.value = p
  view.value = 'thread'
  await loadThread()
  await loadDirectory() // непрочитанные обнулились после чтения
}

const loadThread = async () => {
  if (!selectedPerson.value) return
  try {
    const { data } = await schoolApi.getConversation(selectedPerson.value.user_id)
    messages.value = data
    await nextTick()
    if (msgBox.value) msgBox.value.scrollTop = msgBox.value.scrollHeight
  } catch (e) { /* noop */ }
}

const send = async () => {
  const text = draft.value.trim()
  if (!text || !selectedPerson.value) return
  draft.value = ''
  try {
    const { data } = await schoolApi.sendMessage(selectedPerson.value.user_id, text)
    messages.value.push(data)
    await nextTick()
    if (msgBox.value) msgBox.value.scrollTop = msgBox.value.scrollHeight
  } catch (e) {
    draft.value = text // вернуть, если не ушло
  }
}

const goBack = () => {
  if (view.value === 'thread') view.value = 'people'
  else if (view.value === 'people') view.value = 'list'
  loadDirectory()
}

onMounted(() => {
  loadDirectory()
  poll = setInterval(() => {
    loadDirectory()
    if (open.value && view.value === 'thread') loadThread()
  }, 15000)
})
onUnmounted(() => { if (poll) clearInterval(poll) })
</script>

<style scoped>
.chat-widget {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 200;
  font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif;
}

.chat-fab {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #ffffff;      /* белая кнопка */
  color: #8e1519;          /* красная эмблема (иконка внутри белая - fill: none) */
  border: 1px solid #ece7e1;
  cursor: pointer;
  box-shadow: 0 10px 24px -8px rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.2s, transform 0.2s;
}
.chat-fab:hover { box-shadow: 0 12px 28px -8px rgba(0,0,0,0.45); transform: translateY(-1px); }

.chat-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #e23b3b;
  flex-shrink: 0;
}
.chat-dot--fab {
  position: absolute;
  top: 8px;
  right: 8px;
  border: 2px solid #ffffff;  /* белая обводка под белую кнопку */
}

.chat-panel {
  width: 360px;
  max-width: calc(100vw - 32px);
  height: 520px;
  max-height: calc(100vh - 48px);
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 48px -12px rgba(0,0,0,0.4);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-head {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #0e0c0c;
  color: #fff;
  padding: 12px 14px;
}
.chat-title { flex: 1; font-weight: 600; font-size: 15px; }
.chat-back, .chat-close {
  background: none;
  border: none;
  color: #c9c1ba;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
}
.chat-back:hover, .chat-close:hover { color: #fff; }

.chat-body { flex: 1; display: flex; flex-direction: column; min-height: 0; }

.chat-empty { color: #8a8079; text-align: center; padding: 24px 16px; margin: 0; }

.chat-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  background: none;
  border: none;
  border-bottom: 1px solid #f0ebe5;
  padding: 14px 16px;
  cursor: pointer;
  font-family: inherit;
  font-size: 15px;
  text-align: left;
  color: #1c1c1c;
}
.chat-row:hover { background: #faf8f5; }
.chat-row-ic { flex-shrink: 0; }
.chat-row-name { flex: 1; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #f6f3ef;
}
.chat-msg {
  max-width: 80%;
  padding: 9px 13px;
  border-radius: 14px;
  font-size: 14.5px;
  line-height: 1.4;
  background: #fff;
  border: 1px solid #ece7e1;
  align-self: flex-start;
  white-space: pre-wrap;
  word-break: break-word;
}
.chat-msg.mine {
  align-self: flex-end;
  background: #8e1519;
  color: #fff;
  border-color: #8e1519;
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 10px;
  border-top: 1px solid #ece7e1;
  background: #fff;
}
.chat-input input {
  flex: 1;
  border: 1px solid #e4ddd2;
  border-radius: 999px;
  padding: 10px 14px;
  font-family: inherit;
  font-size: 14.5px;
  outline: none;
}
.chat-input input:focus { border-color: #8e1519; }
.chat-input button {
  background: #0e0c0c;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}
.chat-input button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
