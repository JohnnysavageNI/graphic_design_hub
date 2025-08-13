# orders/webhook_handler.py
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, TemplateDoesNotExist

from .models import Order


class StripeWHHandler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(content=f"Unhandled event: {event['type']}", status=200)

    def _send_confirmation_email(self, order: Order) -> None:
        context = {"order": order}
        try:
            subject = render_to_string("orders/email_confirmation_subject.txt", context).strip()
            body = render_to_string("orders/email_confirmation.txt", context)
        except TemplateDoesNotExist:
            subject = f"Order #{order.id} payment received"
            lines = [f"Thanks! We received your payment for order #{order.id}.", "", "Summary:"]
            for it in order.items.all():
                lines.append(f"- {it.service.name} × {it.qty} = ${it.line_total:.2f}")
            lines.append(f"\nTotal: ${order.total:.2f}")
            body = "\n".join(lines)

        send_mail(
            subject,
            body,
            getattr(settings, "DEFAULT_FROM_EMAIL", None),
            [order.email],
            fail_silently=True,
        )

    def handle_payment_intent_succeeded(self, event):
        """Mark order paid when Stripe confirms the PaymentIntent."""
        intent = event["data"]["object"]
        pid = intent.get("id")

        try:
            order = Order.objects.select_related().prefetch_related("items").get(stripe_pid=pid)
        except Order.DoesNotExist:
            return HttpResponse(content="PI succeeded but order not found", status=200)

        if not order.is_paid:
            order.is_paid = True
            order.save(update_fields=["is_paid"])
            self._send_confirmation_email(order)

        return HttpResponse(content=f"Order #{order.id} marked paid", status=200)

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(content="Payment failed event received", status=200)
