from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import (
    Course, Enrollment, Lesson, LessonProgress, Assignment, Submission,
    ForumThread, ForumPost, DirectMessage, CourseTeacher,
    is_course_participant, is_course_teacher, can_direct_message,
)
from .permissions import IsStudent, IsTeacher, IsDev
from .serializers import (
    ModuleSerializer, MyCourseSerializer, AssignmentDetailSerializer,
    TeacherSubmissionSerializer, TeacherCourseSerializer,
    TeacherStudentProgressSerializer, ForumThreadListSerializer,
    ForumThreadDetailSerializer, ForumPostSerializer, DirectMessageSerializer,
)

User = get_user_model()


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

        # письмо студенту "работа проверена" - best-effort, ревью не роняет
        from .emails import send_submission_reviewed
        send_submission_reviewed(submission)

        return Response({
            'id': submission.id,
            'status': submission.status,
            'score': submission.score,
        })


# ============================================================
# Форум курса
# ============================================================

def _course_teacher_ids(course):
    return set(course.course_teachers.values_list('teacher_id', flat=True))


class CourseThreadsView(APIView):
    """
    GET  /school/courses/<course_id>/threads/ - список тем форума курса.
    POST /school/courses/<course_id>/threads/ - создать тему {title, content}.
    Доступ - только участникам курса (студенты + преподаватели).
    """
    permission_classes = [IsAuthenticated, IsDev]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if not is_course_participant(request.user, course):
            return Response({'error': 'Нет доступа к форуму этого курса'}, status=status.HTTP_403_FORBIDDEN)
        threads = course.forum_threads.select_related('author')
        return Response(ForumThreadListSerializer(threads, many=True).data)

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if not is_course_participant(request.user, course):
            return Response({'error': 'Нет доступа к форуму этого курса'}, status=status.HTTP_403_FORBIDDEN)
        title = (request.data.get('title') or '').strip()
        content = (request.data.get('content') or '').strip()
        if not title or not content:
            return Response({'error': 'Нужны title и content'}, status=status.HTTP_400_BAD_REQUEST)
        thread = ForumThread.objects.create(course=course, author=request.user, title=title)
        ForumPost.objects.create(thread=thread, author=request.user, content=content)
        return Response(ForumThreadListSerializer(thread).data, status=status.HTTP_201_CREATED)


class ThreadDetailView(APIView):
    """ GET /school/threads/<id>/ - тема + все сообщения. """
    permission_classes = [IsAuthenticated, IsDev]

    def get(self, request, thread_id):
        thread = get_object_or_404(ForumThread.objects.select_related('course'), id=thread_id)
        if not is_course_participant(request.user, thread.course):
            return Response({'error': 'Нет доступа'}, status=status.HTTP_403_FORBIDDEN)
        ctx = {'teacher_ids': _course_teacher_ids(thread.course)}
        return Response(ForumThreadDetailSerializer(thread, context=ctx).data)


class ThreadPostsView(APIView):
    """
    POST /school/threads/<id>/posts/ - ответить в теме {content}.
    В закрытой (is_locked) теме отвечать могут только преподаватели.
    """
    permission_classes = [IsAuthenticated, IsDev]

    def post(self, request, thread_id):
        thread = get_object_or_404(ForumThread.objects.select_related('course'), id=thread_id)
        if not is_course_participant(request.user, thread.course):
            return Response({'error': 'Нет доступа'}, status=status.HTTP_403_FORBIDDEN)
        if thread.is_locked and not is_course_teacher(request.user, thread.course):
            return Response({'error': 'Тема закрыта для ответов'}, status=status.HTTP_403_FORBIDDEN)
        content = (request.data.get('content') or '').strip()
        if not content:
            return Response({'error': 'Нужен content'}, status=status.HTTP_400_BAD_REQUEST)
        post = ForumPost.objects.create(thread=thread, author=request.user, content=content)
        # обновляем updated_at темы, чтобы всплыла наверх в списке
        thread.save(update_fields=['updated_at'])
        ctx = {'teacher_ids': _course_teacher_ids(thread.course)}
        return Response(ForumPostSerializer(post, context=ctx).data, status=status.HTTP_201_CREATED)


class ThreadModerateView(APIView):
    """
    POST /school/threads/<id>/moderate/ - закрепить/закрыть тему.
    Тело: {"is_pinned": bool} и/или {"is_locked": bool}. Только препод курса.
    """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def post(self, request, thread_id):
        thread = get_object_or_404(ForumThread.objects.select_related('course'), id=thread_id)
        if not is_course_teacher(request.user, thread.course):
            return Response({'error': 'Это не ваш курс'}, status=status.HTTP_403_FORBIDDEN)
        if 'is_pinned' in request.data:
            thread.is_pinned = bool(request.data.get('is_pinned'))
        if 'is_locked' in request.data:
            thread.is_locked = bool(request.data.get('is_locked'))
        thread.save()
        return Response({'id': thread.id, 'is_pinned': thread.is_pinned, 'is_locked': thread.is_locked})


# ============================================================
# Личные сообщения (студент <-> преподаватель с общим курсом)
# ============================================================

