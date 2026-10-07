"""
Центральный сервис отправки e-mail.

Использование:
    from notifications.services import EmailService

    EmailService.send(
        email_type='purchase',
        recipient=user,
        context={
            'nombre': user.username,
            'numero_pedido': order.order_number,
            ...
        },
        related_order=order,
    )
"""
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from .models import EmailLog

logger = logging.getLogger(__name__)


# Карта: тип письма → (тема, шаблон)
EMAIL_TEMPLATES = {
    'registration': {
        'subject': 'Bienvenido/a a MENTORED',
        'template': 'email/registration.html',
    },
    'purchase': {
        'subject': 'Confirmación de tu compra en MENTORED',
        'template': 'email/purchase.html',
    },
    'course_access': {
        'subject': 'Tu acceso al curso ya está disponible',
        'template': 'email/course_access.html',
    },
    'consultation_request': {
        'subject': 'Recibimos tu solicitud de consulta',
        'template': 'email/consultation_request.html',
    },
    'consultation_confirmed': {
        'subject': 'Tu consulta ha sido confirmada',
        'template': 'email/consultation_confirmed.html',
    },
    'consultation_reminder': {
        'subject': 'Recordatorio de tu consulta en MENTORED',
        'template': 'email/consultation_reminder.html',
    },
    'payment_failed': {
        'subject': 'Tu pago aún no fue completado',
        'template': 'email/payment_failed.html',
    },
    'admin_new_purchase': {
        'subject': 'Nueva compra en MENTORED',
        'template': 'email/admin_new_purchase.html',
    },
}


class EmailService:
    """Сервис отправки писем через Zoho SMTP"""

    @staticmethod
    def send(email_type, recipient, context=None, related_order=None,
             related_course=None, related_product=None):
        """
        Отправить письмо.

        :param email_type: тип письма (registration, purchase, ...)
        :param recipient: User | str (email)
        :param context: dict с переменными для шаблона
        :param related_order: Order (опционально)
        :param related_course: school.Course (опционально)
        :param related_product: mentored.Course (опционально)
        :return: EmailLog | None
        """
        context = context or {}

        # Определяем получателя
        if hasattr(recipient, 'email'):
            recipient_email = recipient.email
            recipient_user = recipient
        else:
            recipient_email = recipient
            recipient_user = None

        # Настройки шаблона
        template_config = EMAIL_TEMPLATES.get(email_type)
        if not template_config:
            logger.error(f"Неизвестный тип письма: {email_type}")
            return None

        subject = template_config['subject']
        template_name = template_config['template']

        # Базовый контекст (доступен во всех шаблонах)
        base_context = {
            'site_url': getattr(settings, 'FRONTEND_URL', 'https://mentoredgroup.com/'),
            'support_email': getattr(settings, 'SUPPORT_EMAIL', 'info@mentoredgroup.com'),
            'logo_url': getattr(settings, 'EMAIL_LOGO_URL', ''),
            'current_year': timezone.now().year,
        }
        base_context.update(context)

        # Создаём лог
        log = EmailLog.objects.create(
            recipient_email=recipient_email,
            recipient_user=recipient_user,
            email_type=email_type,
            subject=subject,
            related_order=related_order,
            related_course=related_course,
            related_product=related_product,
            status='pending',
        )

        try:
            # Рендерим HTML
            html_content = render_to_string(template_name, base_context)

            # Текстовая версия (fallback для старых клиентов)
            text_content = strip_tags(html_content)

            # Создаём письмо
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)

            # Обновляем лог
            log.status = 'sent'
            log.sent_at = timezone.now()
            log.save(update_fields=['status', 'sent_at'])

            logger.info(f"✅ Письмо [{email_type}] отправлено на {recipient_email}")
            return log

        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.save(update_fields=['status', 'error_message'])

            logger.exception(f"❌ Ошибка отправки [{email_type}] на {recipient_email}: {e}")
            return log

    @staticmethod
    def send_to_admins(email_type, context=None, **kwargs):
        """Отправить письмо всем админам (is_staff=True)"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        admins = User.objects.filter(is_staff=True, email__isnull=False, is_superuser=True).exclude(email='')

        for admin in admins:
            EmailService.send(
                email_type=email_type,
                recipient=admin,
                context=context,
                **kwargs,
            )