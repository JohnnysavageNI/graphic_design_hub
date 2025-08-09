from decimal import Decimal
from services.models import Service


CART_SESSION_ID = 'cart'


def cart_contents(request):
    cart = request.session.get(CART_SESSION_ID, {})
    items = []
    subtotal = Decimal('0.00')
    count = 0

    if cart:
        services = Service.objects.filter(id__in=[int(k) for k in cart.keys()])
        by_id = {s.id: s for s in services}
        for sid_str, qty in cart.items():
            sid = int(sid_str)
            s = by_id.get(sid)
            if not s:
                continue
            line_total = s.price * qty
            subtotal += line_total
            count += qty
            items.append({
                'service': s,
                'quantity': qty,
                'line_total': line_total,
            })

    return {
        'cart_items': items,
        'total': subtotal,
        'grand_total': subtotal,
        'item_count': count,
    }
