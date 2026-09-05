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
    nav: { misCursos: 'Mis cursos', panelProfesor: 'Panel de profesor', foros: 'Foros', volverSitio: '← Volver al sitio', salir: 'Salir' },
    common: { cargando: 'Cargando...', progreso: 'Progreso', volver: '← Volver' },
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
    leccion: {
      deMateriales: 'de', materiales: 'materiales', anterior: '← Material anterior',
      siguiente: 'Material siguiente →', tarea: 'Tarea', tuRespuestaTitulo: 'Tu respuesta',
      respuestas: 'Respuestas y comentarios', sinRespuestas: 'Aún no hay respuestas visibles.',
      viejasPrimero: 'antiguas primero', nuevasPrimero: 'nuevas primero',
      soloYo: 'Solo tú y el profesor ven esta respuesta', visibleTodos: 'Visible para todos los alumnos',
      hacerVisible: 'Hacer visible para todos', hacerPrivada: 'Ocultar de otros alumnos',
      comentar: 'Añadir un comentario...', enviarComentario: 'Comentar',
      tareaHecha: 'Tarea completada', tareaPendiente: 'Tarea pendiente', tú: 'Tú',
      completaTareaPrimero: 'Envía tu tarea para poder marcar esta lección como completada.',
    },
    teacher: {
      panel: 'Panel de profesor', hola: 'Hola', misCursos: 'Mis cursos',
      sinCursos: 'Todavía no tienes cursos asignados.', alumnos: 'alumnos', porRevisar: 'por revisar',
      cargandoAlumnos: 'Cargando alumnos...', nadieCompro: 'Nadie ha comprado este curso todavía.',
      tareasPorRevisar: 'Tareas por revisar', sinTareas: 'No hay tareas pendientes de revisión.',
      respuestaAlumno: 'Respuesta del alumno', archivoAdjunto: 'Archivo adjunto', verArchivo: 'Ver archivo',
      sinTexto: '(sin texto)', calificacion: 'Calificación', comentario: 'Comentario (opcional)',
      marcarRevisado: 'Aprobar', devolver: 'Devolver para corrección', guardando: 'Guardando...',
      revisado: '¡Revisado!', progresoAlumno: 'Progreso del alumno',
      tareasTitulo: 'Tareas', tareasCount: 'tareas', hechas: 'hechas',
      sinAsignaciones: 'Este curso aún no tiene tareas.',
    },
    status: { not_submitted: 'No entregada', submitted: 'En revisión', reviewed: 'Revisado', needs_revision: 'Devuelto' },
    statusFull: { submitted: 'Enviado, en revisión', reviewed: 'Revisado', needs_revision: 'Devuelto para corrección' },
    chat: { title: 'Mensajes', placeholder: 'Escribe un mensaje...', send: 'Enviar', empty: 'Aún no hay mensajes.', noChats: 'No hay chats disponibles.', back: '← Atrás' },
    foro: {
      title: 'Foro del curso', open: 'Foro', back: '← Al curso', backThreads: '← Temas',
      newThread: 'Nueva tema', threadTitle: 'Título de la tema', message: 'Mensaje',
      create: 'Crear tema', reply: 'Responder', empty: 'Todavía no hay temas. ¡Crea la primera!',
      noPosts: 'Sin mensajes.', locked: 'Tema cerrada', teacher: 'Profesor',
      pin: 'Fijar', unpin: 'Desfijar', lock: 'Cerrar', unlock: 'Abrir', pinned: '📌 Fijada',
      writeReply: 'Escribe una respuesta...', posts: 'mensajes',
      subtitulo: 'Preguntas y comunidad del curso',
      listaTitle: 'Foros de mis cursos', listaSub: 'Elige el curso para entrar a su foro',
      sinForos: 'No tienes cursos con foro todavía.', temas: 'temas', profe: 'profesor',
    },
    stats: {
      title: 'Analítica', avgProgress: 'Progreso medio', completed: 'Completado',
      inProgress: 'En curso', notStarted: 'Sin empezar', students: 'Alumnos',
      submissions: 'Tareas', pending: 'por revisar', reviewed: 'revisadas',
      platform: 'Analítica de la plataforma', activeCourses: 'Cursos activos',
      activeStudents: 'Alumnos activos', teachers: 'Profesores', enrollments: 'Accesos',
      avgCompletion: 'Finalización media', forumThreads: 'Temas del foro',
    },
  },
  ru: {
    nav: { misCursos: 'Мои курсы', panelProfesor: 'Кабинет преподавателя', foros: 'Форумы', volverSitio: '← Вернуться на сайт', salir: 'Выйти' },
    common: { cargando: 'Загрузка...', progreso: 'Прогресс', volver: '← Назад' },
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
    leccion: {
      deMateriales: 'из', materiales: 'материалов', anterior: '← Предыдущий материал',
      siguiente: 'Следующий материал →', tarea: 'Задание', tuRespuestaTitulo: 'Ваш ответ',
      respuestas: 'Ответы и комментарии', sinRespuestas: 'Открытых ответов пока нет.',
      viejasPrimero: 'старые сначала', nuevasPrimero: 'новые сначала',
      soloYo: 'Ответ видите только вы и преподаватель', visibleTodos: 'Виден всем ученикам',
      hacerVisible: 'Сделать видимым для всех', hacerPrivada: 'Скрыть от других учеников',
      comentar: 'Добавить комментарий...', enviarComentario: 'Отправить',
      tareaHecha: 'Задание выполнено', tareaPendiente: 'Задание не выполнено', tú: 'Вы',
      completaTareaPrimero: 'Сначала отправьте домашнее задание, чтобы отметить урок пройденным.',
    },
    teacher: {
      panel: 'Кабинет преподавателя', hola: 'Привет', misCursos: 'Мои курсы',
      sinCursos: 'Вам пока не назначены курсы.', alumnos: 'студентов', porRevisar: 'на проверку',
      cargandoAlumnos: 'Загружаем студентов...', nadieCompro: 'Этот курс ещё никто не купил.',
      tareasPorRevisar: 'Задания на проверку', sinTareas: 'Нет заданий, ожидающих проверки.',
      respuestaAlumno: 'Ответ студента', archivoAdjunto: 'Прикреплённый файл', verArchivo: 'Открыть файл',
      sinTexto: '(без текста)', calificacion: 'Оценка', comentario: 'Комментарий (необязательно)',
      marcarRevisado: 'Принять', devolver: 'Вернуть на доработку', guardando: 'Сохранение...',
      revisado: 'Проверено!', progresoAlumno: 'Прогресс студента',
      tareasTitulo: 'Домашние задания', tareasCount: 'заданий', hechas: 'выполнено',
      sinAsignaciones: 'В этом курсе пока нет заданий.',
    },
    status: { not_submitted: 'Не выполнено', submitted: 'На проверке', reviewed: 'Проверено', needs_revision: 'Возвращено' },
    statusFull: { submitted: 'Отправлено, на проверке', reviewed: 'Проверено', needs_revision: 'Возвращено на доработку' },
    chat: { title: 'Сообщения', placeholder: 'Напишите сообщение...', send: 'Отправить', empty: 'Пока нет сообщений.', noChats: 'Нет доступных чатов.', back: '← Назад' },
    foro: {
      title: 'Форум курса', open: 'Форум', back: '← К курсу', backThreads: '← Темы',
      newThread: 'Новая тема', threadTitle: 'Заголовок темы', message: 'Сообщение',
      create: 'Создать тему', reply: 'Ответить', empty: 'Тем пока нет. Создайте первую!',
      noPosts: 'Нет сообщений.', locked: 'Тема закрыта', teacher: 'Преподаватель',
      pin: 'Закрепить', unpin: 'Открепить', lock: 'Закрыть', unlock: 'Открыть', pinned: '📌 Закреплена',
      writeReply: 'Напишите ответ...', posts: 'сообщений',
      subtitulo: 'Вопросы и общение по курсу',
      listaTitle: 'Форумы моих курсов', listaSub: 'Выберите курс, чтобы перейти в его форум',
      sinForos: 'У вас пока нет курсов с форумом.', temas: 'тем', profe: 'преподаватель',
    },
    stats: {
      title: 'Аналитика', avgProgress: 'Средний прогресс', completed: 'Завершили',
      inProgress: 'В процессе', notStarted: 'Не начали', students: 'Студентов',
      submissions: 'Домашки', pending: 'на проверку', reviewed: 'проверено',
      platform: 'Аналитика платформы', activeCourses: 'Активных курсов',
      activeStudents: 'Активных студентов', teachers: 'Преподавателей', enrollments: 'Доступов',
      avgCompletion: 'Средняя завершаемость', forumThreads: 'Тем на форуме',
    },
  },
  en: {
    nav: { misCursos: 'My courses', panelProfesor: 'Teacher panel', foros: 'Forums', volverSitio: '← Back to site', salir: 'Log out' },
    common: { cargando: 'Loading...', progreso: 'Progress', volver: '← Back' },
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
    leccion: {
      deMateriales: 'of', materiales: 'materials', anterior: '← Previous material',
      siguiente: 'Next material →', tarea: 'Assignment', tuRespuestaTitulo: 'Your answer',
      respuestas: 'Answers and comments', sinRespuestas: 'No visible answers yet.',
      viejasPrimero: 'oldest first', nuevasPrimero: 'newest first',
      soloYo: 'Only you and the teacher can see this answer', visibleTodos: 'Visible to all students',
      hacerVisible: 'Make visible to everyone', hacerPrivada: 'Hide from other students',
      comentar: 'Add a comment...', enviarComentario: 'Send',
      tareaHecha: 'Assignment completed', tareaPendiente: 'Assignment pending', tú: 'You',
      completaTareaPrimero: 'Submit your assignment to mark this lesson as completed.',
    },
    teacher: {
      panel: 'Teacher panel', hola: 'Hi', misCursos: 'My courses',
      sinCursos: 'You have no assigned courses yet.', alumnos: 'students', porRevisar: 'to review',
      cargandoAlumnos: 'Loading students...', nadieCompro: 'Nobody has bought this course yet.',
      tareasPorRevisar: 'Assignments to review', sinTareas: 'No assignments pending review.',
      respuestaAlumno: 'Student answer', archivoAdjunto: 'Attached file', verArchivo: 'Open file',
      sinTexto: '(no text)', calificacion: 'Grade', comentario: 'Comment (optional)',
      marcarRevisado: 'Approve', devolver: 'Return for revision', guardando: 'Saving...',
      revisado: 'Reviewed!', progresoAlumno: 'Student progress',
      tareasTitulo: 'Homework', tareasCount: 'assignments', hechas: 'done',
      sinAsignaciones: 'This course has no assignments yet.',
    },
    status: { not_submitted: 'Not submitted', submitted: 'In review', reviewed: 'Reviewed', needs_revision: 'Returned' },
    statusFull: { submitted: 'Submitted, in review', reviewed: 'Reviewed', needs_revision: 'Returned for revision' },
    chat: { title: 'Messages', placeholder: 'Write a message...', send: 'Send', empty: 'No messages yet.', noChats: 'No chats available.', back: '← Back' },
    foro: {
      title: 'Course forum', open: 'Forum', back: '← To course', backThreads: '← Threads',
      newThread: 'New thread', threadTitle: 'Thread title', message: 'Message',
      create: 'Create thread', reply: 'Reply', empty: 'No threads yet. Create the first one!',
      noPosts: 'No messages.', locked: 'Thread closed', teacher: 'Teacher',
      pin: 'Pin', unpin: 'Unpin', lock: 'Close', unlock: 'Open', pinned: '📌 Pinned',
      writeReply: 'Write a reply...', posts: 'messages',
      subtitulo: 'Questions and course community',
      listaTitle: 'My course forums', listaSub: 'Pick a course to open its forum',
      sinForos: 'You have no courses with a forum yet.', temas: 'threads', profe: 'teacher',
    },
    stats: {
      title: 'Analytics', avgProgress: 'Avg. progress', completed: 'Completed',
      inProgress: 'In progress', notStarted: 'Not started', students: 'Students',
      submissions: 'Homework', pending: 'to review', reviewed: 'reviewed',
      platform: 'Platform analytics', activeCourses: 'Active courses',
      activeStudents: 'Active students', teachers: 'Teachers', enrollments: 'Enrollments',
      avgCompletion: 'Avg. completion', forumThreads: 'Forum threads',
    },
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
