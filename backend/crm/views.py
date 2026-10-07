from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum, Max
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from mentored.models import ContactMessage, Order, Role
from payments.models import Payment
from school.models import Course, Enrollment, LessonProgress, Submission, Lesson

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

class CrmPagination(PageNumberPagination):
    """
    Пагинация для всех списков CRM.
    По умолчанию 20, но можно ?page_size=50 / ?page_size=100.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200

class StudentListView(APIView):
    """
    GET /crm/students/

    Список учеников с фильтрами и пагинацией.

    Query-параметры:
      - search           — поиск по email, username, phone
      - access           — 'active' | 'none' (фильтр по наличию Enrollment)
      - role             — 'student' | 'teacher' (по роли)
      - ordering         — '-created_at', 'username', 'email'
      - page             — номер страницы
      - page_size        — размер страницы (20/50/100)

    Ответ: {count, page, page_size, pages, results: [...]}
    """
    permission_classes = [IsSuperuser]

    def get(self, request):
        qs = User.objects.filter(is_active=True)

        # --- Поиск ---
        search = (request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(phone__icontains=search)
            )

        # --- Фильтр по доступу ---
        access = request.query_params.get('access')
        if access == 'active':
            qs = qs.filter(enrollments__is_active=True).distinct()
        elif access == 'none':
            qs = qs.exclude(enrollments__is_active=True).distinct()

        # --- Фильтр по роли ---
        role = request.query_params.get('role')
        if role:
            qs = qs.filter(roles__codename=role).distinct()

        # --- Сортировка ---
        ordering = request.query_params.get('ordering', '-created_at')
        allowed_ordering = {
            'created_at', '-created_at',
            'username', '-username',
            'email', '-email',
        }
        if ordering not in allowed_ordering:
            ordering = '-created_at'

        # --- Аннотации: кол-во активных курсов + флаг доступа ---
        qs = qs.annotate(
            courses_count=Count(
                'enrollments',
                filter=Q(enrollments__is_active=True),
                distinct=True,
            ),
        ).prefetch_related('roles').order_by(ordering)

        # --- Пагинация ---
        paginator = CrmPagination()
        page = paginator.paginate_queryset(qs, request, view=self)

        results = [
            {
                'id': u.id,
                'email': u.email,
                'username': u.username,
                'phone': u.phone,
                'created_at': u.created_at,
                'courses_count': u.courses_count,
                'has_access': u.courses_count > 0,
                'roles': [r.codename for r in u.roles.all()],
            }
            for u in page
        ]

        return paginator.get_paginated_response(results)


class StudentDetailView(APIView):
    """
    GET /crm/students/<id>/

    Детальная карточка ученика: основные данные, список курсов
    (с прогрессом по каждому), список заказов, агрегированная статистика.
    """
    permission_classes = [IsSuperuser]

    def get(self, request, pk):
        user = (
            User.objects
            .prefetch_related('roles')
            .filter(pk=pk)
            .first()
        )
        if not user:
            return Response({'detail': 'Alumno no encontrado.'}, status=404)

        # ---------- Курсы ученика с прогрессом ----------
        enrollments = (
            Enrollment.objects
            .filter(user=user)
            .select_related('course')
            .order_by('-enrolled_at')
        )

        courses = []
        for enr in enrollments:
            lessons_total = Lesson.objects.filter(module__course=enr.course).count()
            lessons_completed = LessonProgress.objects.filter(
                enrollment=enr,
                is_completed=True,
            ).count()
            progress_percent = (
                int(round(lessons_completed / lessons_total * 100))
                if lessons_total else 0
            )
            last_activity = (
                LessonProgress.objects
                .filter(enrollment=enr)
                .aggregate(m=Max('updated_at'))['m']
            )

            courses.append({
                'course_id': enr.course.id,
                'course_title': enr.course.title,
                'course_slug': enr.course.slug,
                'enrolled_at': enr.enrolled_at,
                'is_active': enr.is_active,
                'lessons_total': lessons_total,
                'lessons_completed': lessons_completed,
                'progress_percent': progress_percent,
                'last_activity': last_activity,
            })

        # ---------- Заказы ученика ----------
        orders_qs = (
            Order.objects
            .filter(user=user)
            .prefetch_related('items')
            .order_by('-created_at')[:20]
        )

        STATUS_ES = {
            'pending': 'Pendiente',
            'paid': 'Aprobado',
            'processing': 'En proceso',
            'completed': 'Completado',
            'cancelled': 'Cancelado',
            'refunded': 'Reembolsado',
        }

        orders = [
            {
                'id': o.id,
                'order_number': o.order_number,
                'created_at': o.created_at,
                'paid_at': o.paid_at,
                'status': o.status,
                'status_display': STATUS_ES.get(o.status, o.status),
                'total': f"{o.total:.2f}",
                'currency': 'USD',
                'items': [i.product_name for i in o.items.all()],
            }
            for o in orders_qs
        ]

        # ---------- Агрегированная статистика ----------
        orders_paid_qs = Order.objects.filter(user=user, status='paid')
        total_paid = orders_paid_qs.aggregate(s=Sum('total'))['s'] or 0

        # Последняя активность: MAX из LessonProgress.updated_at + Submission.submitted_at
        lp_last = LessonProgress.objects.filter(
            enrollment__user=user,
        ).aggregate(m=Max('updated_at'))['m']

        sub_last = Submission.objects.filter(
            enrollment__user=user,
        ).aggregate(m=Max('submitted_at'))['m']

        last_activity = max([d for d in (lp_last, sub_last) if d], default=None)

        stats = {
            'courses_count': len(courses),
            'courses_active': sum(1 for c in courses if c['is_active']),
            'orders_count': Order.objects.filter(user=user).count(),
            'orders_paid': orders_paid_qs.count(),
            'total_paid_usd': f"{total_paid:.2f}",
            'last_activity': last_activity,
        }

        # ---------- Отдаём ----------
        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None,
            'created_at': user.created_at,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'roles': [r.codename for r in user.roles.all()],
            'courses': courses,
            'orders': orders,
            'stats': stats,
        })