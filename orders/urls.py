from django.urls import path
from . import views
from . import webhooks


app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path(
        "success/<int:request_id>/",
        views.checkout_success,
        name="checkout_success",
    ),
    path(
        "success/<int:order_id>/",
        views.checkout_success,
        name="checkout_success_legacy",
    ),
    path("cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("wh/", views.stripe_webhook, name="stripe_webhook"),
    path(
        "download/<int:upload_id>/",
        views.download_upload,
        name="download_upload",
    ),
]
