from django.contrib import admin
from django.utils.html import format_html
from .models import EmailLog, EmailTemplate


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email_type', 'recipient_email', 'subject',
        'status_colored', 'created_at', 'sent_at',
    )
    list_filter = ('status', 'email_type', 'created_at')
    search_fields = ('recipient_email', 'subject', 'error_message')
    readonly_fields = ('created_at', 'sent_at', 'error_message')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Получатель', {
            'fields': ('recipient_email', 'recipient_user')
        }),
        ('Письмо', {
            'fields': ('email_type', 'subject')
        }),
        ('Связи', {
            'fields': ('related_order', 'related_course', 'related_product'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('status', 'error_message', 'created_at', 'sent_at')
        }),
    )

    def status_colored(self, obj):
        colors = {
            'pending': '#8a5a00',
            'sent': '#1f7a3d',
            'failed': '#8e1519',
        }
        return format_html(
            '<span style="color:{};font-weight:600;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display(),
        )
    status_colored.short_description = 'Статус'

    def has_add_permission(self, request):
        # Логи создаются автоматически, вручную не нужны
        return False


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'subject', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'name', 'subject')
    prepopulated_fields = {'code': ('name',)}