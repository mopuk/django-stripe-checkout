import stripe
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from catalog.models import Item, Order, OrderItem

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def catalog(request: HttpRequest) -> HttpResponse:
    items = Item.objects.all()
    return render(request, "catalog/catalog.html", {"items": items})


def item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    item_obj = get_object_or_404(Item, id=item_id)
    return render(
        request,
        "catalog/item.html",
        {"item": item_obj},
    )


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order_obj = get_object_or_404(Order, id=order_id)
    order_items = order_obj.items.select_related("item").all()

    if order_items.exists():
        currency = order_items.first().item.currency.lower()
    else:
        currency = ""

    total_price = order_obj.get_total_price()

    return render(
        request,
        "catalog/order_details.html",
        {
            "order": order_obj,
            "items": order_items,
            "total_price": total_price,
            "currency": currency,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )


def order_success(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, "catalog/success.html", {"order": order})


def buy(request: HttpRequest, order_id: int) -> JsonResponse:
    order = get_object_or_404(Order, id=order_id)

    total_amount = order.get_total_price()
    if order.items.exists():
        currency = order.items.first().item.currency.lower()
    else:
        return JsonResponse({"error": "Order is empty"}, status=400)

    intent = client.v1.payment_intents.create(
        {
            "amount": int(total_amount * 100),
            "currency": currency,
            "automatic_payment_methods": {"enabled": True},
            "metadata": {"order_id": order.id},
        }
    )
    return JsonResponse(
        {
            "clientSecret": intent.client_secret,
            "publishableKey": settings.STRIPE_PUBLISHABLE_KEY,
        }
    )


@require_POST
def add_item_to_order(request: HttpRequest, item_id: int) -> JsonResponse:
    order_id = request.session.get("order_id")
    item_obj = get_object_or_404(Item, id=item_id)

    if order_id:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = Order.objects.create(status=Order.Status.PENDING)
        request.session["order_id"] = order.id

    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item_obj, defaults={"quantity": 1}
    )
    if not created:
        order_item.quantity += 1
        order_item.save(update_fields=["quantity"])

    return JsonResponse(
        {
            "id": order.id,
            "status": "success",
            "total_items": order.items.count(),
        }
    )


@require_POST
def remove_item_from_order(
    request: HttpRequest, item_id: int
) -> JsonResponse | HttpResponse:
    order_id = request.session.get("order_id")
    if not order_id:
        raise Http404("Order does not exist")

    order = get_object_or_404(Order, id=order_id, status=Order.Status.PENDING)
    order_item = order.items.filter(item=item_id).first()
    if not order_item:
        return JsonResponse({"error": "Item not found in order"}, status=404)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save(update_fields=["quantity"])

    else:
        order_item.delete()

    return JsonResponse(
        {
            "status": "success",
            "order_id": order.id,
            "total_items": order.items.count(),
        }
    )
