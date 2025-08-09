from django.db import models
from django.conf import settings
from services.models import Service


class DesignRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    instructions = models.TextField()  # ← must exist
    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)  # ← must exist

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self) -> str:
        return f"DesignRequest from {self.full_name or self.user}"


class OrderUpload(models.Model):
    """Files attached to the final order/request after payment succeeds."""
    request = models.ForeignKey(DesignRequest, related_name='uploads', on_delete=models.CASCADE)
    file = models.FileField(upload_to='order_uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
