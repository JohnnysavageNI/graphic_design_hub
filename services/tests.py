from django.test import TestCase
from services.models import Service


class ServiceModelTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Logo Design",
            description="High-quality custom logo",
            price=99.99,
            stripe_price_id="price_test_001"
        )

    def test_str_method(self):
        self.assertEqual(str(self.service), "Logo Design")

    def test_service_price_decimal(self):
        self.assertIsInstance(self.service.price, type(99.99))

    def test_service_is_active_default_true(self):
        self.assertTrue(self.service.is_active)
