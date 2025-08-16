(function () {
  const form = document.getElementById("payment-form");
  if (!form) return;

  function readJSON(id) {
    const el = document.getElementById(id);
    return el ? JSON.parse(el.textContent) : null;
  }

  const stripePublicKey = readJSON("id_stripe_public_key");
  const clientSecret    = readJSON("id_client_secret");

  if (!window.Stripe) {
    console.error("Stripe.js not loaded. Ensure <script src='https://js.stripe.com/v3/'></script> is in base.html before this file.");
    return;
  }
  if (!stripePublicKey) {
    console.error("Missing stripe_public_key JSON script on the page.");
    return;
  }
  if (!clientSecret) {
    console.error("Missing client_secret JSON script on the page.");
    return;
  }

  const stripe   = Stripe(stripePublicKey);
  const elements = stripe.elements();

  const style = {
    base: {
      color: "#000",
      fontFamily: '"Lato", "Helvetica Neue", Arial, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": { color: "#666" },
    },
    invalid: { color: "#dc3545", iconColor: "#dc3545" },
  };

  const card = elements.create("card", { style, hidePostalCode: true });

  const cardElement = document.getElementById("card-element");
  if (!cardElement) {
    console.error("No #card-element container in the template.");
    return;
  }

  card.mount("#card-element");

  const errorEl = document.getElementById("card-errors");
  card.on("change", function (event) {
    if (errorEl) errorEl.textContent = event.error ? event.error.message : "";
  });

  const submitBtn = document.getElementById("submit-button");
  function setLoading(loading) {
    if (!submitBtn) return;
    submitBtn.disabled = !!loading;
    submitBtn.innerText = loading ? "Processing…" : "Pay Now";
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    setLoading(true);
    if (errorEl) errorEl.textContent = "";

    try {
      const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            name: (form.querySelector('[name="full_name"]') || {}).value || "",
            email: (form.querySelector('[name="email"]') || {}).value || "",
          },
        },
      });

      if (result.error) {
        if (errorEl) errorEl.textContent = result.error.message || "Payment error.";
        setLoading(false);
        return;
      }

      if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
        form.submit();
      } else {
        if (errorEl) errorEl.textContent = "Payment was not completed. Please try again.";
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      if (errorEl) errorEl.textContent = "Unexpected error. Please try again.";
      setLoading(false);
    }
  });
})();
