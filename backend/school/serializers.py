from rest_framework import serializers

from .models import (
    Course, Module, Lesson, LessonMaterial, Enrollment, LessonProgress,
    Assignment, Submission, SubmissionComment, ForumThread, ForumPost,
    DirectMessage,
)


def _display_name(user):
    if not user:
        return 'Usuario eliminado'
    return user.username or user.email


class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = ['id', 'title', 'file']


class LessonAssignmentBriefSerializer(serializers.ModelSerializer):
    """ Короткая карточка задания в списке уроков (без ответа студента). """
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'max_score']


class LessonSerializer(serializers.ModelSerializer):
    """
    Урок с точки зрения студента. Используется только там, где доступ к
    курсу уже проверен (активный Enrollment) - см. CourseDetailView,
    поэтому video_url/content отдаются без дополнительных условий здесь.

    is_completed/last_position_seconds считаются не запросом к БД на
    каждый урок, а через `progress_by_lesson` в context (словарь
    lesson_id -> LessonProgress), который CourseDetailView собирает
    одним запросом на весь курс.
    """
    materials = LessonMaterialSerializer(many=True, read_only=True)
    assignments = LessonAssignmentBriefSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()
    last_position_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'order', 'video_url', 'content', 'duration_minutes',
            'is_free_preview', 'materials', 'assignments', 'is_completed', 'last_position_seconds',
        ]

    def _progress_for(self, obj):
        return self.context.get('progress_by_lesson', {}).get(obj.id)

    def get_is_completed(self, obj):
        progress = self._progress_for(obj)
        return bool(progress and progress.is_completed)

    def get_last_position_seconds(self, obj):
        progress = self._progress_for(obj)
        return progress.last_position_seconds if progress else 0


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons']


class MyCourseSerializer(serializers.ModelSerializer):
    """
    Один курс в списке "Mis cursos" студента - на базе Enrollment, а не
    Course напрямую, потому что именно Enrollment определяет, что
    студент вообще должен видеть этот курс (см. архитектурное решение
    в PLAN_ETAP2.md - доступ выдаёт ProductCourseAccess -> Enrollment).
    """
    id = serializers.IntegerField(source='course.id')
    slug = serializers.SlugField(source='course.slug')
    title = serializers.CharField(source='course.title')
    description = serializers.CharField(source='course.description')
    teachers = serializers.SerializerMethodField()
    lessons_total = serializers.SerializerMethodField()
    lessons_completed = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'slug', 'title', 'description', 'teachers',
            'lessons_total', 'lessons_completed', 'progress_percent',
            'enrolled_at',
        ]

    def get_teachers(self, obj):
        return [
            ct.teacher.username or ct.teacher.email
            for ct in obj.course.course_teachers.select_related('teacher').all()
        ]

    def get_lessons_total(self, obj):
        return Lesson.objects.filter(module__course=obj.course).count()

    def get_lessons_completed(self, obj):
        return LessonProgress.objects.filter(enrollment=obj, is_completed=True).count()

    def get_progress_percent(self, obj):
        total = self.get_lessons_total(obj)
        if not total:
            return 0
        return round(self.get_lessons_completed(obj) / total * 100)


class SubmissionCommentSerializer(serializers.ModelSerializer):
    """ Комментарий под ответом на задание (переписка в ленте ответов). """
    author = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    is_teacher = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionComment
        fields = ['id', 'author', 'author_id', 'is_teacher', 'text', 'created_at']

    def get_author(self, obj):
        return _display_name(obj.author)

    def get_is_teacher(self, obj):
        # teacher_ids кладёт вью одним запросом на курс
        return obj.author_id in self.context.get('teacher_ids', set())


class SubmissionSerializer(serializers.ModelSerializer):
    """ Ответ студента на задание (для кабинета студента). """
    comments = SubmissionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'text', 'file', 'status', 'is_public', 'score',
            'mentor_comment', 'submitted_at', 'reviewed_at', 'comments',
        ]
        read_only_fields = ['id', 'status', 'score', 'mentor_comment', 'submitted_at', 'reviewed_at']


