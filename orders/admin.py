from django.contrib import admin
from .models import DesignRequest


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'status')
    list_filter = ('status',)
