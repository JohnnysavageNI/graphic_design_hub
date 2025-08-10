from django.contrib import admin
from .models import Order, OrderItem, Upload, DesignRequest, OrderUpload


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("service", "qty", "unit_price", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "total", "is_paid", "created_at")
    list_filter = ("is_paid", "created_at")
    search_fields = ("id", "email", "stripe_pid")
    inlines = [OrderItemInline]


admin.site.register(Upload)
admin.site.register(DesignRequest)
admin.site.register(OrderUpload)