class AnswerFeedSerializer(serializers.ModelSerializer):
    """
    Ответ в ленте «Ответы и комментарии» под заданием: публичные ответы
    студентов курса (+ всегда свой), с автором и комментариями.
    """
    student = serializers.SerializerMethodField()
    student_id = serializers.IntegerField(source='enrollment.user.id', read_only=True)
    is_mine = serializers.SerializerMethodField()
    comments = SubmissionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'student', 'student_id', 'is_mine', 'text', 'file',
            'status', 'is_public', 'score', 'submitted_at', 'comments',
        ]

    def get_student(self, obj):
        return _display_name(obj.enrollment.user)

    def get_is_mine(self, obj):
        return obj.enrollment.user_id == self.context.get('me_id')


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """ Задание + ответ текущего студента (my_submission из context). """
    my_submission = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'max_score', 'my_submission']

    def get_my_submission(self, obj):
        sub = self.context.get('my_submission')
        # прокидываем request дальше, чтобы file отдавался абсолютным URL
        return SubmissionSerializer(sub, context=self.context).data if sub else None


class TeacherSubmissionSerializer(serializers.ModelSerializer):
    """ Сдача глазами ментора - с контекстом (кто, какой курс/задание). """
    student = serializers.SerializerMethodField()
    assignment_title = serializers.CharField(source='assignment.title')
    course_title = serializers.CharField(source='assignment.lesson.module.course.title')
    lesson_title = serializers.CharField(source='assignment.lesson.title')
    max_score = serializers.IntegerField(source='assignment.max_score')

    class Meta:
        model = Submission
        fields = [
            'id', 'student', 'course_title', 'lesson_title', 'assignment_title',
            'max_score', 'text', 'file', 'status', 'score', 'mentor_comment',
            'submitted_at', 'reviewed_at',
        ]

    def get_student(self, obj):
        u = obj.enrollment.user
        return u.username or u.email


class TeacherCourseSerializer(serializers.ModelSerializer):
    """ Курс в кабинете преподавателя: со счётчиками студентов и сдач на проверку. """
    students_count = serializers.SerializerMethodField()
    pending_submissions_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'slug', 'title', 'is_active', 'students_count', 'pending_submissions_count']

    def get_students_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()

    def get_pending_submissions_count(self, obj):
        return Submission.objects.filter(
            assignment__lesson__module__course=obj, status='submitted',
        ).count()


class TeacherStudentProgressSerializer(serializers.ModelSerializer):
    """ Строка ростера: студент курса + его прогресс (на базе Enrollment). """
    student = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    lessons_total = serializers.SerializerMethodField()
    lessons_completed = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user_id', 'student', 'email', 'is_active', 'enrolled_at',
            'lessons_total', 'lessons_completed', 'progress_percent',
        ]

    def get_student(self, obj):
        return obj.user.username or obj.user.email

    def get_lessons_total(self, obj):
        # считается один раз на курс и кладётся в context, чтобы не
        # дёргать БД для каждого студента ростера
        return self.context.get('lessons_total', 0)

    def get_lessons_completed(self, obj):
        return LessonProgress.objects.filter(enrollment=obj, is_completed=True).count()

    def get_progress_percent(self, obj):
        total = self.get_lessons_total(obj)
        if not total:
            return 0
        return round(self.get_lessons_completed(obj) / total * 100)


# ============================================================
# Форум и личные сообщения
# ============================================================

class ForumPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_teacher = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = ['id', 'author', 'author_id', 'is_teacher', 'content', 'created_at']

    def get_author(self, obj):
        return _display_name(obj.author)

    def get_is_teacher(self, obj):
        # автор - препод этого курса? (для метки "преподаватель" в UI)
        teacher_ids = self.context.get('teacher_ids', set())
        return obj.author_id in teacher_ids


class ForumThreadListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumThread
        fields = ['id', 'title', 'author', 'is_pinned', 'is_locked', 'posts_count', 'created_at', 'updated_at']

    def get_author(self, obj):
        return _display_name(obj.author)

    def get_posts_count(self, obj):
        return obj.posts.count()


class ForumThreadDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    posts = ForumPostSerializer(many=True, read_only=True)

    class Meta:
        model = ForumThread
        fields = ['id', 'title', 'author', 'is_pinned', 'is_locked', 'created_at', 'posts']

    def get_author(self, obj):
        return _display_name(obj.author)


class DirectMessageSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender_id', 'content', 'is_read', 'is_mine', 'created_at']

    def get_is_mine(self, obj):
        return obj.sender_id == self.context.get('me_id')
