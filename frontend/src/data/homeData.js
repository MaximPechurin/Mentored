import { ref } from 'vue'

export const useHomeData = () => {
  const feelings = ref([
    {
      title: "Falta de energía",
      text: "Te sientes agotada sin saber por qué.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>`
    },
    {
      title: "Procrastinación",
      text: "Postergas lo importante una y otra vez.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg>`
    },
    {
      title: "Falta de claridad",
      text: "No sabes cuál es tu siguiente paso.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`
    },
    {
      title: "Estrés financiero",
      text: "Tu relación con el dinero te frena.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`
    },
    {
      title: "Cansancio emocional",
      text: "Sientes que das más de lo que recibes.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>`
    },
    {
      title: "Necesidad de apoyo",
      text: "Quieres acompañamiento real y profundo.",
      icon: `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`
    }
  ])

  const cycle = ref([
    { week: "Semana 1", title: "Energía", text: "Reconectamos contigo y tu propósito." },
    { week: "Semana 2", title: "Metas", text: "Alineas objetivos y creas un plan que te mueve." },
    { week: "Semana 3", title: "Dinero", text: "Transformas tu relación con el dinero y la abundancia." },
    { week: "Semana 4", title: "Relaciones", text: "Sanas vínculos y cuidas tus relaciones con claridad." }
  ])

  const founderBullets = ref([
    {
      text: "Más de 15 años de experiencia en mentoría",
      icon: `<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`
    },
    {
      text: "Miles de personas transformadas en Latinoamérica y España",
      icon: `<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`
    },
    {
      text: "Formación MBA/PHD en escuelas de prestigio internacional",
      icon: `<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`
    },
    {
      text: "Especialista en psicología clínica y organizacional",
      icon: `<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`
    }
  ])

  const testimonials = ref([
    {
      quote: "Irina tiene una claridad única para ayudarme a ver lo que realmente importa. Sus sesiones me dieron dirección y paz.",
      name: "María G.",
      role: "Emprendedora",
      initial: "M"
    },
    {
      quote: "Su acompañamiento es profundo, humano y estratégico. Me ayudó a transformar mi vida y mi negocio.",
      name: "Carlos R.",
      role: "Consultor",
      initial: "C"
    },
    {
      quote: "Gracias a Irina volví a confiar en mí y tomé decisiones que cambiaron mi camino.",
      name: "Lucía P.",
      role: "Directora de Marketing",
      initial: "L"
    }
  ])

  return {
    feelings,
    cycle,
    founderBullets,
    testimonials
  }
}