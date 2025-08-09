from decimal import Decimal
from typing import Dict, Tuple, List
from django.conf import settings
from services.models import Service


CartDict = Dict[str, int]


SESSION_KEY = getattr(settings, 'CART_SESSION_ID', 'cart')


def get_cart(session) -> CartDict:
    return session.get(SESSION_KEY, {})


def save_cart(session, cart: CartDict) -> None:
    session[SESSION_KEY] = cart
    session.modified = True


def add_item(session, service_id: int, qty: int = 1) -> CartDict:
    cart = get_cart(session)
    sid = str(service_id)
    cart[sid] = cart.get(sid, 0) + qty
    save_cart(session, cart)
    return cart


def remove_item(session, service_id: int) -> CartDict:
    cart = get_cart(session)
    sid = str(service_id)
    if sid in cart:
        del cart[sid]
        save_cart(session, cart)
    return cart


def clear_cart(session) -> None:
    if SESSION_KEY in session:
        del session[SESSION_KEY]
        session.modified = True


def build_cart_context(session):
    cart = get_cart(session)
    ids = [int(k) for k in cart.keys()]
    services = Service.objects.filter(id__in=ids)
    items: List[dict] = []
    subtotal = Decimal('0.00')
    for s in services:
        qty = cart.get(str(s.id), 0)
        line_total = s.price * qty
        subtotal += line_total
        items.append({
            'service': s,
            'qty': qty,
            'line_total': line_total,
        })
    return {
        'cart_items': items,
        'cart_subtotal': subtotal,
        'cart_count': sum(cart.values()),
    }
