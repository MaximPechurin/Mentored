<template>
  <div v-if="checking" class="esc-checking">{{ st('common.cargando') }}</div>
  <div v-else class="esc-page">
    <section class="esc-hero">
      <div class="esc-hero-container">
        <div>
          <a href="#" class="esc-back" @click.prevent="goBack">{{ st('foro.back') }}</a>
          <h1 class="esc-hero-title">{{ st('foro.title') }}</h1>
        </div>
      </div>
    </section>

    <div class="esc-shell">
      <!-- Список тем -->
      <template v-if="!activeThread">
        <!-- новая тема -->
        <div class="foro-new">
          <input v-model="newTitle" :placeholder="st('foro.threadTitle')" class="foro-input" />
          <textarea v-model="newContent" rows="2" :placeholder="st('foro.message')" class="esc-textarea"></textarea>
          <button class="esc-complete-btn" :disabled="creating || !newTitle.trim() || !newContent.trim()" @click="create">
            {{ st('foro.create') }}
          </button>
        </div>

        <p v-if="!loading && threads.length === 0" class="foro-empty">{{ st('foro.empty') }}</p>

        <div class="foro-threads">
          <button v-for="t in threads" :key="t.id" class="foro-thread-row" @click="openThread(t.id)">
            <div class="foro-thread-main">
              <span class="foro-thread-title">
                <span v-if="t.is_pinned" class="foro-pin">{{ st('foro.pinned') }}</span>
                {{ t.title }}
              </span>
              <span class="foro-thread-meta">{{ t.author }} · {{ t.posts_count }} {{ st('foro.posts') }}</span>
            </div>
            <span v-if="t.is_locked" class="foro-badge-lock">🔒</span>
          </button>
        </div>
      </template>

      <!-- Открытая тема -->
      <template v-else>
        <a href="#" class="esc-back esc-back--dark" @click.prevent="activeThread = null">{{ st('foro.backThreads') }}</a>
        <div class="foro-thread-head">
          <h2 class="foro-open-title">
            <span v-if="activeThread.is_pinned" class="foro-pin">{{ st('foro.pinned') }}</span>
            {{ activeThread.title }}
            <span v-if="activeThread.is_locked" class="foro-lock-tag">🔒 {{ st('foro.locked') }}</span>
          </h2>
          <div v-if="isTeacher" class="foro-mod">
            <button @click="moderate('is_pinned', !activeThread.is_pinned)">
              {{ activeThread.is_pinned ? st('foro.unpin') : st('foro.pin') }}
            </button>
            <button @click="moderate('is_locked', !activeThread.is_locked)">
              {{ activeThread.is_locked ? st('foro.unlock') : st('foro.lock') }}
            </button>
          </div>
        </div>

        <div class="foro-posts">
          <p v-if="activeThread.posts.length === 0" class="foro-empty">{{ st('foro.noPosts') }}</p>
          <div v-for="p in activeThread.posts" :key="p.id" class="foro-post">
            <div class="foro-post-head">
              <span class="foro-post-author">{{ p.author }}</span>
              <span v-if="p.is_teacher" class="foro-teacher-badge">{{ st('foro.teacher') }}</span>
            </div>
            <div class="foro-post-text">{{ p.content }}</div>
          </div>
        </div>

        <!-- ответ (в закрытой теме - только преподаватель) -->
        <div v-if="!activeThread.is_locked || isTeacher" class="foro-reply">
          <textarea v-model="replyText" rows="2" :placeholder="st('foro.writeReply')" class="esc-textarea"></textarea>
          <button class="esc-complete-btn" :disabled="replying || !replyText.trim()" @click="reply">
            {{ st('foro.reply') }}
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { schoolApi } from '../../api/school'
import { useSchoolLang } from '../../composables/useSchoolLang'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, refreshUser } = useAuth()
const { st } = useSchoolLang()

const courseId = route.params.courseId
const checking = ref(true)
const loading = ref(true)
const threads = ref([])
const activeThread = ref(null)
const newTitle = ref('')
const newContent = ref('')
const creating = ref(false)
const replyText = ref('')
const replying = ref(false)

const isTeacher = computed(() => !!user.value?.roles?.includes('teacher'))

const goBack = () => router.back()

const loadThreads = async () => {
  loading.value = true
  try {
    const { data } = await schoolApi.courseThreads(courseId)
    threads.value = data
  } catch (e) { console.error('foro threads', e) } finally { loading.value = false }
}

const create = async () => {
  creating.value = true
  try {
    await schoolApi.createThread(courseId, { title: newTitle.value, content: newContent.value })
    newTitle.value = ''; newContent.value = ''
    await loadThreads()
  } catch (e) { console.error('foro create', e); alert('Error') } finally { creating.value = false }
}

const openThread = async (id) => {
  try {
    const { data } = await schoolApi.getThread(id)
    activeThread.value = data
  } catch (e) { console.error('foro open', e) }
}

