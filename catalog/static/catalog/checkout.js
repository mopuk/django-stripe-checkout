document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("payment-form");

  const stripeKey = form.dataset.stripeKey;
  const orderId = form.dataset.orderId;

  const stripe = Stripe(stripeKey);

  function getCookie(name) {
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  }

  const csrfToken = getCookie("csrftoken");

  async function initialize() {
    const response = await fetch(`/buy/${orderId}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    });

    const { clientSecret } = await response.json();

    const elements = stripe.elements({ clientSecret });
    const paymentElement = elements.create("payment");

    paymentElement.mount("#payment-element");

    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: window.location.origin + `/order/success/${orderId}`,
        },
      });
      if (error) {
        console.error(error.message);
      }
    });
  }
  initialize();
});
