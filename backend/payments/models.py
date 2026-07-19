from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('approved', 'Оплачен'),
        ('rejected', 'Отклонён'),
        ('cancelled', 'Отменён'),
        ('refunded', 'Возвращён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    order = models.OneToOneField(
        'mentored.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment',
        verbose_name='Заказ'
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ID транзакции'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Способ оплаты'
    )
    payment_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Ответ от платежной системы'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f"Платёж #{self.id} - {self.user.email} - {self.status}"