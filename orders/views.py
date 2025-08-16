from __future__ import annotations
from decimal import Decimal
from typing import Dict

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from cart.utils import build_cart_context
from services.models import Service
from .forms import CheckoutForm
from .models import Order, DesignRequest, OrderUpload

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


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def checkout(request):
    ctx = build_cart_context(request.session)
    cart_items = ctx.get("cart_items", [])
    amount_cents = int(round(float(ctx.get("cart_subtotal") or ctx.get("grand_total") or 0) * 100))

    payment_intent = stripe.PaymentIntent.create(
        amount=max(amount_cents, 0),
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    client_secret = payment_intent.client_secret
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == "POST":
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            created_requests = []
            for item in cart_items:
                dr = DesignRequest.objects.create(
                    user=request.user,
                    service=item["service"],
                    full_name=form.cleaned_data.get("full_name") or request.user.get_username(),
                    email=form.cleaned_data.get("email") or request.user.email,
                    instructions=form.cleaned_data.get("instructions", ""),
                )
                created_requests.append(dr)

            files = request.FILES.getlist("uploaded_files")
            if created_requests and files:
                first_request = created_requests[0]
                for f in files:
                    OrderUpload.objects.create(request=first_request, file=f)

            messages.success(request, "Order submitted. We’ll email you once it’s processed.")
            return redirect("orders:checkout_success", request_id=created_requests[0].id if created_requests else 0)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial = {"full_name": request.user.get_username(), "email": request.user.email}
        form = CheckoutForm(initial=initial)

    return render(
        request,
        "orders/checkout.html",
        {
            **ctx,
            "form": form,
            "stripe_public_key": stripe_public_key,
            "client_secret": client_secret,
        },
    )


@login_required(login_url="/accounts/login/")
def checkout_success(request, request_id: int = None, order_id: int = None):
    pk = request_id if request_id is not None else order_id

    try:
        dr = DesignRequest.objects.get(pk=pk, user=request.user)
        request.session["cart"] = {}
        request.session.modified = True
        return render(request, "orders/success.html", {"design_request": dr})
    except DesignRequest.DoesNotExist:
        pass

    try:
        order = Order.objects.get(pk=pk)
        request.session["cart"] = {}
        request.session.modified = True
        return render(request, "orders/success.html", {"order": order})
    except Order.DoesNotExist:
        return render(
            request,
            "orders/success.html",
            {"not_found_id": pk},
            status=404,
        )


def checkout_cancel(request):
    return render(request, "orders/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    return HttpResponse(status=200)


@login_required(login_url="/accounts/login/")
def download_upload(request, upload_id: int):
    up = get_object_or_404(OrderUpload.objects.select_related("request__user"), pk=upload_id)
    if (up.request.user_id != request.user.id) and (not request.user.is_superuser):
        raise Http404("Not found")
    return FileResponse(up.file.open("rb"), as_attachment=True, filename=up.file.name.rsplit("/", 1)[-1])
