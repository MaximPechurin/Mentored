from rest_framework import serializers


class CounterSerializer(serializers.Serializer):
    """
    Счётчики для верхнего ряда карточек дашборда.
    Все поля — int, кроме revenue_usd_30d (строка, т.к. Decimal).
    """
    students_active = serializers.IntegerField()
    students_total = serializers.IntegerField()
    courses_active = serializers.IntegerField()
    teachers = serializers.IntegerField()
    orders_paid_30d = serializers.IntegerField()
    revenue_usd_30d = serializers.CharField()
    contact_messages_unread = serializers.IntegerField()
    submissions_pending = serializers.IntegerField()


class RecentPaymentSerializer(serializers.Serializer):
    """Строка блока 'Последние оплаты'."""
    id = serializers.IntegerField()
    order_number = serializers.CharField()
    user_email = serializers.EmailField()
    user_name = serializers.CharField()
    amount = serializers.CharField()
    currency = serializers.CharField()
    status = serializers.CharField()
    status_display = serializers.CharField()
    paid_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()


class RecentRegistrationSerializer(serializers.Serializer):
    """Строка блока 'Последние регистрации'."""
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    phone = serializers.CharField(allow_null=True)
    roles = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField()


class RecentContactMessageSerializer(serializers.Serializer):
    """Строка блока 'Свежие заявки'."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    motivo = serializers.CharField()
    message_preview = serializers.CharField()
    is_read = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class DashboardSerializer(serializers.Serializer):
    """
    Ответ GET /api/crm/dashboard/.
    Всё, что нужно главному экрану CRM — одним запросом.
    """
    counters = CounterSerializer()
    recent_payments = RecentPaymentSerializer(many=True)
    recent_registrations = RecentRegistrationSerializer(many=True)
    recent_contact_messages = RecentContactMessageSerializer(many=True)