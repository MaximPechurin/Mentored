import { ref, readonly } from 'vue'

// Мультиязычность ТОЛЬКО для учебной платформы (/escuela/*).
// Полностью независима от useLanguage витрины (свой ключ в localStorage),
// чтобы выбор языка в школе не менял язык продажного сайта.
// По умолчанию - испанский; доступны es / ru / en.

const SUPPORTED = ['es', 'ru', 'en']
const stored = localStorage.getItem('school_lang')
const schoolLang = ref(SUPPORTED.includes(stored) ? stored : 'es')

const dict = {
  es: {
    nav: { misCursos: 'Mis cursos', panelProfesor: 'Panel de profesor', volverSitio: '← Volver al sitio', salir: 'Salir' },
    common: { cargando: 'Cargando...', progreso: 'Progreso' },
    student: {
      panel: 'Panel de estudiante', hola: 'Hola', misCursos: 'Mis cursos',
      cargandoCursos: 'Cargando tus cursos...', sinCursos: 'Aún no tienes cursos activos.',
      verCursos: 'Ver cursos disponibles',
    },
    course: {
      sinAcceso: 'No tienes acceso a este curso.', volverCursos: '← Mis cursos',
      verVideo: 'Ver video', completar: 'Marcar como completado', descompletar: 'Marcar como no visto',
      pts: 'pts', comentarioMentor: 'Comentario del mentor:', tuRespuesta: 'Escribe tu respuesta...',
      enviar: 'Enviar respuesta', reenviar: 'Reenviar', enviando: 'Enviando...',
      adjunta: 'Adjunta un texto o un archivo.', min: 'min',
    },
    teacher: {
      panel: 'Panel de profesor', hola: 'Hola', misCursos: 'Mis cursos',
      sinCursos: 'Todavía no tienes cursos asignados.', alumnos: 'alumnos', porRevisar: 'por revisar',
      cargandoAlumnos: 'Cargando alumnos...', nadieCompro: 'Nadie ha comprado este curso todavía.',
      tareasPorRevisar: 'Tareas por revisar', sinTareas: 'No hay tareas pendientes de revisión.',
    },
    status: { submitted: 'En revisión', reviewed: 'Revisado', needs_revision: 'Devuelto' },
    statusFull: { submitted: 'Enviado, en revisión', reviewed: 'Revisado', needs_revision: 'Devuelto para corrección' },
  },
  ru: {
    nav: { misCursos: 'Мои курсы', panelProfesor: 'Кабинет преподавателя', volverSitio: '← Вернуться на сайт', salir: 'Выйти' },
    common: { cargando: 'Загрузка...', progreso: 'Прогресс' },
    student: {
      panel: 'Кабинет студента', hola: 'Привет', misCursos: 'Мои курсы',
      cargandoCursos: 'Загружаем ваши курсы...', sinCursos: 'У вас пока нет активных курсов.',
      verCursos: 'Смотреть доступные курсы',
    },
    course: {
      sinAcceso: 'У вас нет доступа к этому курсу.', volverCursos: '← Мои курсы',
      verVideo: 'Смотреть видео', completar: 'Отметить пройденным', descompletar: 'Снять отметку',
      pts: 'баллов', comentarioMentor: 'Комментарий преподавателя:', tuRespuesta: 'Напишите ваш ответ...',
      enviar: 'Отправить ответ', reenviar: 'Отправить заново', enviando: 'Отправка...',
      adjunta: 'Приложите текст или файл.', min: 'мин',
    },
    teacher: {
      panel: 'Кабинет преподавателя', hola: 'Привет', misCursos: 'Мои курсы',
      sinCursos: 'Вам пока не назначены курсы.', alumnos: 'студентов', porRevisar: 'на проверку',
      cargandoAlumnos: 'Загружаем студентов...', nadieCompro: 'Этот курс ещё никто не купил.',
      tareasPorRevisar: 'Задания на проверку', sinTareas: 'Нет заданий, ожидающих проверки.',
    },
    status: { submitted: 'На проверке', reviewed: 'Проверено', needs_revision: 'Возвращено' },
    statusFull: { submitted: 'Отправлено, на проверке', reviewed: 'Проверено', needs_revision: 'Возвращено на доработку' },
  },
  en: {
    nav: { misCursos: 'My courses', panelProfesor: 'Teacher panel', volverSitio: '← Back to site', salir: 'Log out' },
    common: { cargando: 'Loading...', progreso: 'Progress' },
    student: {
      panel: 'Student panel', hola: 'Hi', misCursos: 'My courses',
      cargandoCursos: 'Loading your courses...', sinCursos: 'You have no active courses yet.',
      verCursos: 'Browse available courses',
    },
    course: {
      sinAcceso: 'You do not have access to this course.', volverCursos: '← My courses',
      verVideo: 'Watch video', completar: 'Mark as completed', descompletar: 'Mark as not done',
      pts: 'pts', comentarioMentor: 'Mentor comment:', tuRespuesta: 'Write your answer...',
      enviar: 'Submit answer', reenviar: 'Resubmit', enviando: 'Submitting...',
      adjunta: 'Attach text or a file.', min: 'min',
    },
    teacher: {
      panel: 'Teacher panel', hola: 'Hi', misCursos: 'My courses',
      sinCursos: 'You have no assigned courses yet.', alumnos: 'students', porRevisar: 'to review',
      cargandoAlumnos: 'Loading students...', nadieCompro: 'Nobody has bought this course yet.',
      tareasPorRevisar: 'Assignments to review', sinTareas: 'No assignments pending review.',
    },
    status: { submitted: 'In review', reviewed: 'Reviewed', needs_revision: 'Returned' },
    statusFull: { submitted: 'Submitted, in review', reviewed: 'Reviewed', needs_revision: 'Returned for revision' },
  },
}

function translate(key) {
  const parts = key.split('.')
  const lookup = (langObj) => parts.reduce((acc, p) => (acc && acc[p] !== undefined ? acc[p] : undefined), langObj)
  let val = lookup(dict[schoolLang.value])
  if (val === undefined) val = lookup(dict.es) // фолбэк на испанский
  return val === undefined ? key : val
}

export function useSchoolLang() {
  const setSchoolLang = (lang) => {
    if (SUPPORTED.includes(lang)) {
      schoolLang.value = lang
      localStorage.setItem('school_lang', lang)
    }
  }
  return {
    schoolLang: readonly(schoolLang),
    supported: SUPPORTED,
    setSchoolLang,
    st: translate,
  }
}
