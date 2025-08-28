from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from orders import webhooks


class WebhookTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_webhook_missing_secret(self):
        request = self.factory.post("/orders/wh/", data={}, content_type="application/json")
        response = webhooks.stripe_webhook(request)
        self.assertEqual(response.status_code, 400)

    def test_webhook_bad_signature(self):
        request = self.factory.post(
            "/orders/wh/",
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="bad"
        )
        from django.conf import settings
        settings.STRIPE_WH_SECRET = "whsec_test"

        response = webhooks.stripe_webhook(request)
        self.assertEqual(response.status_code, 400)
