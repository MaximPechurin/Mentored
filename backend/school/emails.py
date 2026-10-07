"""
Email-уведомления школы. Все отправки best-effort (как в
ContactMessageView Этапа 1): SMTP не настроен или упал - пишем в лог и
живём дальше, основную операцию (оплату/ревью) никогда не роняем.

Тексты на испанском - язык аудитории платформы.

ВАЖНО (история): письмо "доступ к курсу" раньше слалось простым
send_mail() с plain-text прямо отсюда - это дублировало наш общий
EmailService и не попадало в журнал EmailLog. Теперь оно уходит через
EmailService (HTML-шаблон, лог в админке, единый стиль MENTORED).
Письмо "работа проверена" пока оставлено как было - для него нет
отдельного HTML-шаблона в ТЗ, при необходимости переведём позже.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

from notifications.services import EmailService

logger = logging.getLogger(__name__)

SITE_URL = 'https://www.mentoredgroup.com'


def _send(subject, message, recipient):
    """ Устаревший helper для plain-text писем (оставлен для send_submission_reviewed). """
    if not settings.EMAIL_HOST_USER:
        logger.warning(
            "EMAIL_HOST_USER не настроен - письмо '%s' для %s не отправлено.",
            subject, recipient,
        )
        return
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Не удалось отправить письмо '%s' для %s", subject, recipient)


def send_course_access_granted(user, course):
    """
    Доступ к курсу открыт (после оплаты или вручную из админки).

    Уходит через общий EmailService: HTML-шаблон emails/course_access.html,
    лог в EmailLog, единый стиль MENTORED.
    """
    #name = user.username or user.email
    #_send(
    #    subject=f'¡Ya tienes acceso al curso «{course.title}»!',
    #    message=(
    #        f'Hola {name},\n\n'
    #        f'Tu acceso al curso «{course.title}» ya está activo.\n'
    #        f'Puedes empezar cuando quieras desde tu panel de estudiante:\n'
    #        f'{SITE_URL}/escuela/estudiante\n\n'
    #        f'¡Buen aprendizaje!\n'
    #        f'Equipo Mentored'
    #    ),
    #    recipient=user.email,
    #)

    EmailService.send(
        email_type='course_access',
        recipient=user,
        context={
            'nombre': user.username or user.email,
            'nombre_curso': course.title,
            'link_curso': f'{SITE_URL}/escuela/curso/{course.slug}',
        },
        related_course=course,
    )


def send_submission_reviewed(submission):
    """
    Домашняя работа проверена ментором (reviewed / needs_revision).

    Пока остаётся plain-text через send_mail() - отдельного HTML-шаблона
    для этого письма в ТЗ нет.
    """
    user = submission.enrollment.user
    name = user.username or user.email
    assignment = submission.assignment
    course = assignment.lesson.module.course

    if submission.status == 'needs_revision':
        headline = 'Tu tarea fue devuelta para corrección'
    else:
        headline = 'Tu tarea fue revisada'

    score_line = ''
    if submission.score is not None:
        score_line = f'Calificación: {submission.score}/{assignment.max_score}\n'

    comment_line = ''
    if submission.mentor_comment:
        comment_line = f'Comentario del mentor:\n{submission.mentor_comment}\n\n'

    _send(
        subject=f'{headline}: «{assignment.title}»',
        message=(
            f'Hola {name},\n\n'
            f'{headline}.\n'
            f'Curso: {course.title}\n'
            f'Tarea: {assignment.title}\n'
            f'{score_line}\n'
            f'{comment_line}'
            f'Ver detalles en tu panel: {SITE_URL}/escuela/curso/{course.slug}\n\n'
            f'Equipo Mentored'
        ),
        recipient=user.email,
    )
