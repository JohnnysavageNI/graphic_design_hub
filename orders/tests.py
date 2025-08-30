from django.test import TestCase
from django.contrib.auth import get_user_model
from services.models import Service
from orders.models import Order, OrderItem, DesignRequest

User = get_user_model()


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='orderuser',
            password='pass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            instructions='Make it simple.',
            total=150.00,
            stripe_pid='stripe_123'
        )

    def test_str_method_paid(self):
        self.order.is_paid = True
        self.order.save()
        self.assertIn("PAID", str(self.order))

    def test_order_defaults(self):
        self.assertFalse(self.order.is_paid)
        self.assertIsNotNone(self.order.created_at)


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Business Card",
            description="Design business card",
            price=49.99,
            stripe_price_id="pid_456"
        )
        self.order = Order.objects.create(
            full_name='Customer',
            email='cust@example.com'
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            service=self.service,
            qty=2,
            unit_price=49.99,
            line_total=99.98
        )

    def test_str_method(self):
        self.assertIn("Business Card", str(self.item))


class DesignRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='designer', password='pass'
        )
        self.service = Service.objects.create(
            name="Poster",
            description="Poster Design",
            price=60,
            stripe_price_id="pid789"
        )
        self.request = DesignRequest.objects.create(
            user=self.user,
            service=self.service,
            instructions="Make it pop!"
        )

    def test_str_method(self):
        self.assertIn("Poster", str(self.request))

    def test_status_default_pending(self):
        self.assertEqual(self.request.status, "pending")
