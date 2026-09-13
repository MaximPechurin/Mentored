import DOMPurify from 'dompurify'

// Текст урока исторически хранился как обычный текст (plain text), а с
// появлением визуального редактора - как HTML. Чтобы старые уроки
// отображались ровно как раньше, а новые - с форматированием, различаем
// эти два случая по наличию HTML-тегов.
const HTML_RE = /<\/?[a-z][\s\S]*>/i

export function isHtmlContent(content) {
  return !!content && HTML_RE.test(content)
}

// Безопасный HTML для вставки через v-html. Разрешаем только
// форматирование, которое умеет наш редактор (Quill), + картинки со
// ссылкой; скрипты/обработчики событий DOMPurify вырезает.
export function sanitizeLessonHtml(content) {
  return DOMPurify.sanitize(content || '', {
    ALLOWED_TAGS: [
      'p', 'br', 'span', 'strong', 'b', 'em', 'i', 'u', 's', 'blockquote',
      'h1', 'h2', 'h3', 'h4', 'ol', 'ul', 'li', 'a', 'img',
    ],
    ALLOWED_ATTR: ['href', 'target', 'rel', 'src', 'alt', 'class', 'style'],
    ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto|tel):|[^a-z]|[a-z+.-]+(?:[^a-z+.:-]|$))/i,
  })
}
