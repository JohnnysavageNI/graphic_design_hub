import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from .models import Service


def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/service_list.html', {'services': services})


def create_checkout_session(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': service.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/services/success/'),
        cancel_url=request.build_absolute_uri('/services/cancel/'),
    )
    return redirect(checkout_session.url)


def success(request):
    return render(request, 'services/success.html')


def cancel(request):
    return render(request, 'services/cancel.html')


def add_to_cart(request, service_id):
    cart = request.session.get('cart', [])
    if service_id not in cart:
        cart.append(service_id)
    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', [])
    services = Service.objects.filter(id__in=cart)
    total = sum(s.price for s in services)
    return render(request, 'services/cart.html', {
        'services': services,
        'total': total
    })
