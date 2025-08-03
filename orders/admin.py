from django.contrib import admin
from .models import DesignRequest


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'service__name')
