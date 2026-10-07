from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Sum, Max, Avg, IntegerField, Value, OuterRef, Subquery, Exists
from django.db.models.functions import Coalesce, Cast
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from mentored.models import ContactMessage, Order, Role
from payments.models import Payment
from school.models import Course, Enrollment, LessonProgress, Submission, Lesson, Certificate, ProductCourseAccess
from mentored.models import OrderItem, Order

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


class CourseListView(APIView):
    """
    GET /crm/courses/

    Список учебных курсов (school.Course) с агрегатами:
      - студентов активных
      - завершивших (по Certificate)
      - средний прогресс (Subquery)
      - оплат (через ProductCourseAccess → OrderItem → Order paid)
      - суммы продаж в USD

    Query-параметры:
      - search          — по названию и slug
      - status          — 'active' | 'inactive'
      - has_whatsapp    — 'true' — только с WhatsApp-ссылкой
      - ordering        — title, -title, created_at, -created_at,
                          students_count, -students_count,
                          avg_progress, -avg_progress,
                          revenue_usd, -revenue_usd
      - page, page_size — пагинация
    """
    permission_classes = [IsSuperuser]

    def get(self, request):
        qs = Course.objects.all()

        # --- Поиск ---
        search = (request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(slug__icontains=search))

        # --- Фильтр по статусу ---
        status = request.query_params.get('status')
        if status == 'active':
            qs = qs.filter(is_active=True)
        elif status == 'inactive':
            qs = qs.filter(is_active=False)

        # --- Только с WhatsApp ---
        if request.query_params.get('has_whatsapp') == 'true':
            qs = qs.exclude(whatsapp_group_url='')

        # --- Subquery: средний прогресс по курсу ---
        # avg_progress = AVG(
        #   completed_lessons_per_enrollment / total_lessons * 100
        # )
        # Считаем вложенным Subquery - Django умеет.
        total_lessons_sq = (
            Lesson.objects
            .filter(module__course__id=OuterRef('id'))
            .values('module__course__id')
            .annotate(c=Count('id'))
            .values('c')
        )
        completed_lessons_sq = (
            LessonProgress.objects
            .filter(enrollment__course__id=OuterRef('id'), is_completed=True)
            .values('enrollment__course__id')
            .annotate(c=Count('id'))
            .values('c')
        )
        # Приближённый расчёт: общее кол-во completed / (students * lessons)
        # Точный AVG по каждому ученику был бы ещё одним уровнем subquery.
        # Для списка курсов это компромисс - достаточно для дашборда.
        qs = qs.annotate(
            total_lessons=Coalesce(
                Subquery(total_lessons_sq, output_field=IntegerField()),
                Value(0),
            ),
            completed_lessons=Coalesce(
                Subquery(completed_lessons_sq, output_field=IntegerField()),
                Value(0),
            ),
        )

        # --- Аннотации ---
        qs = qs.annotate(
            students_count=Count(
                'enrollments',
                filter=Q(enrollments__is_active=True),
                distinct=True,
            ),
            completions_count=Count(
                'enrollments__certificate',
                distinct=True,
            ),
        )

        # --- Сортировка ---
        ordering = request.query_params.get('ordering', 'title')
        allowed = {
            'title', '-title',
            'created_at', '-created_at',
            'students_count', '-students_count',
            'completions_count', '-completions_count',
        }
        if ordering not in allowed:
            ordering = 'title'
        qs = qs.order_by(ordering)

        # --- Пагинация ---
        paginator = CrmPagination()
        page = paginator.paginate_queryset(qs, request, view=self)

        # --- Продажи: собираем через ProductCourseAccess -> OrderItem ---
        # За один проход: берём ID всех курсов на странице,
        # находим связанные ProductCourseAccess, потом OrderItem.
        course_ids = [c.id for c in page]
        sales_by_course = _aggregate_sales_by_course(course_ids)

        results = []
        for c in page:
            total_lessons = c.total_lessons or 0
            completed_lessons = c.completed_lessons or 0
            students_count = c.students_count or 0
            avg_progress = 0
            if total_lessons > 0 and students_count > 0:
                # Приближённое среднее
                avg_progress = int(round(
                    (completed_lessons / (total_lessons * students_count)) * 100
                ))
                avg_progress = min(avg_progress, 100)

            sales = sales_by_course.get(c.id, {'count': 0, 'total': 0})

            results.append({
                'id': c.id,
                'title': c.title,
                'slug': c.slug,
                'is_active': c.is_active,
                'created_at': c.created_at,
                'has_whatsapp': bool(c.whatsapp_group_url),
                'students_count': students_count,
                'completions_count': c.completions_count or 0,
                'avg_progress': avg_progress,
                'payments_count': sales['count'],
                'revenue_usd': f"{sales['total']:.2f}",
            })

        return paginator.get_paginated_response(results)


