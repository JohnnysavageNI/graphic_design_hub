from django.test import TestCase
from django.urls import reverse
from services.models import Service


class CartTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Poster",
            description="desc",
            price=10.00,
            stripe_price_id="test_456",
        )

    def test_add_to_cart(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.service.id])
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart", {})
        self.assertIn(str(self.service.id), cart)

    def test_remove_from_cart(self):
        self.client.post(reverse("add_to_cart", args=[self.service.id]))
        response = self.client.post(
            reverse("remove_from_cart", args=[self.service.id])
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart", {})
        self.assertNotIn(str(self.service.id), cart)
