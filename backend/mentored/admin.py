from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, BlogCategory, BlogPost, FAQ, Testimonial, Book, Course, Consultation, Membership, \
    Cart, CartItem, ContactMessage

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'phone',
        'avatar_preview',
        'is_active',
        'is_staff',
        'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'phone', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('created_at', 'updated_at', 'avatar_preview')

    fieldsets = (
        ('Основное', {
            'fields': ('email', 'username', 'password')
        }),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'avatar_preview')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url
            )
        return '—'
    avatar_preview.short_description = 'Аватар'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'author',
        'image_preview',
        'is_published',
        'created_at'
    )
    list_filter = ('category', 'is_published', 'author')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('is_published',)

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'category', 'author', 'is_published')
        }),
        ('Контент', {
            'fields': ('short_description', 'content')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview', 'file')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:100px;max-height:60px;object-fit:cover;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Превью'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('is_active',)
    ordering = ('id',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'author_role',
        'author_initial',
        'author_image_preview',
        'is_active',
        'is_featured',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured')
    search_fields = ('author', 'text', 'author_role')
    list_editable = ('is_active', 'is_featured')
    readonly_fields = ('created_at', 'updated_at', 'author_image_preview')

    def author_image_preview(self, obj):
        if obj.author_image:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                obj.author_image.url
            )
        return '—'
    author_image_preview.short_description = 'Фото'


class BaseProductAdmin(admin.ModelAdmin):
    """Базовый класс для всех товаров"""
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('price', 'old_price', 'is_active', 'is_featured')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:80px;max-height:60px;object-fit:cover;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Превью'


@admin.register(Book)
class BookAdmin(BaseProductAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'old_price',
        'book_format',
        'pages',
        'image_preview',
        'is_active',
        'is_featured',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured', 'book_format', 'book_language')
    search_fields = ('name', 'short_description', 'description', 'author')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'short_description', 'description', 'long_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview')
        }),
        ('Характеристики книги', {
            'fields': ('book_format', 'pages', 'book_language', 'year', 'book_file')
        }),
        ('Что входит', {
            'fields': ('includes',)
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(BaseProductAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'old_price',
        'duration',
        'lessons',
        'certificate',
        'image_preview',
        'is_active',
        'is_featured',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured', 'certificate', 'level')
    search_fields = ('name', 'short_description', 'description')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'short_description', 'description', 'long_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview')
        }),
        ('Характеристики курса', {
            'fields': ('duration', 'lessons', 'video_hours', 'level', 'certificate')
        }),
        ('Что входит', {
            'fields': ('includes',)
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Consultation)
class ConsultationAdmin(BaseProductAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'old_price',
        'duration_minutes',
        'expert',
        'image_preview',
        'is_active',
        'is_featured',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'short_description', 'description', 'expert')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'short_description', 'description', 'long_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview')
        }),
        ('Характеристики консультации', {
            'fields': ('duration_minutes', 'expert', 'platform', 'languages')
        }),
        ('Что входит', {
            'fields': ('includes',)
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Membership)
class MembershipAdmin(BaseProductAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'old_price',
        'cycle',
        'cancel_anytime',
        'image_preview',
        'is_active',
        'is_featured',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured', 'cancel_anytime')
    search_fields = ('name', 'short_description', 'description')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'short_description', 'description', 'long_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Медиа', {
            'fields': ('image', 'image_preview')
        }),
        ('Характеристики мембершипа', {
            'fields': ('cycle', 'cancel_anytime')
        }),
        ('Что входит', {
            'fields': ('includes',)
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'Товаров'

    def total_price(self, obj):
        return f"${obj.total_price:.2f}"
    total_price.short_description = 'Сумма'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product_name', 'quantity', 'total_price', 'created_at')
    search_fields = ('cart__user__email', 'cart__user__username')
    list_filter = ('content_type',)
    readonly_fields = ('created_at', 'updated_at')

    def product_name(self, obj):
        return str(obj.product) if obj.product else 'Товар удалён'
    product_name.short_description = 'Товар'

    def total_price(self, obj):
        return f"${obj.total_price:.2f}"
    total_price.short_description = 'Сумма'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'motivo', 'is_read', 'created_at')
    list_filter = ('motivo', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'motivo', 'message', 'created_at')
    list_editable = ('is_read',)
