"""
Экспорт данных CRM в XLSX.

Каждая функция принимает готовый queryset (уже отфильтрованный) и
возвращает (filename, bytes) — имя файла и содержимое в виде байтов.
"""
from io import BytesIO
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter


HEADER_FILL = PatternFill(start_color="0E0C0C", end_color="0E0C0C", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)


def _new_workbook(title):
    wb = Workbook()
    ws = wb.active
    ws.title = title
    return wb, ws


def _write_header(ws, headers):
    ws.append(headers)
    for col_idx, _ in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = HEADER_ALIGN
    ws.freeze_panes = "A2"


def _autosize(ws, min_width=10, max_width=50):
    for col_idx, column in enumerate(ws.iter_cols(min_row=1, max_row=ws.max_row), start=1):
        max_len = 0
        for cell in column:
            if cell.value is not None:
                max_len = max(max_len, len(str(cell.value)))
        width = min(max(max_len + 2, min_width), max_width)
        ws.column_dimensions[get_column_letter(col_idx)].width = width


def _to_bytes(wb):
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()


def _filename(prefix):
    return f"{prefix}-{datetime.now().strftime('%Y-%m-%d')}.xlsx"


def _fmt_date(dt):
    if not dt:
        return ''
    return dt.strftime('%d/%m/%Y')


def _fmt_datetime(dt):
    if not dt:
        return ''
    return dt.strftime('%d/%m/%Y %H:%M')


# ============================================================
# ALUMNOS
# ============================================================

def export_students(queryset):
    wb, ws = _new_workbook("Alumnos")
    _write_header(ws, [
        "ID", "Nombre", "Email", "Teléfono",
        "Roles", "Cursos activos", "Estado",
        "Registro",
    ])

    for u in queryset:
        courses_active = u.enrollments.filter(is_active=True).count() if hasattr(u, 'enrollments') else 0
        ws.append([
            u.id,
            u.username or u.email,
            u.email,
            u.phone or '',
            ', '.join(r.codename for r in u.roles.all()),
            courses_active,
            'Activo' if u.is_active else 'Inactivo',
            _fmt_date(u.created_at),
        ])

    _autosize(ws)
    return _filename('alumnos'), _to_bytes(wb)


# ============================================================
# CURSOS
# ============================================================

def export_courses(queryset):
    from school.models import Enrollment, Lesson, LessonProgress, Certificate

    wb, ws = _new_workbook("Cursos")
    _write_header(ws, [
        "ID", "Título", "Slug", "Estado",
        "Alumnos activos", "Completados", "Progreso medio %",
        "WhatsApp", "Creado",
    ])

    for c in queryset:
        students = Enrollment.objects.filter(course=c, is_active=True).count()
        completions = Certificate.objects.filter(enrollment__course=c).count()

        total_lessons = Lesson.objects.filter(module__course=c).count()
        completed_lessons = LessonProgress.objects.filter(
            enrollment__course=c, is_completed=True,
        ).count()
        avg = 0
        if total_lessons > 0 and students > 0:
            avg = int(round((completed_lessons / (total_lessons * students)) * 100))
            avg = min(avg, 100)

        ws.append([
            c.id,
            c.title,
            c.slug,
            'Activo' if c.is_active else 'Inactivo',
            students,
            completions,
            avg,
            'Sí' if c.whatsapp_group_url else 'No',
            _fmt_date(c.created_at),
        ])

    _autosize(ws)
    return _filename('cursos'), _to_bytes(wb)


# ============================================================
# PROFESORES
# ============================================================

def export_teachers(queryset):
    wb, ws = _new_workbook("Profesores")
    _write_header(ws, [
        "ID", "Nombre", "Email", "Teléfono",
        "Cursos asignados", "Alumnos únicos", "Estado", "Registro",
    ])

    for u in queryset:
        courses = u.taught_courses.count() if hasattr(u, 'taught_courses') else 0
        student_ids = set()
        if hasattr(u, 'taught_courses'):
            for ct in u.taught_courses.all():
                student_ids.update(
                    ct.course.enrollments.filter(is_active=True).values_list('user_id', flat=True)
                )
        ws.append([
            u.id,
            u.username or u.email,
            u.email,
            u.phone or '',
            courses,
            len(student_ids),
            'Activo' if u.is_active else 'Inactivo',
            _fmt_date(u.created_at),
        ])

    _autosize(ws)
    return _filename('profesores'), _to_bytes(wb)


# ============================================================
# PEDIDOS (Orders)
# ============================================================

STATUS_ES = {
    'pending': 'Pendiente',
    'paid': 'Aprobado',
    'processing': 'En proceso',
    'completed': 'Completado',
    'cancelled': 'Cancelado',
    'refunded': 'Reembolsado',
}


