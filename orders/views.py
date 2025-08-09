from decimal import Decimal
import stripe
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from services.models import Service
from .models import DesignRequest
from .forms import CheckoutForm

CART_SESSION_ID = 'cart'
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = request.session.get(CART_SESSION_ID, {})
    if not cart:
        return redirect('view_cart')

    services = Service.objects.filter(id__in=[int(k) for k in cart.keys()])
    subtotal = sum((s.price * cart.get(str(s.id), 0)) for s in services)
    amount_cents = int((subtotal * Decimal('100')).quantize(Decimal('1')))

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            dr = form.save(commit=False)
            dr.user = request.user
            dr.service = services.first()
            dr.status = 'pending'
            dr.save()

            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'design_request_id': str(dr.id),
                    'user_id': str(request.user.id),
                    'services': ",".join([str(s.id) for s in services]),
                }
            )

            request.session['pi_id'] = intent['id']

            context = {
                'form': form,
                'services': services,
                'total': subtotal,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                'client_secret': intent['client_secret'],
            }
            return render(request, 'orders/checkout.html', context)
    else:
        form = CheckoutForm()

    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency='usd',
        metadata={'preview': 'true'}
    )

    context = {
        'form': form,
        'services': services,
        'total': subtotal,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent['client_secret'],
    }
    return render(request, 'orders/checkout.html', context)


def checkout_success(request):
    return render(request, 'orders/checkout_success.html')


def checkout_cancel(request):
    return render(request, 'orders/checkout_cancel.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    if event['type'] == 'payment_intent.succeeded':
        pi = event['data']['object']
        dr_id = pi.get('metadata', {}).get('design_request_id')
        if dr_id:
            try:
                dr = DesignRequest.objects.get(id=dr_id)
                dr.status = 'completed'
                dr.save()
            except DesignRequest.DoesNotExist:
                pass

    return HttpResponse(status=200)