def _aggregate_sales_by_course(course_ids):
    """
    Для списка ID курсов возвращает {course_id: {'count': N, 'total': Decimal}}.
    Идёт через ProductCourseAccess → OrderItem → Order(status='paid').

    Один товар может открывать несколько курсов, поэтому считаем
    OrderItem.count по каждому из связанных курсов (то есть продажи
    одного товара попадут во все курсы, которые он открывает).
    """
    if not course_ids:
        return {}

    # Все связи товар -> курс для нужных курсов
    links = (
        ProductCourseAccess.objects
        .filter(course_id__in=course_ids)
        .values('course_id', 'content_type_id', 'object_id')
    )

    # Собираем (course_id) -> [(ct_id, obj_id), ...]
    course_to_products = {}
    for link in links:
        course_to_products.setdefault(link['course_id'], []).append(
            (link['content_type_id'], link['object_id'])
        )

    if not course_to_products:
        return {cid: {'count': 0, 'total': 0} for cid in course_ids}

    # Все OrderItem по оплаченным заказам
    # Фильтруем по (product_type, product_id) - product_type у тебя = ContentType.model
    paid_items = (
        OrderItem.objects
        .filter(order__status='paid')
        .values('product_type', 'product_id', 'quantity', 'total')
    )

    # Индекс: (product_type, product_id) -> list of items
    items_index = {}
    for item in paid_items:
        key = (item['product_type'], item['product_id'])
        items_index.setdefault(key, []).append(item)

    # Считаем по каждому курсу
    result = {}
    for course_id in course_ids:
        count = 0
        total = 0
        for ct_id, obj_id in course_to_products.get(course_id, []):
            # Находим model-имя ContentType
            ct = ContentType.objects.filter(id=ct_id).first()
            if not ct:
                continue
            model_name = ct.model  # 'course', 'membership', ...
            key = (model_name, obj_id)
            for item in items_index.get(key, []):
                count += 1
                total += item['total']
        result[course_id] = {'count': count, 'total': total}

    return result


STATUS_ES_ORDER = {
    'pending': 'Pendiente',
    'paid': 'Aprobado',
    'processing': 'En proceso',
    'completed': 'Completado',
    'cancelled': 'Cancelado',
    'refunded': 'Reembolsado',
}


def _course_stats(course):
    """
    Считает агрегаты для одного курса: ученики, завершившие,
    средний прогресс, оплаты, сумма продаж.
    Возвращает dict.
    """
    students_count = Enrollment.objects.filter(course=course, is_active=True).count()
    completions_count = Certificate.objects.filter(enrollment__course=course).count()

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = LessonProgress.objects.filter(
        enrollment__course=course, is_completed=True,
    ).count()

    avg_progress = 0
    if total_lessons > 0 and students_count > 0:
        avg_progress = int(round(
            (completed_lessons / (total_lessons * students_count)) * 100
        ))
        avg_progress = min(avg_progress, 100)

    sales = _aggregate_sales_by_course([course.id]).get(course.id, {'count': 0, 'total': 0})

    return {
        'students_count': students_count,
        'completions_count': completions_count,
        'avg_progress': avg_progress,
        'payments_count': sales['count'],
        'revenue_usd': f"{sales['total']:.2f}",
    }


class CourseDetailView(APIView):
    """
    GET /crm/courses/<id>/

    Детальная карточка курса: хедер, статистика, модули+уроки,
    первые 20 учеников, первые 20 заказов, связанные товары,
    ссылка на форум и WhatsApp.
    """
    permission_classes = [IsSuperuser]

    def get(self, request, pk):
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return Response({'detail': 'Curso no encontrado.'}, status=404)

        # --- Модули и уроки ---
        modules = (
            Module.objects
            .filter(course=course)
            .prefetch_related('lessons')
            .order_by('order', 'id')
        )
        modules_data = []
        for m in modules:
            lessons = m.lessons.all().order_by('order', 'id')
            modules_data.append({
                'id': m.id,
                'title': m.title,
                'order': m.order,
                'lessons': [
                    {
                        'id': l.id,
                        'title': l.title,
                        'order': l.order,
                        'duration_minutes': l.duration_minutes,
                        'is_free_preview': l.is_free_preview,
                        'has_video': bool(l.video_file or l.video_url),
                    }
                    for l in lessons
                ],
            })

        # --- Ученики (первые 20) ---
        students_qs = (
            Enrollment.objects
            .filter(course=course)
            .select_related('user')
            .order_by('-enrolled_at')
        )
        students_total = students_qs.count()
        students_first_page = students_qs[:20]
        students_data = _serialize_course_students(students_first_page, course)

        # --- Заказы (первые 20) ---
        orders_qs, orders_total = _get_course_orders(course)
        orders_first_page = orders_qs[:20]
        orders_data = _serialize_course_orders(orders_first_page)

        # --- Связанные витринные товары ---
        links = (
            ProductCourseAccess.objects
            .filter(course=course)
            .select_related('content_type')
        )
        products_data = []
        for link in links:
            p = link.product  # через GenericForeignKey
            if not p:
                continue
            products_data.append({
                'type': link.content_type.model,   # 'course', 'membership', ...
                'id': p.id,
                'name': getattr(p, 'name', str(p)),
                'price': f"{getattr(p, 'price', 0):.2f}",
                'is_active': getattr(p, 'is_active', True),
                'admin_url': f"/admin/{link.content_type.app_label}/{link.content_type.model}/{p.id}/change/",
            })

        return Response({
            'id': course.id,
            'title': course.title,
            'slug': course.slug,
            'description': course.description,
            'is_active': course.is_active,
            'created_at': course.created_at,
            'updated_at': course.updated_at,
            'whatsapp_group_url': course.whatsapp_group_url,
            'creator': {
                'id': course.creator.id,
                'username': course.creator.username,
                'email': course.creator.email,
            } if course.creator else None,
            'stats': _course_stats(course),
            'modules': modules_data,
            'students': {
                'count': students_total,
                'page_size': 20,
                'results': students_data,
            },
            'orders': {
                'count': orders_total,
                'page_size': 20,
                'results': orders_data,
            },
            'products': products_data,
            'forum_url': f"/escuela/foro/{course.id}",
        })


