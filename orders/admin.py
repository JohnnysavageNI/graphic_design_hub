from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import DesignRequest, OrderUpload


class OrderUploadInline(admin.TabularInline):
    model = OrderUpload
    extra = 1
    fields = ("file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "user", "status", "uploads_count")
    list_filter = ("status", "service")
    search_fields = ("id", "user__username", "full_name", "email", "service__name")
    inlines = [OrderUploadInline]

    fields = ("user", "service", "full_name", "email", "instructions", "status")
    readonly_fields = ("user", "service", "full_name", "email", "instructions")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj: DesignRequest = form.instance
        if obj.status == "completed" and obj.uploads.count() == 0:
            raise ValidationError("Cannot mark as Completed without at least one uploaded deliverable.")
