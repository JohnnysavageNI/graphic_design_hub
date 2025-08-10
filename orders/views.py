# orders/views.py
from __future__ import annotations
from decimal import Decimal
from typing import Dict, List

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from cart.utils import build_cart_context
from services.models import Service
from .forms import CheckoutForm
from .models import Order, OrderItem, Upload

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def _cart_items_from_ctx(ctx: Dict) -> list[dict]:
    items = []
    for raw in ctx.get("cart_items", []):
        service: Service = raw["service"]
        qty = int(raw.get("qty") or 1)
        unit_price = Decimal(str(service.price))
        line_total = Decimal(str(raw.get("line_total") or unit_price * qty))
        items.append({"service": service, "qty": qty, "unit_price": unit_price, "line_total": line_total})
    return items


@require_http_methods(["GET", "POST"])
def checkout(request: HttpRequest) -> HttpResponse:
    cart_ctx = build_cart_context(request.session)
    items = _cart_items_from_ctx(cart_ctx)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("view_cart")

    grand_total = Decimal(str(cart_ctx.get("cart_subtotal") or cart_ctx.get("grand_total") or "0"))
    amount_cents = int(grand_total * 100)

    if request.method == "POST":
        payment_intent_id = request.POST.get("payment_intent_id")
        form = CheckoutForm(request.POST, request.FILES)
        if not payment_intent_id:
            messages.error(request, "Payment was not completed. Please try again.")
        elif form.is_valid():
            paid_ok = False
            try:
                pi = stripe.PaymentIntent.retrieve(payment_intent_id)
                paid_ok = (pi.status == "succeeded")
            except Exception:
                paid_ok = False

            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                instructions=form.cleaned_data.get("instructions", "").strip(),
                total=grand_total,
                stripe_pid=payment_intent_id,
                is_paid=bool(paid_ok),
            )
            for it in items:
                OrderItem.objects.create(
                    order=order,
                    service=it["service"],
                    qty=it["qty"],
                    unit_price=it["unit_price"],
                    line_total=it["line_total"],
                )
            for f in request.FILES.getlist("files"):
                Upload.objects.create(order=order, file=f)

            request.session["cart"] = {}
            request.session.modified = True

            if paid_ok:
                messages.success(request, f"Payment complete. Order #{order.id} created.")
            else:
                messages.warning(request, "Payment pending/failed. We recorded your order and will verify payment.")
            return redirect(reverse("orders:checkout_success", args=[order.id]))
    else:
        form = CheckoutForm(initial=({
            "full_name": (getattr(request.user, "get_full_name", lambda: "")() or request.user.username),
            "email": request.user.email} if request.user.is_authenticated else {}))

    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=getattr(settings, "STRIPE_CURRENCY", "usd"),
        automatic_payment_methods={"enabled": True},
        metadata={"cart_total": str(grand_total)},
    )

    return render(
        request,
        "orders/checkout.html",
        {
            **cart_ctx,
            "form": form,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "client_secret": intent.client_secret,
        },
    )


def checkout_success(request, order_id: int):
    from .models import Order
    order = get_object_or_404(Order, pk=order_id)
    request.session["cart"] = {}
    request.session.modified = True
    return render(request, "orders/success.html", {"order": order})


def checkout_cancel(request):
    return render(request, "orders/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    return HttpResponse(status=200)
