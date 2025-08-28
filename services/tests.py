from django.test import TestCase
from services.models import Service


def create_test_service(name="Test Service"):
    return Service.objects.create(
        name=name,
        description="desc",
        price=1.00,
        stripe_price_id="test_123"
    )


class ServiceModelTest(TestCase):
    def test_str_method(self):
        service = create_test_service("Logo Design")
        self.assertEqual(str(service), "Logo Design")
