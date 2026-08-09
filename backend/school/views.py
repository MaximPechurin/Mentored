from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
    Course, Enrollment, Lesson, LessonProgress, Assignment, Submission,
)
from .permissions import IsStudent, IsTeacher, IsDev
from .serializers import (
    ModuleSerializer, MyCourseSerializer, AssignmentDetailSerializer,
    TeacherSubmissionSerializer, TeacherCourseSerializer,
    TeacherStudentProgressSerializer,
)


class MyCoursesView(APIView):
    """ GET /school/my-courses/ - курсы, купленные студентом (активный Enrollment). """
    # IsDev - временный гейт, пока школа не открыта для всех (см. permissions.py)
    permission_classes = [IsAuthenticated, IsDev, IsStudent]

    def get(self, request):
        enrollments = Enrollment.objects.filter(
            user=request.user, is_active=True,
        ).select_related('course').order_by('-enrolled_at')
        serializer = MyCourseSerializer(enrollments, many=True)
        return Response(serializer.data)


class CourseDetailView(APIView):
    """
    GET /school/courses/<slug>/ - модули/уроки курса, на который у
    пользователя есть активный доступ (Enrollment). Без доступа - 403.

    Анонимный просмотр is_free_preview уроков без залогина/покупки
    сознательно не делаем сейчас - это отдельная задача на будущее
    (публичные превью-уроки для маркетинга), не путать с "доступ есть,
    но урок помечен free preview" - тут это уже неважно, раз Enrollment
    и так есть.
    """
    permission_classes = [IsAuthenticated, IsDev, IsStudent]

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_active=True)
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course, is_active=True,
        ).first()
        if not enrollment:
            return Response({'error': 'Нет доступа к этому курсу'}, status=status.HTTP_403_FORBIDDEN)

        modules = course.modules.prefetch_related(
            'lessons__materials', 'lessons__assignments',
        ).order_by('order')
        progress_by_lesson = {
            p.lesson_id: p for p in LessonProgress.objects.filter(enrollment=enrollment)
        }
        modules_data = ModuleSerializer(
            modules, many=True, context={'progress_by_lesson': progress_by_lesson},
        ).data

        return Response({
            'id': course.id,
            'slug': course.slug,
            'title': course.title,
            'description': course.description,
            'modules': modules_data,
        })


