from django.contrib import admin

from .models import (
    TeacherProfile, Course, ProductCourseAccess, CourseTeacher, Module, Lesson,
    LessonMaterial, Enrollment, LessonProgress, Assignment, Submission,
)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_public', 'created_at')
    list_filter = ('is_public',)
    search_fields = ('user__email', 'user__username', 'specialization')
    readonly_fields = ('created_at', 'updated_at')


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
    extra = 0
    fields = ('content_type', 'object_id')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModuleInline, CourseTeacherInline, ProductCourseAccessInline]


@admin.register(ProductCourseAccess)
class ProductCourseAccessAdmin(admin.ModelAdmin):
    """
    Отдельный экран на случай, когда удобнее искать не "от курса", а "от
    товара" - например, у какого-то товара уже есть привязка или нет.
    Выбор товара пока через content_type + object_id (тип + ID) - без
    красивого автокомплита, это можно улучшить отдельно, когда появится
    реальная потребность (сейчас только один тип товара - mentored.Course).
    """
    list_display = ('course', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'course')
    search_fields = ('course__title',)
    readonly_fields = ('created_at',)


@admin.register(CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'assigned_at')
    list_filter = ('course',)
    search_fields = ('course__title', 'teacher__email')


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
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration_minutes', 'is_free_preview')
    list_filter = ('module__course', 'is_free_preview')
    search_fields = ('title', 'module__title')
    inlines = [LessonMaterialInline, AssignmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_active', 'enrolled_at')
    list_filter = ('is_active', 'course', 'enrolled_at')
    search_fields = ('user__email', 'course__title')
    date_hierarchy = 'enrolled_at'


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('enrollment__user__email', 'lesson__title')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'max_score')
    search_fields = ('title', 'lesson__title')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'enrollment', 'status', 'score', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('enrollment__user__email', 'assignment__title')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('assignment', 'enrollment', 'text', 'file', 'submitted_at')
