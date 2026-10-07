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

class StudentListSerializer(serializers.Serializer):
    """
    Строка списка учеников на /crm/students/.
    Прогресс НЕ считаем здесь (тяжело) - только кол-во курсов и флаг доступа.
    """
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    phone = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    courses_count = serializers.IntegerField()
    has_access = serializers.BooleanField()
    roles = serializers.ListField(child=serializers.CharField())


class CourseListSerializer(serializers.Serializer):
    """
    Строка списка курсов на /crm/courses/.
    Агрегаты (alumnos, completados, прогресс, pagos, ventas) считаем
    на бэке через annotate/Subquery в StudentCourseListView.
    """
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()

    has_whatsapp = serializers.BooleanField()

    students_count = serializers.IntegerField()
    completions_count = serializers.IntegerField()
    avg_progress = serializers.IntegerField()      # процент, целое 0-100
    payments_count = serializers.IntegerField()
    revenue_usd = serializers.CharField()          # строка, чтобы Decimal не терялся