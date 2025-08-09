from __future__ import annotations

from django.contrib import messages
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.views.decorators.http import require_POST

from services.models import Service
from .utils import add_item, build_cart_context


def _is_ajax(request: HttpRequest) -> bool:
    return (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in (request.headers.get("Accept") or "")
    )


def _mutate_cart(session, service_id: int, *, set_to: int | None = None,
                 delta: int | None = None, remove: bool = False) -> None:
    cart = session.get("cart", {})
    key = str(service_id)

    if remove:
        cart.pop(key, None)
        session["cart"] = cart
        return

    if key not in cart:
        if delta is None and set_to is None:
            return
        if set_to is not None:
            cart[key] = set_to
            session["cart"] = cart
            return
        return

    entry = cart[key]

    def get_qty(e) -> int:
        return int(e.get("qty", 0)) if isinstance(e, dict) else int(e)

    def set_qty(e, q: int):
        if isinstance(e, dict):
            e["qty"] = q
        else:
            cart[key] = q

    qty = get_qty(entry)

    if set_to is not None:
        qty = max(0, int(set_to))
    elif delta is not None:
        qty = max(0, qty + int(delta))

    if qty <= 0:
        cart.pop(key, None)
    else:
        set_qty(entry, qty)

    session["cart"] = cart


def view_cart(request: HttpRequest) -> HttpResponse:
    ctx = build_cart_context(request.session)
    return render(request, "cart/cart.html", ctx)


@require_POST
def add_to_cart(request: HttpRequest, service_id: int) -> HttpResponse:
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    add_item(request.session, service_id, qty=1)

    ctx = build_cart_context(request.session)

    # Try to render mini-cart partial if it exists; tolerate absence.
    mini_cart_html = ""
    try:
        mini_cart_html = render_to_string("cart/_mini_cart.html", ctx, request=request)
    except TemplateDoesNotExist:
        mini_cart_html = ""

    toast_html = render_to_string(
        "includes/toasts/toast_success.html",
        {**ctx, "message": f"{service.name} added to your cart."},
        request=request,
    )

    if _is_ajax(request):
        return JsonResponse(
            {
                "mini_cart_html": mini_cart_html,
                "toast_html": toast_html,
                "count": ctx.get("cart_count", 0),
                "subtotal": str(ctx.get("cart_subtotal", "0.00")),
            }
        )

    messages.success(request, toast_html, extra_tags="cart_toast")
    return redirect(request.META.get("HTTP_REFERER") or "service_list")


def mini_cart_fragment(request: HttpRequest) -> JsonResponse:
    ctx = build_cart_context(request.session)
    html = ""
    try:
        html = render_to_string("cart/_mini_cart.html", ctx, request=request)
    except TemplateDoesNotExist:
        html = ""
    return JsonResponse(
        {
            "mini_cart_html": html,
            "count": ctx.get("cart_count", 0),
            "subtotal": str(ctx.get("cart_subtotal", "0.00")),
        }
    )


@require_POST
def decrement_from_cart(request: HttpRequest, service_id: int) -> HttpResponse:
    _mutate_cart(request.session, service_id, delta=-1)
    return redirect("view_cart")


@require_POST
def remove_from_cart(request: HttpRequest, service_id: int) -> HttpResponse:
    _mutate_cart(request.session, service_id, remove=True)
    return redirect("view_cart")
