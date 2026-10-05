from django.db import models
from django.conf import settings


class EmailLog(models.Model):
    """Журнал всех отправленных писем"""

    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка отправки'),
    ]

    # Кому
    recipient_email = models.EmailField(verbose_name='Email получателя')
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
        verbose_name='Пользователь',
    )

    # Что за письмо
    email_type = models.CharField(
        max_length=50,
        verbose_name='Тип письма',
        help_text='registration, purchase, course_access, consultation_request, '
                  'consultation_confirmed, consultation_reminder, payment_failed, '
                  'admin_new_purchase',
    )
    subject = models.CharField(max_length=255, verbose_name='Тема')

    # Связи (для контекста)
    related_order = models.ForeignKey(
        'mentored.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
        verbose_name='Заказ',
    )
    related_course = models.ForeignKey(
        'school.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
        verbose_name='Курс',
    )
    related_product = models.ForeignKey(
        'mentored.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
        verbose_name='Товар (витрина)',
    )

    # Статус
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус',
    )
    error_message = models.TextField(
        blank=True,
        verbose_name='Текст ошибки',
    )

    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Лог письма'
        verbose_name_plural = 'Журнал писем'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email_type', 'status']),
            models.Index(fields=['recipient_email']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.email_type} → {self.recipient_email}"


class EmailTemplate(models.Model):
    """Редактируемые шаблоны писем (опционально — можно редактировать из админки)"""
    code = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Код шаблона',
        help_text='registration, purchase, course_access и т.д.',
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    subject = models.CharField(max_length=255, verbose_name='Тема (по умолчанию)')
    html_body = models.TextField(
        verbose_name='HTML-тело',
        help_text='Поддерживает переменные: {{ nombre }}, {{ numero_pedido }} и т.д.',
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Шаблон письма'
        verbose_name_plural = 'Шаблоны писем'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.name}"