const reply = async () => {
  replying.value = true
  try {
    const { data } = await schoolApi.replyThread(activeThread.value.id, replyText.value)
    activeThread.value.posts.push(data)
    replyText.value = ''
  } catch (e) { console.error('foro reply', e); alert('Error') } finally { replying.value = false }
}

const moderate = async (field, value) => {
  try {
    const { data } = await schoolApi.moderateThread(activeThread.value.id, { [field]: value })
    activeThread.value.is_pinned = data.is_pinned
    activeThread.value.is_locked = data.is_locked
  } catch (e) { console.error('foro moderate', e); alert('Solo el profesor del curso') }
}

onMounted(async () => {
  if (!isAuthenticated.value) { router.replace('/login'); return }
  const fresh = await refreshUser()
  const isDev = fresh?.is_dev ?? user.value?.is_dev ?? false
  if (!isDev) { router.replace('/'); return }
  checking.value = false
  await loadThreads()
})
</script>

<style scoped>
.esc-checking { min-height: 60vh; display: flex; align-items: center; justify-content: center; font-family: 'Hanken Grotesk', sans-serif; color: #6b6259; }
.esc-page { font-family: 'Hanken Grotesk', -apple-system, Helvetica, Arial, sans-serif; font-weight: 300; color: #1c1c1c; background: #f6f3ef; min-height: 100vh; }
.esc-hero { background: #0e0c0c; padding: 52px 32px; }
.esc-hero-container { max-width: 820px; margin: 0 auto; }
.esc-back { display: inline-block; color: #c49a3f; text-decoration: none; font-size: 14px; font-weight: 500; margin-bottom: 12px; }
.esc-back:hover { text-decoration: underline; }
.esc-back--dark { color: #8e1519; margin-bottom: 16px; }
.esc-hero-title { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 600; color: #fff; margin: 0; }
.esc-shell { max-width: 820px; margin: 0 auto; padding: 32px 32px 88px; }

.esc-textarea { width: 100%; box-sizing: border-box; border: 1px solid #e4ddd2; border-radius: 10px; padding: 10px 12px; font-family: inherit; font-size: 14.5px; background: #fbf9f6; outline: none; resize: vertical; margin-bottom: 10px; }
.esc-textarea:focus { border-color: #8e1519; }
.foro-input { width: 100%; box-sizing: border-box; border: 1px solid #e4ddd2; border-radius: 10px; padding: 11px 12px; font-family: inherit; font-size: 15px; background: #fbf9f6; outline: none; margin-bottom: 10px; }
.foro-input:focus { border-color: #8e1519; }
.esc-complete-btn { background: #0e0c0c; color: #fff; border: none; border-radius: 999px; font-weight: 600; font-size: 14.5px; padding: 10px 22px; cursor: pointer; font-family: inherit; }
.esc-complete-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.foro-new { background: #fff; border: 1px solid #ece7e1; border-radius: 16px; padding: 18px; margin-bottom: 22px; }
.foro-empty { color: #8a8079; text-align: center; padding: 24px; }

.foro-threads { display: flex; flex-direction: column; gap: 10px; }
.foro-thread-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%; background: #fff; border: 1px solid #ece7e1; border-radius: 14px; padding: 15px 18px; cursor: pointer; font-family: inherit; text-align: left; }
.foro-thread-row:hover { border-color: #8e1519; }
.foro-thread-main { display: flex; flex-direction: column; min-width: 0; }
.foro-thread-title { font-weight: 600; color: #15110f; font-size: 15.5px; }
.foro-thread-meta { font-size: 13px; color: #8a8079; margin-top: 2px; }
.foro-pin { color: #c49a3f; font-size: 12.5px; font-weight: 600; margin-right: 6px; }
.foro-badge-lock { flex-shrink: 0; }

.foro-thread-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; margin-bottom: 16px; }
.foro-open-title { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 600; color: #15110f; margin: 0; }
.foro-lock-tag { font-size: 13px; color: #a52a2a; font-family: 'Hanken Grotesk', sans-serif; font-weight: 500; margin-left: 8px; }
.foro-mod { display: flex; gap: 8px; flex-shrink: 0; }
.foro-mod button { background: #fff; border: 1px solid #e4ddd2; border-radius: 999px; padding: 6px 14px; font-family: inherit; font-size: 13px; cursor: pointer; color: #5d544c; }
.foro-mod button:hover { border-color: #8e1519; color: #8e1519; }

.foro-posts { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }
.foro-post { background: #fff; border: 1px solid #ece7e1; border-radius: 14px; padding: 14px 16px; }
.foro-post-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.foro-post-author { font-weight: 600; color: #15110f; font-size: 14.5px; }
.foro-teacher-badge { background: #fff4e0; color: #9a6a00; font-size: 11.5px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.foro-post-text { font-size: 14.5px; line-height: 1.6; color: #3f3a35; white-space: pre-wrap; word-break: break-word; }

.foro-reply { background: #fff; border: 1px solid #ece7e1; border-radius: 16px; padding: 16px; }
</style>