class ConversationsView(APIView):
    """ GET /school/messages/ - список диалогов (собеседник + последнее сообщение + непрочитанные). """
    permission_classes = [IsAuthenticated, IsDev]

    def get(self, request):
        me = request.user
        msgs = DirectMessage.objects.filter(
            Q(sender=me) | Q(recipient=me),
        ).select_related('sender', 'recipient').order_by('-created_at')

        conversations = {}
        for m in msgs:
            other = m.recipient if m.sender_id == me.id else m.sender
            if other.id not in conversations:
                conversations[other.id] = {
                    'user_id': other.id,
                    'name': other.username or other.email,
                    'last_message': m.content,
                    'last_at': m.created_at,
                    'unread': 0,
                }
            # непрочитанные = входящие мне и is_read=False
            if m.recipient_id == me.id and not m.is_read:
                conversations[other.id]['unread'] += 1

        return Response(list(conversations.values()))


class ConversationView(APIView):
    """
    GET  /school/messages/<user_id>/ - переписка с пользователем (и помечает входящие прочитанными).
    POST /school/messages/<user_id>/ - отправить сообщение {content}.
    Разрешено только между студентом и преподавателем с общим курсом.
    """
    permission_classes = [IsAuthenticated, IsDev]

    def get(self, request, user_id):
        other = get_object_or_404(User, id=user_id)
        me = request.user
        qs = DirectMessage.objects.filter(
            Q(sender=me, recipient=other) | Q(sender=other, recipient=me),
        ).order_by('created_at')
        # помечаем входящие прочитанными
        DirectMessage.objects.filter(sender=other, recipient=me, is_read=False).update(is_read=True)
        return Response(DirectMessageSerializer(qs, many=True, context={'me_id': me.id}).data)

    def post(self, request, user_id):
        other = get_object_or_404(User, id=user_id)
        me = request.user
        if not can_direct_message(me, other):
            return Response(
                {'error': 'Личные сообщения доступны только между студентом и преподавателем общего курса'},
                status=status.HTTP_403_FORBIDDEN,
            )
        content = (request.data.get('content') or '').strip()
        if not content:
            return Response({'error': 'Нужен content'}, status=status.HTTP_400_BAD_REQUEST)
        msg = DirectMessage.objects.create(sender=me, recipient=other, content=content)
        return Response(DirectMessageSerializer(msg, context={'me_id': me.id}).data, status=status.HTTP_201_CREATED)


# ============================================================
# Аналитика (только бэкенд, read-only)
# ============================================================

class TeacherCourseAnalyticsView(APIView):
    """
    GET /school/teacher/courses/<course_id>/analytics/ - сводка по курсу
    для его преподавателя: студенты, средний прогресс, распределение
    (завершили/в процессе/не начали), статистика по домашкам.
    """
    permission_classes = [IsAuthenticated, IsDev, IsTeacher]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if not is_course_teacher(request.user, course):
            return Response({'error': 'Это не ваш курс'}, status=status.HTTP_403_FORBIDDEN)

        lessons_total = Lesson.objects.filter(module__course=course).count()
        enrollments = list(course.enrollments.filter(is_active=True))
        students_count = len(enrollments)

        completed = in_progress = not_started = 0
        progress_sum = 0
        for e in enrollments:
            done = LessonProgress.objects.filter(enrollment=e, is_completed=True).count()
            pct = round(done / lessons_total * 100) if lessons_total else 0
            progress_sum += pct
            if pct == 0:
                not_started += 1
            elif pct >= 100:
                completed += 1
            else:
                in_progress += 1

        avg_progress = round(progress_sum / students_count) if students_count else 0

        subs = Submission.objects.filter(assignment__lesson__module__course=course)
        submissions_stats = {
            'submitted': subs.filter(status='submitted').count(),
            'reviewed': subs.filter(status='reviewed').count(),
            'needs_revision': subs.filter(status='needs_revision').count(),
        }

        return Response({
            'course': {'id': course.id, 'title': course.title, 'lessons_total': lessons_total},
            'students_count': students_count,
            'avg_progress': avg_progress,
            'distribution': {
                'completed': completed,
                'in_progress': in_progress,
                'not_started': not_started,
            },
            'submissions': submissions_stats,
        })


class PlatformAnalyticsView(APIView):
    """
    GET /school/analytics/overview/ - общая аналитика по школе.
    Только суперюзер (без IsDev/IsTeacher - это админский обзор).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Только для администратора'}, status=status.HTTP_403_FORBIDDEN)

        courses_total = Course.objects.count()
        courses_active = Course.objects.filter(is_active=True).count()
        enrollments_active = Enrollment.objects.filter(is_active=True).count()
        students_active = Enrollment.objects.filter(is_active=True).values('user').distinct().count()
        teachers_total = CourseTeacher.objects.values('teacher').distinct().count()

        # средняя завершаемость по всем активным доступам
        total_pct = 0
        active = list(Enrollment.objects.filter(is_active=True).select_related('course'))
        for e in active:
            lt = Lesson.objects.filter(module__course=e.course).count()
            done = LessonProgress.objects.filter(enrollment=e, is_completed=True).count()
            total_pct += round(done / lt * 100) if lt else 0
        avg_completion = round(total_pct / len(active)) if active else 0

        return Response({
            'courses_total': courses_total,
            'courses_active': courses_active,
            'enrollments_active': enrollments_active,
            'students_active': students_active,
            'teachers_total': teachers_total,
            'avg_completion': avg_completion,
            'submissions_pending': Submission.objects.filter(status='submitted').count(),
            'forum_threads': ForumThread.objects.count(),
        })
