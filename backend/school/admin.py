from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from mentored.models import Course as StoreCourse

from .models import (
    TeacherProfile, Course, ProductCourseAccess, CourseTeacher, Module, Lesson,
    LessonMaterial, Enrollment, LessonProgress, Assignment, Submission,
    SubmissionComment, Certificate, ForumThread, ForumPost, DirectMessage,
)


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} — S/ {obj.price} (ID {obj.pk})'


class ProductCourseAccessForm(forms.ModelForm):
    """
    Вместо голого "Тип товара" + "ID товара" - выпадающий список реальных
    товаров с названием и ценой. Пока в магазине единственный тип товара,
    который можно связать с учебным курсом, - mentored.Course (см. модель
    ProductCourseAccess) - когда появится второй тип, этот список нужно
    будет расширить (например, отдельным полем "тип товара" над списком).
    """
    product = ProductChoiceField(
        queryset=StoreCourse.objects.all().order_by('name'),
        label='Товар (курс в магазине)',
    )

    class Meta:
        model = ProductCourseAccess
        fields = ['product', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.object_id:
            self.fields['product'].initial = self.instance.object_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_type = ContentType.objects.get_for_model(StoreCourse)
        instance.object_id = self.cleaned_data['product'].pk
        if commit:
            instance.save()
        return instance


class TeacherScopedAdminMixin:
    """
    Ограничивает то, что видит в этой админке пользователь с ролью
    teacher (не суперюзер): только объекты, относящиеся к курсам,
    которые он ведёт (school.CourseTeacher). Суперюзер и staff без роли
    teacher видят всё как раньше - это не сужает админку в целом, а
    именно закрывает ментору доступ к чужим курсам/студентам/работам.

    course_lookup - путь ORM от модели этой админки до school.Course,
    например '' для самой Course, 'course' для Module, 'module__course'
    для Lesson и т.д.
    """
    course_lookup = ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or not user.is_teacher:
            return qs
        prefix = f"{self.course_lookup}__" if self.course_lookup else ""
        return qs.filter(**{f"{prefix}course_teachers__teacher": user}).distinct()


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_public', 'created_at')
    list_filter = ('is_public',)
    search_fields = ('user__email', 'user__username', 'specialization')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        # Отдельный случай - тут нет course_teachers, ограничиваем сразу
        # по владельцу профиля: ментор видит и редактирует только свою
        # карточку, не чужие.
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or not user.is_teacher:
            return qs
        return qs.filter(user=user)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('title', 'order')


class CourseTeacherInline(admin.TabularInline):
    model = CourseTeacher
    extra = 0


class ProductCourseAccessInline(admin.TabularInline):
    """
    Привязка товаров, открывающих доступ к этому курсу. Прямо здесь, на
    странице курса, а не отдельным экраном - привязка настраивается там
    же, где заводится сам курс.
    """
    model = ProductCourseAccess
    form = ProductCourseAccessForm
    extra = 0
    fields = ('product',)


@admin.register(Course)
class CourseAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = ''
    list_display = ('title', 'creator', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModuleInline, CourseTeacherInline, ProductCourseAccessInline]


@admin.register(ProductCourseAccess)
class ProductCourseAccessAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'course'
    """
    Отдельный экран на случай, когда удобнее искать не "от курса", а "от
    товара" - например, у какого-то товара уже есть привязка или нет.
    """
    form = ProductCourseAccessForm
    list_display = ('course', 'product_display', 'created_at')
    list_filter = ('course',)
    search_fields = ('course__title',)
    readonly_fields = ('created_at',)

    def product_display(self, obj):
        return str(obj.product) if obj.product else '—'
    product_display.short_description = 'Товар'


@admin.register(CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'assigned_at')
    list_filter = ('course',)
    search_fields = ('course__title', 'teacher__email')

    def get_queryset(self, request):
        # Особый случай - это сама таблица назначений, ограничиваем
        # напрямую по teacher, а не через course_teachers (это она и
        # есть), иначе ментор видел бы и других менторов на своих курсах.
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or not user.is_teacher:
            return qs
        return qs.filter(teacher=user)


class LessonMaterialInline(admin.TabularInline):
    model = LessonMaterial
    extra = 0


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ('title', 'max_score')


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('title', 'order', 'is_free_preview', 'duration_minutes')


@admin.register(Module)
class ModuleAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'course'
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'module__course'
    list_display = ('title', 'module', 'order', 'duration_minutes', 'is_free_preview')
    list_filter = ('module__course', 'is_free_preview')
    search_fields = ('title', 'module__title')
    inlines = [LessonMaterialInline, AssignmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'course'
    list_display = ('user', 'course', 'is_active', 'enrolled_at')
    list_filter = ('is_active', 'course', 'enrolled_at')
    search_fields = ('user__email', 'course__title')
    date_hierarchy = 'enrolled_at'


@admin.register(LessonProgress)
class LessonProgressAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'enrollment__course'
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('enrollment__user__email', 'lesson__title')


@admin.register(Certificate)
class CertificateAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'enrollment__course'
    list_display = ('enrollment', 'issued_at')
    search_fields = ('enrollment__user__email', 'enrollment__course__title')
    date_hierarchy = 'issued_at'
    readonly_fields = ('enrollment', 'issued_at')


@admin.register(Assignment)
class AssignmentAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'lesson__module__course'
    list_display = ('title', 'lesson', 'max_score')
    search_fields = ('title', 'lesson__title')


class SubmissionCommentInline(admin.TabularInline):
    model = SubmissionComment
    extra = 0
    fields = ('author', 'text', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Submission)
class SubmissionAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'assignment__lesson__module__course'
    list_display = ('assignment', 'enrollment', 'status', 'is_public', 'score', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'is_public', 'submitted_at')
    search_fields = ('enrollment__user__email', 'assignment__title')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('assignment', 'enrollment', 'text', 'file', 'submitted_at')
    inlines = [SubmissionCommentInline]


@admin.register(SubmissionComment)
class SubmissionCommentAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'submission__assignment__lesson__module__course'
    list_display = ('submission', 'author', 'created_at')
    search_fields = ('author__email', 'text', 'submission__assignment__title')


class ForumPostInline(admin.TabularInline):
    model = ForumPost
    extra = 0
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ForumThread)
class ForumThreadAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'course'
    list_display = ('title', 'course', 'author', 'is_pinned', 'is_locked', 'updated_at')
    list_filter = ('is_pinned', 'is_locked', 'course')
    search_fields = ('title', 'course__title', 'author__email')
    inlines = [ForumPostInline]


@admin.register(ForumPost)
class ForumPostAdmin(TeacherScopedAdminMixin, admin.ModelAdmin):
    course_lookup = 'thread__course'
    list_display = ('thread', 'author', 'created_at')
    search_fields = ('thread__title', 'author__email', 'content')


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'recipient__email', 'content')
    readonly_fields = ('sender', 'recipient', 'content', 'created_at')
