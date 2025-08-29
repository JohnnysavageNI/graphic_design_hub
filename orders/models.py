from __future__ import annotations

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from services.models import Service
from .storage import ProtectedStorage


class DesignRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    instructions = models.TextField(blank=False)
    uploaded_file = models.FileField(
        upload_to="user_inputs/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    def __str__(self):
        return f"DesignRequest #{self.pk} — {self.service.name}"

    @property
    def uploads_count(self) -> int:
        return self.uploads.count()


class OrderUpload(models.Model):
    request = models.ForeignKey(
        DesignRequest,
        related_name="uploads",
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        storage=ProtectedStorage(),
        upload_to="order_uploads/%Y/%m/%d/",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload #{self.pk} for Request #{self.request_id}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    instructions = models.TextField(blank=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    stripe_pid = models.CharField(
        max_length=255,
        blank=True,
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Order #{self.pk} - {'PAID' if self.is_paid else 'UNPAID'}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="+",
    )
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return f"{self.service} × {self.qty}"


class Upload(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="uploads",
    )
    file = models.FileField(
        upload_to="order_uploads/%Y/%m/%d/",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Upload #{self.pk} for Order #{self.order_id}"