class LessonProgressView(APIView):
    """
    POST /school/lessons/<id>/progress/ - отметить прогресс по уроку.
    Тело: {"is_completed": true} и/или {"last_position_seconds": 120}.
    Требует активного Enrollment на курс, которому принадлежит урок -
    иначе можно было бы отмечать прогресс по чужим/некупленным курсам.
    """
    permission_classes = [IsAuthenticated, IsDev, IsStudent]

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = lesson.module.course
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course, is_active=True,
        ).first()
        if not enrollment:
            return Response({'error': 'Нет доступа к этому курсу'}, status=status.HTTP_403_FORBIDDEN)

        progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)

        is_completed = request.data.get('is_completed')
        last_position_seconds = request.data.get('last_position_seconds')

        if is_completed is not None:
            progress.is_completed = bool(is_completed)
            progress.completed_at = timezone.now() if progress.is_completed else None

        if last_position_seconds is not None:
            try:
                progress.last_position_seconds = int(last_position_seconds)
            except (TypeError, ValueError):
                return Response(
                    {'error': 'last_position_seconds должен быть числом'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        progress.save()
        return Response({
            'is_completed': progress.is_completed,
            'last_position_seconds': progress.last_position_seconds,
        })


def _student_enrollment_for_assignment(user, assignment):
    """ Активный Enrollment студента на курс, к которому относится задание, либо None. """
    course = assignment.lesson.module.course
    return Enrollment.objects.filter(user=user, course=course, is_active=True).first()


class AssignmentDetailView(APIView):
    """ GET /school/assignments/<id>/ - задание + мой ответ. Нужен доступ к курсу. """
    permission_classes = [IsAuthenticated, IsDev, IsStudent]

    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        enrollment = _student_enrollment_for_assignment(request.user, assignment)
        if not enrollment:
            return Response({'error': 'Нет доступа к этому курсу'}, status=status.HTTP_403_FORBIDDEN)
        my_sub = Submission.objects.filter(assignment=assignment, enrollment=enrollment).first()
        data = AssignmentDetailSerializer(assignment, context={'my_submission': my_sub}).data
        return Response(data)


class AssignmentSubmitView(APIView):
    """
    POST /school/assignments/<id>/submit/ - сдать/пересдать задание.
    Тело (multipart или json): text и/или file.

    Держим один "текущий" ответ на пару (задание, студент): повторная
    отправка обновляет его и сбрасывает статус в 'submitted' (снимая
    прошлую оценку/комментарий), а не плодит новые записи. Пересдать
    после проверки можно всегда - на случай доработки.
    """
    permission_classes = [IsAuthenticated, IsDev, IsStudent]
    # Глобально в проекте только JSONParser (см. settings), а тут нужен
    # приём файла - разрешаем multipart/form-data точечно на этой вью.
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        enrollment = _student_enrollment_for_assignment(request.user, assignment)
        if not enrollment:
            return Response({'error': 'Нет доступа к этому курсу'}, status=status.HTTP_403_FORBIDDEN)

        text = request.data.get('text', '')
        file = request.FILES.get('file')
        if not text and not file:
            return Response(
                {'error': 'Нужно приложить текст или файл'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission, _ = Submission.objects.get_or_create(
            assignment=assignment, enrollment=enrollment,
        )
        submission.text = text
        if file:
            submission.file = file
        # новая отправка - снова "на проверке", прошлая оценка неактуальна
        submission.status = 'submitted'
        submission.score = None
        submission.mentor_comment = ''
        submission.reviewed_by = None
        submission.reviewed_at = None
        submission.save()

        return Response({
            'id': submission.id,
            'status': submission.status,
        }, status=status.HTTP_201_CREATED)


class TeacherCoursesView(APIView):
    """ GET /school/teacher/courses/ - курсы, которые ведёт этот ментор. """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def get(self, request):
        courses = Course.objects.filter(
            course_teachers__teacher=request.user,
        ).distinct().order_by('title')
        return Response(TeacherCourseSerializer(courses, many=True).data)


class TeacherCourseStudentsView(APIView):
    """
    GET /school/teacher/courses/<course_id>/students/ - ростер студентов
    курса с прогрессом. Только для ментора этого курса, иначе 403.
    """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if not course.course_teachers.filter(teacher=request.user).exists():
            return Response({'error': 'Это не ваш курс'}, status=status.HTTP_403_FORBIDDEN)

        lessons_total = Lesson.objects.filter(module__course=course).count()
        enrollments = course.enrollments.select_related('user').order_by('-enrolled_at')
        data = TeacherStudentProgressSerializer(
            enrollments, many=True, context={'lessons_total': lessons_total},
        ).data
        return Response({
            'course': {'id': course.id, 'title': course.title, 'lessons_total': lessons_total},
            'students': data,
        })


class TeacherSubmissionsView(APIView):
    """
    GET /school/teacher/submissions/ - очередь на проверку: сдачи по
    курсам, которые ведёт этот ментор (school.CourseTeacher).
    По умолчанию только status='submitted' (ждут проверки); ?status=all
    - все, ?status=<value> - конкретный статус.
    """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def get(self, request):
        qs = Submission.objects.filter(
            assignment__lesson__module__course__course_teachers__teacher=request.user,
        ).select_related(
            'enrollment__user', 'assignment__lesson__module__course',
        ).distinct().order_by('-submitted_at')

        status_filter = request.query_params.get('status', 'submitted')
        if status_filter != 'all':
            qs = qs.filter(status=status_filter)

        return Response(TeacherSubmissionSerializer(qs, many=True).data)


class TeacherSubmissionReviewView(APIView):
    """
    POST /school/teacher/submissions/<id>/review/ - проверить сдачу.
    Тело: {"status": "reviewed"|"needs_revision", "score": int|null,
    "mentor_comment": str}. Разрешено только ментору этого курса.
    """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def post(self, request, submission_id):
        submission = get_object_or_404(
            Submission.objects.select_related('assignment__lesson__module__course'),
            id=submission_id,
        )
        course = submission.assignment.lesson.module.course
        # ментор может проверять только сдачи по своим курсам
        if not course.course_teachers.filter(teacher=request.user).exists():
            return Response(
                {'error': 'Это не ваш курс'},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_status = request.data.get('status')
        if new_status not in ('reviewed', 'needs_revision'):
            return Response(
                {'error': "status должен быть 'reviewed' или 'needs_revision'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        score = request.data.get('score')
        if score is not None:
            try:
                score = int(score)
            except (TypeError, ValueError):
                return Response({'error': 'score должен быть числом'}, status=status.HTTP_400_BAD_REQUEST)
            if score < 0 or score > submission.assignment.max_score:
                return Response(
                    {'error': f'score должен быть от 0 до {submission.assignment.max_score}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        submission.status = new_status
        submission.score = score
        submission.mentor_comment = request.data.get('mentor_comment', '')
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save()

        return Response({
            'id': submission.id,
            'status': submission.status,
            'score': submission.score,
        })
