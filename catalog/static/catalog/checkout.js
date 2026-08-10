const buyButton = document.getElementById("buy-button");

const itemId = buyButton.dataset.itemId;
const stripeKey = buyButton.dataset.stripeKey;

const stripe = Stripe(stripeKey);
buyButton.addEventListener("click", async () => {
  const response = await fetch(`/buy/${itemId}`);
  const session = await response.json();

  await stripe.redirectToCheckout({ sessionId: session.id });
});
