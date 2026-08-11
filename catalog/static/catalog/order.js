document.addEventListener("DOMContentLoaded", () => {
  const addButton = document.getElementById("add-button");
  const checkoutContainer = document.getElementById("checkout-container");
  const itemId = addButton.dataset.itemId;
  let isPending = false;

  function getCookie(name) {
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  }

  const csrfToken = getCookie("csrftoken");

  async function handleItem(id, action) {
    const url = action == "add" ? `/order/add/${id}` : `/order/remove/${id}`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "same-origin",
      });

      if (!response.ok) {
        console.error((await response).statusText);
        return null;
      }
      return await response.json();
    } catch (err) {
      console.error("Network error", err);
      return null;
    }
  }

  async function handleRemoveItem(e) {
    if (isPending) return;
    isPending = true;

    const isRemoved = await handleItem(itemId, "remove");

    if (!isRemoved) return;

    addButton.removeEventListener("click", handleRemoveItem);
    addButton.addEventListener("click", handleAddItem);
    addButton.textContent = "Add to order";
    unmountCheckoutButton();
    isPending = false;
  }
  async function handleAddItem(e) {
    if (isPending) return;
    isPending = true;
    const isAdded = await handleItem(itemId, "add");
    if (!isAdded) return;

    addButton.removeEventListener("click", handleAddItem);
    addButton.addEventListener("click", handleRemoveItem);
    addButton.textContent = "Remove from order";
    mountCheckoutButton(isAdded.id);
    isPending = false;
  }

  addButton.addEventListener("click", handleAddItem);

  function mountCheckoutButton(orderId) {
    if (!checkoutContainer) return;
    if (!orderId) return;

    if (document.getElementById("checkout-link")) return;

    const checkoutLink = document.createElement("a");
    checkoutLink.id = "checkout-link";
    checkoutLink.href = `/order/details/${orderId}`;
    checkoutLink.textContent = "Checkout";

    checkoutContainer.appendChild(checkoutLink);
  }

  function unmountCheckoutButton() {
    const checkoutBtn = document.getElementById("checkout-link");
    if (checkoutBtn) {
      checkoutBtn.remove();
    }
  }
});
