from django.urls import path
from . import views
from .webhooks import stripe_webhook

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.checkout_success, name="checkout_success"),
    path("cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("wh/stripe/", views.stripe_webhook, name="stripe_webhook"),
]
