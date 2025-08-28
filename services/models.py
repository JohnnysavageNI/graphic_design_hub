from django.db import models
from custom_storages import MediaStorage


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(
        storage=MediaStorage(),
        upload_to="service_images/", 
        blank=True, 
        null=True
    )
    stripe_price_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
