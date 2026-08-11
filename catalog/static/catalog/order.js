document.addEventListener("DOMContentLoaded", () => {
  // Logic to add/remove item from order
  function getCookie(name) {
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));

    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  }

  const csrfToken = getCookie("csrftoken");

  const addButton = document.getElementById("add-button");

  if (addButton) {
    const checkoutContainer = document.getElementById("checkout-container");
    const quantityCounter = document.getElementById("item-quantity");

    const itemId = addButton.dataset.itemId;
    let isPending = false;

    async function addItemToOrder(id) {
      try {
        const response = await fetch(`/order/add/${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          credentials: "same-origin",
        });

        if (!response.ok) {
          console.error(await response.text());
          return null;
        }

        return await response.json();
      } catch (err) {
        console.error("Network error", err);
        return null;
      }
    }

    async function handleAddItem() {
      if (isPending) return;

      isPending = true;

      const result = await addItemToOrder(itemId);

      if (result) {
        if (quantityCounter) {
          quantityCounter.textContent = result.item.quantity;
        }

        mountCheckoutButton(result.id);
      }

      isPending = false;
    }

    addButton.addEventListener("click", handleAddItem);

    function mountCheckoutButton(orderId) {
      if (!checkoutContainer || !orderId) return;

      if (document.getElementById("checkout-link")) return;

      const checkoutLink = document.createElement("a");

      checkoutLink.id = "checkout-link";
      checkoutLink.href = `/order/details/${orderId}`;
      checkoutLink.textContent = "Checkout";

      checkoutContainer.appendChild(checkoutLink);
    }
  }

  // Logic to remove order
  const removeOrderButton = document.getElementById("remove-order-btn");

  if (removeOrderButton) {
    removeOrderButton.addEventListener("click", async () => {
      try {
        const response = await fetch("/order/remove", {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
          },
          credentials: "same-origin",
        });

        if (!response.ok) {
          console.error(await response.text());
          return;
        }

        window.location.reload();
      } catch (err) {
        console.error("Network error", err);
      }
    });
  }
});
