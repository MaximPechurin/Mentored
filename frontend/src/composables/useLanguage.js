import { ref, computed, readonly } from 'vue'

// Загружаем язык из localStorage или используем 'es' по умолчанию
const storedLang = localStorage.getItem('lang') || 'es'
const currentLang = ref(storedLang)

// Словари переводов
const translations = {
  es: {
    nav: {
      cursos: 'Cursos',
      consultas: 'Consultas',
      expertos: 'Expertos',
      tienda: 'Tienda',
      comunidad: 'Comunidad',
      gratis: 'Gratis',
      blog: 'Blog',
      contacto: 'Contacto',
      test: 'Hacer el test',
      carrito: 'Carrito',
      cuenta: 'Cuenta'
    },
    hero: {
      tag: 'Bienvenida a Mentored',
      title: {
        part1: 'Transforma tu vida con',
        part2: 'claridad',
        part3: 'energía',
        part4: 'y propósito'
      },
      sub: 'Cursos, consultas, libros y comunidad para tu crecimiento personal y profesional.',
      quote: '«No se trata de hacerlo perfecto. Se trata de volver a ti y avanzar.»',
      btnPrimary: 'Empezar aquí',
      btnSecondary: 'Hacer el test'
    },
  },
  ru: {
    nav: {
      cursos: 'Курсы',
      consultas: 'Консультации',
      expertos: 'Эксперты',
      tienda: 'Магазин',
      comunidad: 'Сообщество',
      gratis: 'Бесплатно',
      blog: 'Блог',
      contacto: 'Контакты',
      test: 'Пройти тест',
      carrito: 'Корзина',
      cuenta: 'Аккаунт'
    },
    hero: {
      tag: 'Добро пожаловать в Mentored',
      title: {
        part1: 'Трансформируй свою жизнь с',
        part2: 'ясностью',
        part3: 'энергией',
        part4: 'и целью'
      },
      sub: 'Курсы, консультации, книги и сообщество для твоего личностного и профессионального роста.',
      quote: '«Дело не в том, чтобы сделать всё идеально. Дело в том, чтобы вернуться к себе и двигаться вперёд.»',
      btnPrimary: 'Начать здесь',
      btnSecondary: 'Пройти тест'
    }
  }
}

// Функция для получения перевода
const t = (key) => {
  const keys = key.split('.')
  let result = translations[currentLang.value]

  for (const k of keys) {
    if (result && result[k] !== undefined) {
      result = result[k]
    } else {
      console.warn(`Translation missing for key: ${key}`)
      return key
    }
  }

  return result
}

export function useLanguage() {
  const setLanguage = (lang) => {
    if (lang === 'es' || lang === 'ru') {
      currentLang.value = lang
      localStorage.setItem('lang', lang)
    }
  }

  const isSpanish = computed(() => currentLang.value === 'es')
  const isRussian = computed(() => currentLang.value === 'ru')

  return {
    currentLang: readonly(currentLang),
    setLanguage,
    isSpanish,
    isRussian,
    t
  }
}