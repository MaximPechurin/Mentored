<template>
  <div class="lg-body">
    <div v-if="tab === 'info'">
      <p class="lg-updated">Última actualización: 1 de junio de 2026</p>

      <h2 class="lg-h2">Titularidad del sitio</h2>
      <p class="lg-p">
        El presente sitio web y la plataforma Mentored son operados por <strong>Mentored</strong>, dedicada a la formación, las consultas individuales y el acompañamiento en crecimiento personal y profesional. El acceso y uso del sitio implican la aceptación de las condiciones recogidas en este aviso.
      </p>

      <h2 class="lg-h2">Datos de contacto</h2>
      <ul class="lg-contact">
        <li><strong>Correo electrónico:</strong> <a href="mailto:hola@mentored.com">hola@mentored.com</a></li>
        <li><strong>WhatsApp:</strong> <a href="https://wa.me/51940304595">+51 940 304 595</a></li>
      </ul>

      <h2 class="lg-h2">Propiedad intelectual</h2>
      <p class="lg-p">
        Todos los contenidos del sitio —textos, cursos, materiales descargables, imágenes, logotipos y diseño— son titularidad de Mentored o de sus legítimos autores, y están protegidos por la normativa de propiedad intelectual. Queda prohibida su reproducción, distribución o comunicación pública sin autorización expresa.
      </p>
      <p class="lg-p">
        El acceso a los cursos y materiales adquiridos es de uso personal e intransferible. No está permitido compartir credenciales ni redistribuir el contenido.
      </p>

      <h2 class="lg-h2">Responsabilidad</h2>
      <p class="lg-p">
        Los contenidos de Mentored tienen carácter formativo e informativo y no sustituyen el asesoramiento médico, psicológico o jurídico profesional. Mentored no garantiza resultados concretos, que dependen del compromiso y las circunstancias de cada persona.
      </p>

      <h2 class="lg-h2">Legislación aplicable</h2>
      <p class="lg-p">
        Cualquier controversia derivada del uso del sitio se regirá por la legislación aplicable y se someterá a los tribunales competentes del domicilio de Mentored, salvo que la normativa de consumo disponga otra cosa.
      </p>
    </div>

    <div v-else-if="tab === 'oferta'">
      <p class="lg-updated">Última actualización: 1 de junio de 2026</p>

      <h2 class="lg-h2">Objeto de la oferta</h2>
      <p class="lg-p">
        Este documento constituye una oferta pública dirigida a cualquier persona (el «Usuario») para la adquisición de los productos y servicios ofrecidos por Mentored: cursos digitales, libros, consultas individuales y membresías de comunidad. La realización de un pedido supone la aceptación plena de las presentes condiciones.
      </p>

      <h2 class="lg-h2">Productos y servicios</h2>
      <ul class="lg-list">
        <li><strong>Cursos y materiales digitales:</strong> acceso en línea tras la confirmación del pago, según las condiciones de cada producto.</li>
        <li><strong>Consultas individuales:</strong> sesiones programadas con un experto, en la fecha y hora acordadas.</li>
        <li><strong>Membresías:</strong> acceso a la comunidad y a los recursos durante el periodo contratado.</li>
      </ul>

      <h2 class="lg-h2">Precios y pago</h2>
      <p class="lg-p">
        Los precios figuran en cada ficha de producto e incluyen los impuestos aplicables salvo indicación contraria. El pago se realiza a través de los medios habilitados en el sitio. El acceso al producto o servicio se activa una vez confirmado el pago.
      </p>

      <h2 class="lg-h2">Obligaciones del usuario</h2>
      <p class="lg-p">
        El Usuario se compromete a facilitar datos veraces, a utilizar los contenidos de forma personal y a no compartir, copiar ni redistribuir los materiales. El incumplimiento puede suponer la suspensión del acceso sin derecho a reembolso.
      </p>

      <h2 class="lg-h2">Vigencia y modificaciones</h2>
      <p class="lg-p">
        Mentored podrá actualizar estas condiciones y su catálogo en cualquier momento. Las condiciones aplicables serán las vigentes en el momento de realizar el pedido. Las cuestiones de devolución se rigen por la sección <router-link to="/compras">Condiciones de compra y devoluciones</router-link>.
      </p>
    </div>

    <div v-else-if="tab === 'privacidad'">
      <p class="lg-updated">Última actualización: 1 de junio de 2026</p>

      <h2 class="lg-h2">Responsable del tratamiento</h2>
      <p class="lg-p">
        Mentored es responsable del tratamiento de los datos personales que nos facilitas a través del sitio. Tratamos tus datos con confidencialidad y solo para las finalidades descritas en esta política.
      </p>

      <h2 class="lg-h2">Datos que recogemos</h2>
      <ul class="lg-list">
        <li>Datos de identificación y contacto (nombre, correo electrónico, teléfono).</li>
        <li>Datos de compra y facturación necesarios para gestionar tus pedidos.</li>
        <li>Datos de navegación y uso del sitio, mediante cookies y tecnologías similares.</li>
      </ul>

      <h2 class="lg-h2">Finalidad y base legal</h2>
      <p class="lg-p">
        Utilizamos tus datos para gestionar tu cuenta y tus compras, prestar los servicios contratados, atender tus consultas y, si lo autorizas, enviarte comunicaciones e información sobre nuestros recursos. La base legal es la ejecución del contrato, el cumplimiento de obligaciones legales y tu consentimiento.
      </p>

      <h2 class="lg-h2">Conservación y cesión</h2>
      <p class="lg-p">
        Conservamos tus datos mientras mantengas tu cuenta o sean necesarios para las finalidades indicadas y para cumplir obligaciones legales. No cedemos tus datos a terceros, salvo a los proveedores que nos ayudan a prestar el servicio (pagos, alojamiento, correo) y siempre con las debidas garantías.
      </p>

      <h2 class="lg-h2">Tus derechos</h2>
      <p class="lg-p">
        Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <a href="mailto:hola@mentored.com">hola@mentored.com</a>. También puedes retirar tu consentimiento en cualquier momento y presentar una reclamación ante la autoridad de control competente.
      </p>

      <h2 class="lg-h2">Cookies</h2>
      <p class="lg-p">
        Usamos cookies técnicas necesarias para el funcionamiento del sitio y, con tu consentimiento, cookies analíticas para mejorar la experiencia. Puedes configurar tu navegador para gestionarlas o bloquearlas.
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  tab: {
    type: String,
    default: 'info'
  }
})
</script>

