from rest_framework import serializers

from .models import (
    Course, Module, Lesson, LessonMaterial, Enrollment, LessonProgress,
    Assignment, Submission,
)


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


class SubmissionSerializer(serializers.ModelSerializer):
    """ Ответ студента на задание (для кабинета студента). """
    class Meta:
        model = Submission
        fields = [
            'id', 'text', 'file', 'status', 'score', 'mentor_comment',
            'submitted_at', 'reviewed_at',
        ]
        read_only_fields = ['id', 'status', 'score', 'mentor_comment', 'submitted_at', 'reviewed_at']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """ Задание + ответ текущего студента (my_submission из context). """
    my_submission = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'max_score', 'my_submission']

    def get_my_submission(self, obj):
        sub = self.context.get('my_submission')
        return SubmissionSerializer(sub).data if sub else None


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
    email = serializers.EmailField(source='user.email')
    lessons_total = serializers.SerializerMethodField()
    lessons_completed = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'email', 'is_active', 'enrolled_at',
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
