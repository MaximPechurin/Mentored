from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_link', 'user', 'transaction_id', 'status',
        'amount', 'payment_method', 'created_at', 'paid_at',
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'user__email', 'order__order_number')
    date_hierarchy = 'created_at'
    readonly_fields = (
        'user', 'order', 'transaction_id', 'amount', 'payment_method',
        'payment_response', 'created_at', 'updated_at', 'paid_at',
    )

    def order_link(self, obj):
        return obj.order.order_number if obj.order else '-'
    order_link.short_description = 'Заказ'
