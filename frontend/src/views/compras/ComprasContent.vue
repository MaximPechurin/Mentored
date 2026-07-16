<template>
  <div class="cp-body">
    <!-- Pagos -->
    <h2 class="cp-h2">Pagos</h2>
    <p class="cp-p">
      Los precios indicados en cada producto incluyen los impuestos aplicables salvo que se indique lo contrario. Aceptamos los medios de pago habilitados en el checkout. El acceso al producto o la confirmación de la consulta se activan una vez recibido el pago. Recibirás un comprobante por correo electrónico.
    </p>

    <!-- Garantía -->
    <div class="cp-garantia">
      <h2 class="cp-garantia-title">Garantía de 14 días</h2>
      <p class="cp-garantia-text">
        Si un curso o libro digital no es lo que esperabas, dispones de <strong>14 días naturales</strong> desde la compra para solicitar el reembolso, siempre que no hayas completado más del 30% del contenido.
      </p>
    </div>

    <!-- Política de devoluciones -->
    <h2 class="cp-h2">Política de devoluciones</h2>
    <p class="cp-p">
      Queremos que compres con confianza. Las condiciones de reembolso varían según el tipo de producto:
    </p>
    <ul class="cp-list">
      <li>
        <strong>Cursos y libros digitales:</strong> reembolso completo dentro de los 14 días si no se ha consumido más del 30% del contenido.
      </li>
      <li>
        <strong>Consultas individuales:</strong> puedes reprogramar o cancelar con reembolso hasta 48 horas antes de la sesión. Después de ese plazo, la sesión no es reembolsable.
      </li>
      <li>
        <strong>Membresías:</strong> puedes cancelar la renovación en cualquier momento; el acceso se mantiene hasta el final del periodo ya pagado, sin reembolso del periodo en curso.
      </li>
    </ul>
    <p class="cp-p">
      No se admiten devoluciones de productos personalizados ni de sesiones ya realizadas.
    </p>

    <!-- Cómo solicitar reembolso -->
    <h2 class="cp-h2">Cómo solicitar un reembolso</h2>
    <p class="cp-p">
      Escríbenos a <a href="mailto:hola@mentored.com" class="cp-link">hola@mentored.com</a> o por <a href="https://wa.me/0000000000" class="cp-link">WhatsApp</a> indicando tu número de pedido y el motivo. Revisaremos tu solicitud y, si procede, gestionaremos el reembolso por el mismo medio de pago en un plazo de hasta 14 días.
    </p>

    <!-- Botones de contacto -->
    <div class="cp-buttons">
      <a href="mailto:hola@mentored.com" class="cp-btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <path d="m22 7-10 6L2 7"/>
        </svg>
        Escribir por correo
      </a>
      <a href="https://wa.me/0000000000" class="cp-btn-secondary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
        </svg>
        WhatsApp
      </a>
    </div>
  </div>
</template>

<style scoped>
.cp-body {
  max-width: 920px;
  margin: 0 auto;
  padding: 48px 32px 96px;
}

.cp-h2 {
  font-family: 'Playfair Display', serif;
  font-size: 30px;
  font-weight: 600;
  color: #15110f;
  margin: 40px 0 16px;
  letter-spacing: -0.3px;
}

.cp-h2:first-of-type {
  margin-top: 0;
}

.cp-p {
  font-size: 17px;
  line-height: 1.75;
  color: #5d544c;
  margin: 0 0 18px;
}

.cp-p:last-child {
  margin-bottom: 0;
}

.cp-link {
  color: #8e1519;
  text-decoration: none;
}

.cp-link:hover {
  text-decoration: underline;
}

.cp-garantia {
  background: #0e0c0c;
  border-radius: 20px;
  padding: 34px;
  margin: 44px 0;
}

.cp-garantia-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 12px;
  letter-spacing: -0.3px;
}

.cp-garantia-text {
  font-size: 17px;
  line-height: 1.7;
  color: #cfc7be;
  margin: 0;
}

.cp-garantia-text strong {
  color: #fff;
  font-weight: 600;
}

.cp-list {
  margin: 0 0 18px;
  padding-left: 22px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cp-list li {
  font-size: 17px;
  line-height: 1.7;
  color: #5d544c;
}

.cp-list li strong {
  font-weight: 600;
  color: #15110f;
}

.cp-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 28px;
}

.cp-btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  background: #8e1519;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  padding: 14px 26px;
  border-radius: 999px;
  transition: background 0.3s;
}

.cp-btn-primary:hover {
  background: #a01a1f;
}

.cp-btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  border: 1.5px solid #8e1519;
  color: #8e1519;
  font-weight: 600;
  font-size: 16px;
  padding: 13px 26px;
  border-radius: 999px;
  transition: all 0.3s;
}

.cp-btn-secondary:hover {
  background: #8e1519;
  color: #fff;
}

@media (max-width: 860px) {
  .cp-body { padding: 48px 20px 80px !important; }
  .cp-body h2 { font-size: 26px !important; }
}
</style>