def export_orders(queryset):
    wb, ws = _new_workbook("Pedidos")
    _write_header(ws, [
        "Pedido", "Cliente", "Email", "Productos",
        "Total USD", "Estado pedido", "Estado pago", "Método",
        "Creado", "Pagado",
    ])

    for o in queryset:
        payment = getattr(o, 'payment', None)
        product_names = ', '.join(i.product_name for i in o.items.all())
        ws.append([
            o.order_number,
            o.user.username or o.user.email,
            o.user.email,
            product_names,
            float(o.total),
            STATUS_ES.get(o.status, o.status),
            STATUS_ES.get(payment.status, payment.status) if payment else '',
            payment.payment_method if payment else '',
            _fmt_datetime(o.created_at),
            _fmt_datetime(o.paid_at),
        ])

    _autosize(ws)
    return _filename('pedidos'), _to_bytes(wb)


# ============================================================
# TAREAS (Submissions)
# ============================================================

STATUS_ES_SUBMISSION = {
    'submitted': 'Pendiente',
    'reviewed': 'Revisado',
    'needs_revision': 'Revisión',
}


def export_submissions(queryset):
    wb, ws = _new_workbook("Tareas")
    _write_header(ws, [
        "ID", "Alumno", "Email", "Curso", "Lección", "Tarea",
        "Estado", "Nota", "Revisado por", "Fecha envío", "Fecha revisión",
    ])

    for s in queryset:
        course = s.assignment.lesson.module.course
        ws.append([
            s.id,
            s.enrollment.user.username or s.enrollment.user.email,
            s.enrollment.user.email,
            course.title,
            s.assignment.lesson.title,
            s.assignment.title,
            STATUS_ES_SUBMISSION.get(s.status, s.status),
            s.score if s.score is not None else '',
            (s.reviewed_by.username or s.reviewed_by.email) if s.reviewed_by else '',
            _fmt_datetime(s.submitted_at),
            _fmt_datetime(s.reviewed_at),
        ])

    _autosize(ws)
    return _filename('tareas'), _to_bytes(wb)


# ============================================================
# MENSAJES
# ============================================================

def export_contact_messages(queryset):
    wb, ws = _new_workbook("Mensajes")
    _write_header(ws, [
        "ID", "Nombre", "Email", "Motivo",
        "Mensaje", "Leído", "Fecha",
    ])

    for m in queryset:
        ws.append([
            m.id,
            m.name,
            m.email,
            m.motivo,
            m.message,
            'Sí' if m.is_read else 'No',
            _fmt_datetime(m.created_at),
        ])

    _autosize(ws)
    return _filename('mensajes'), _to_bytes(wb)


# ============================================================
# ОТЧЁТ ПО КУРСУ
# ============================================================

def export_course_report(course):
    from school.models import Enrollment, Lesson, LessonProgress, Certificate
    from django.db.models import Max

    wb, ws = _new_workbook(f"Curso {course.id}")
    _write_header(ws, [
        "Alumno", "Email", "Inscrito",
        "Lecciones completadas", "Total lecciones",
        "Progreso %", "Completado", "Última actividad",
    ])

    total_lessons = Lesson.objects.filter(module__course=course).count()
    enrollments = Enrollment.objects.filter(course=course).select_related('user').order_by('-enrolled_at')

    for enr in enrollments:
        completed = LessonProgress.objects.filter(enrollment=enr, is_completed=True).count()
        progress = int(round(completed / total_lessons * 100)) if total_lessons else 0
        last = LessonProgress.objects.filter(enrollment=enr).aggregate(m=Max('updated_at'))['m']
        has_cert = Certificate.objects.filter(enrollment=enr).exists()

        ws.append([
            enr.user.username or enr.user.email,
            enr.user.email,
            _fmt_date(enr.enrolled_at),
            completed,
            total_lessons,
            progress,
            'Sí' if has_cert else 'No',
            _fmt_date(last),
        ])

    _autosize(ws)
    return _filename(f'curso-{course.id}-reporte'), _to_bytes(wb)


# ============================================================
# ОТЧЁТ ПО ПРОДАЖАМ ЗА ПЕРИОД
# ============================================================

def export_sales_report(date_from=None, date_to=None):
    """
    Сводка по проданным товарам: course / membership / book / consultation.
    Считаем по OrderItem оплаченных заказов за период.
    """
    from django.db.models import Count, Sum
    from mentored.models import OrderItem

    qs = OrderItem.objects.filter(order__status='paid')
    if date_from:
        qs = qs.filter(order__paid_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(order__paid_at__date__lte=date_to)

    summary = (
        qs.values('product_type', 'product_name')
        .annotate(
            count=Count('id'),
            total=Sum('total'),
        )
        .order_by('-total')
    )

    wb, ws = _new_workbook("Ventas")
    _write_header(ws, [
        "Tipo de producto", "Producto",
        "Cantidad de ventas", "Total USD",
    ])

    grand_count = 0
    grand_total = 0
    for row in summary:
        count = row['count']
        total = float(row['total'] or 0)
        grand_count += count
        grand_total += total
        ws.append([
            row['product_type'] or '—',
            row['product_name'],
            count,
            round(total, 2),
        ])

    ws.append([])
    total_row_idx = ws.max_row + 1
    ws.append(["TOTAL", "", grand_count, round(grand_total, 2)])
    for col_idx in range(1, 5):
        c = ws.cell(row=total_row_idx, column=col_idx)
        c.font = Font(bold=True)

    _autosize(ws)
    return _filename('reporte-ventas'), _to_bytes(wb)