from django.test import TestCase, Client
from django.urls import reverse
from services.models import Service


class CartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name="Website Design",
            description="Custom responsive website",
            price=200.00,
            stripe_price_id="stripe_web_001"
        )

    def test_add_to_cart(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.service.id]),
            data={'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        cart = session.get('cart', {})
        self.assertIn(str(self.service.id), cart)
        print(cart)
        self.assertEqual(cart[str(self.service.id)], 1)

    def test_remove_from_cart(self):
        session = self.client.session
        session['cart'] = {
            str(self.service.id): {
                'quantity': 1,
                'price': str(self.service.price)
            }
        }
        session.save()

        response = self.client.post(
            reverse('remove_from_cart', args=[self.service.id])
        )
        self.assertEqual(response.status_code, 302)

        updated_cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.service.id), updated_cart)
