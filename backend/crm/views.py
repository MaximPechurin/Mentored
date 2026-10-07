from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from mentored.models import ContactMessage, Order, Payment, Role
from school.models import Course, Enrollment, LessonProgress, Submission

from .permissions import IsSuperuser

User = get_user_model()


class DashboardView(APIView):
    """
    GET /api/crm/dashboard/

    Отдаёт всё для главного экрана CRM одним запросом: счётчики,
    последние оплаты, регистрации, заявки с формы.

    Только is_superuser (по ТЗ 'руководитель проекта').
    """
    permission_classes = [IsSuperuser]

    def get(self, request):
        now = timezone.now()
        month_ago = now - timedelta(days=30)

        # ---------- Счётчики ----------
        students_active_qs = Enrollment.objects.filter(is_active=True).values('user_id').distinct()
        students_active = students_active_qs.count()
        students_total = User.objects.filter(is_active=True).count()

        courses_active = Course.objects.filter(is_active=True).count()

        teachers = User.objects.filter(
            is_active=True,
            roles__codename=Role.TEACHER,
        ).distinct().count()

        paid_orders_qs = Order.objects.filter(
            status='paid',
            paid_at__gte=month_ago,
        )
        orders_paid_30d = paid_orders_qs.count()

        revenue_30d = paid_orders_qs.aggregate(s=Sum('total'))['s'] or 0

        contact_messages_unread = ContactMessage.objects.filter(is_read=False).count()

        submissions_pending = Submission.objects.filter(status='submitted').count()

        counters = {
            'students_active': students_active,
            'students_total': students_total,
            'courses_active': courses_active,
            'teachers': teachers,
            'orders_paid_30d': orders_paid_30d,
            'revenue_usd_30d': f"{revenue_30d:.2f}",
            'contact_messages_unread': contact_messages_unread,
            'submissions_pending': submissions_pending,
        }

        # ---------- Последние оплаты ----------
        recent_payments_qs = (
            Payment.objects
            .filter(status='approved')
            .select_related('user', 'order')
            .order_by('-paid_at', '-created_at')[:5]
        )
        recent_payments = [
            {
                'id': p.id,
                'order_number': p.order.order_number if p.order else '—',
                'user_email': p.user.email,
                'user_name': p.user.username or p.user.email,
                'amount': f"{p.amount:.2f}",
                'currency': 'USD',
                'status': p.status,
                'status_display': p.get_status_display(),
                'paid_at': p.paid_at,
                'created_at': p.created_at,
            }
            for p in recent_payments_qs
        ]

        # ---------- Последние регистрации ----------
        recent_users_qs = (
            User.objects
            .prefetch_related('roles')
            .order_by('-created_at')[:5]
        )
        recent_registrations = [
            {
                'id': u.id,
                'email': u.email,
                'username': u.username,
                'phone': u.phone,
                'roles': [r.codename for r in u.roles.all()],
                'created_at': u.created_at,
            }
            for u in recent_users_qs
        ]

        # ---------- Свежие заявки ----------
        recent_messages_qs = (
            ContactMessage.objects
            .order_by('-created_at')[:5]
        )
        recent_contact_messages = [
            {
                'id': m.id,
                'name': m.name,
                'email': m.email,
                'motivo': m.motivo,
                'message_preview': (m.message[:120] + '...') if len(m.message) > 120 else m.message,
                'is_read': m.is_read,
                'created_at': m.created_at,
            }
            for m in recent_messages_qs
        ]

        return Response({
            'counters': counters,
            'recent_payments': recent_payments,
            'recent_registrations': recent_registrations,
            'recent_contact_messages': recent_contact_messages,
        })