class CourseStudentsView(APIView):
    """
    GET /crm/courses/<id>/students/?page=N&page_size=20
    Пагинация учеников курса.
    """
    permission_classes = [IsSuperuser]

    def get(self, request, pk):
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return Response({'detail': 'Curso no encontrado.'}, status=404)

        qs = (
            Enrollment.objects
            .filter(course=course)
            .select_related('user')
            .order_by('-enrolled_at')
        )

        paginator = CrmPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        data = _serialize_course_students(page, course)
        return paginator.get_paginated_response(data)


class CourseOrdersView(APIView):
    """
    GET /crm/courses/<id>/orders/?page=N&page_size=20
    Пагинация заказов, содержащих этот курс.
    """
    permission_classes = [IsSuperuser]

    def get(self, request, pk):
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return Response({'detail': 'Curso no encontrado.'}, status=404)

        qs, _ = _get_course_orders(course)

        paginator = CrmPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        data = _serialize_course_orders(page)
        return paginator.get_paginated_response(data)


# ============================================================
# Хелперы
# ============================================================

def _serialize_course_students(enrollments, course):
    """
    Для списка Enrollment возвращает компактные строки с прогрессом.
    """
    total_lessons = Lesson.objects.filter(module__course=course).count()

    result = []
    for enr in enrollments:
        completed = LessonProgress.objects.filter(
            enrollment=enr, is_completed=True,
        ).count()
        progress = int(round(completed / total_lessons * 100)) if total_lessons else 0
        last_activity = (
            LessonProgress.objects
            .filter(enrollment=enr)
            .aggregate(m=Max('updated_at'))['m']
        )
        has_certificate = Certificate.objects.filter(enrollment=enr).exists()

        result.append({
            'user_id': enr.user.id,
            'username': enr.user.username or enr.user.email,
            'email': enr.user.email,
            'enrolled_at': enr.enrolled_at,
            'is_active': enr.is_active,
            'lessons_total': total_lessons,
            'lessons_completed': completed,
            'progress_percent': progress,
            'completed': has_certificate,
            'last_activity': last_activity,
        })
    return result


def _get_course_orders(course):
    """
    Возвращает (queryset Order, total_count) для заказов, где
    встречается хотя бы один товар, открывающий доступ к этому курсу.
    """
    # Все товары, открывающие доступ к курсу
    links = ProductCourseAccess.objects.filter(course=course).select_related('content_type')
    product_keys = [
        (link.content_type.model, link.object_id)   # ('course', 5) или ('membership', 2)
        for link in links
    ]

    if not product_keys:
        return Order.objects.none(), 0

    # Все OrderItem, у которых (product_type, product_id) из product_keys
    q = Q()
    for ptype, pid in product_keys:
        q |= Q(product_type=ptype, product_id=pid)

    items = OrderItem.objects.filter(q).values_list('order_id', flat=True)
    orders_qs = (
        Order.objects
        .filter(id__in=items)
        .select_related('user')
        .prefetch_related('items')
        .order_by('-created_at')
    )
    return orders_qs, orders_qs.count()


def _serialize_course_orders(orders):
    result = []
    for o in orders:
        result.append({
            'id': o.id,
            'order_number': o.order_number,
            'user_name': o.user.username or o.user.email,
            'user_email': o.user.email,
            'status': o.status,
            'status_display': STATUS_ES_ORDER.get(o.status, o.status),
            'total': f"{o.total:.2f}",
            'currency': 'USD',
            'paid_at': o.paid_at,
            'created_at': o.created_at,
            'items': [i.product_name for i in o.items.all()],
        })
    return result