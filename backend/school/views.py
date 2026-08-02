from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Course, Enrollment, Lesson, LessonProgress
from .permissions import IsStudent
from .serializers import ModuleSerializer, MyCourseSerializer


class MyCoursesView(APIView):
    """ GET /school/my-courses/ - курсы, купленные студентом (активный Enrollment). """
    permission_classes = [IsAuthenticated, IsStudent]

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
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_active=True)
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course, is_active=True,
        ).first()
        if not enrollment:
            return Response({'error': 'Нет доступа к этому курсу'}, status=status.HTTP_403_FORBIDDEN)

        modules = course.modules.prefetch_related('lessons__materials').order_by('order')
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
    permission_classes = [IsAuthenticated, IsStudent]

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
