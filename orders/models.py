from django.db import models
from django.conf import settings
from services.models import Service


class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to='client_uploads/', blank=True, null=True)
    delivered_file = models.FileField(upload_to='designs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} for {self.user.username} ({self.status})"
