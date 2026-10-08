from django.core.management.base import BaseCommand
from school.models import Course, Enrollment


class Command(BaseCommand):
    help = (
        'Пересчитать access_expires_at для всех Enrollment курса '
        'по текущим настройкам. Используется, когда админ меняет режим '
        'доступа курса (например, с duration на unlimited).'
    )

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='ID курса')

    def handle(self, *args, **options):
        course_id = options['course_id']
        course = Course.objects.filter(pk=course_id).first()
        if not course:
            self.stdout.write(self.style.ERROR(f'Курс #{course_id} не найден'))
            return

        from school.signals import compute_access_expires_at

        enrollments = Enrollment.objects.filter(course=course)
        updated = 0
        for enr in enrollments:
            new_expires = compute_access_expires_at(enr)
            if enr.access_expires_at != new_expires:
                enr.access_expires_at = new_expires
                enr.save(update_fields=['access_expires_at'])
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Обновлено {updated} из {enrollments.count()} Enrollment '
            f'для курса «{course.title}» (mode={course.access_mode})'
        ))
