(function () {
  const pubEl = document.getElementById('id_stripe_public_key');
  const secEl = document.getElementById('id_client_secret');
  const form = document.getElementById('payment-form');
  const submitBtn = document.getElementById('submit-button');
  const cardErrors = document.getElementById('card-errors');
  const piInput = document.getElementById('payment_intent_id');

  if (!pubEl || !secEl || !form) return;

  const stripePublicKey = JSON.parse(pubEl.textContent);
  const clientSecret = JSON.parse(secEl.textContent);

  const stripe = Stripe(stripePublicKey, { locale: 'en-GB' });
  const elements = stripe.elements();

  const style = {
    base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': { color: '#6c757d' }
    },
    invalid: { color: '#dc3545', iconColor: '#dc3545' }
  };

  const card = elements.create('card', { hidePostalCode: true, style });
  card.mount('#card-element');

  card.on('change', function (event) {
    if (!cardErrors) return;
    cardErrors.textContent = event.error ? (event.error.message || 'Invalid card details') : '';
  });

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (submitBtn) submitBtn.disabled = true;

    const fullName = document.getElementById('id_full_name')?.value || '';
    const email = document.getElementById('id_email')?.value || '';

    const { paymentIntent, error } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: { card, billing_details: { name: fullName, email } }
    });

    if (error) {
      if (cardErrors) cardErrors.textContent = error.message || 'Payment failed. Please check your card details.';
      if (submitBtn) submitBtn.disabled = false;
      return;
    }

    if (paymentIntent && paymentIntent.status === 'succeeded') {
      if (piInput) piInput.value = paymentIntent.id;
      form.submit();
    } else {
      if (cardErrors) cardErrors.textContent = 'Payment was not completed. Please try again.';
      if (submitBtn) submitBtn.disabled = false;
    }
  });
})();