<style scoped>
.lg-body {
  max-width: 920px;
  margin: 0 auto;
  padding: 64px 32px 96px;
}

.lg-updated {
  font-size: 14px;
  color: #a59c93;
  margin: 0 0 32px;
}

.lg-h2 {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  color: #15110f;
  margin: 40px 0 16px;
  letter-spacing: -0.3px;
}

.lg-h2:first-of-type {
  margin-top: 0;
}

.lg-p {
  font-size: 17px;
  line-height: 1.75;
  color: #5d544c;
  margin: 0 0 18px;
}

.lg-p:last-child {
  margin-bottom: 0;
}

.lg-p strong {
  font-weight: 600;
  color: #15110f;
}

.lg-contact {
  list-style: none;
  margin: 0 0 28px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.lg-contact li {
  font-size: 17px;
  line-height: 1.6;
  color: #5d544c;
}

.lg-contact li strong {
  font-weight: 600;
  color: #15110f;
}

.lg-contact li a {
  color: #8e1519;
  text-decoration: none;
}

.lg-contact li a:hover {
  text-decoration: underline;
}

.lg-list {
  margin: 0 0 28px;
  padding-left: 22px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.lg-list li {
  font-size: 17px;
  line-height: 1.7;
  color: #5d544c;
}

.lg-list li strong {
  font-weight: 600;
  color: #15110f;
}

.lg-body a {
  color: #8e1519;
  text-decoration: none;
}

.lg-body a:hover {
  text-decoration: underline;
}

@media (max-width: 860px) {
  .lg-body { padding: 48px 20px 72px !important; }
  .lg-body h2 { font-size: 25px !important; }
}
</style>