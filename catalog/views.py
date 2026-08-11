from decimal import Decimal

import stripe
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from catalog.models import Item, Order, OrderItem
from catalog.services import get_item, get_or_create_order, get_order

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def catalog(request: HttpRequest) -> HttpResponse:
    items = Item.objects.all()
    order = get_order(request)
    return render(
        request,
        "catalog/catalog.html",
        {
            "items": items,
            "order": order,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )


def item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    item_obj = get_item(item_id)
    return render(
        request,
        "catalog/item.html",
        {"item": item_obj},
    )


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    session_order_id = request.session.get("order_id")

    if order_id != session_order_id:
        raise Http404("Order not found")

    order = get_object_or_404(
        Order,
        id=order_id,
        status=Order.Status.PENDING,
    )
    order_items = order.items.select_related("item").all()

    if order_items.exists():
        currency = order_items.first().item.currency.lower()
    else:
        currency = ""

    total_price = order.get_total_price()

    return render(
        request,
        "catalog/order_details.html",
        {
            "order": order,
            "items": order_items,
            "total_price": total_price,
            "currency": currency,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )


def order_success(request: HttpRequest, order_id: int) -> HttpResponse:
    session_order_id = request.session.get("order_id")

    if session_order_id != order_id:
        raise Http404("Order not found")

    order = get_object_or_404(Order, id=order_id)

    payment_intent_id = request.GET.get("payment_intent")

    if payment_intent_id and payment_intent_id == order.stripe_payment_intent_id:
        intent = client.v1.payment_intents.retrieve(payment_intent_id)

        if intent.status == "succeeded":
            order.status = Order.Status.SUCCESSFUL
            order.save(update_fields=["status"])

    return render(request, "catalog/success.html", {"order": order})


def buy(request: HttpRequest, order_id: int) -> JsonResponse:
    session_order_id = request.session.get("order_id")

    if session_order_id != order_id:
        raise Http404("Order not found")

    order = get_object_or_404(
        Order,
        id=order_id,
        status=Order.Status.PENDING,
    )

    if not order.items.exists():
        return JsonResponse(
            {"error": "Order is empty"},
            status=400,
        )

    total_amount = order.get_total_price()

    currency = order.items.first().item.currency.lower()

    intent = client.v1.payment_intents.create(
        {
            "amount": int(total_amount * Decimal("100.00")),
            "currency": currency,
            "automatic_payment_methods": {"enabled": True},
            "metadata": {"order_id": order.id},
        }
    )

    order.stripe_payment_intent_id = intent.id
    order.save(update_fields=["stripe_payment_intent_id"])

    return JsonResponse(
        {
            "clientSecret": intent.client_secret,
            "publishableKey": settings.STRIPE_PUBLISHABLE_KEY,
        }
    )


@require_POST
def add_item_to_order(request: HttpRequest, item_id: int) -> JsonResponse:

    item = get_item(item_id)
    order = get_or_create_order(request)

    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, defaults={"quantity": 1}
    )
    if not created:
        order_item.quantity += 1
        order_item.save(update_fields=["quantity"])

    return JsonResponse(
        {
            "id": order.id,
            "status": "success",
            "total_items": order.items.count(),
            "item": {
                "id": item.id,
                "quantity": order_item.quantity,
            },
        }
    )


@require_POST
def remove_item_from_order(request: HttpRequest, item_id: int) -> JsonResponse:
    order = get_order(request)

    if order is None:
        raise Http404("Order does not exist")

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


@require_POST
def remove_order(request: HttpRequest) -> JsonResponse:
    order_id = request.session.get("order_id")

    if not order_id:
        raise Http404("Order not found")

    order = get_object_or_404(Order, id=order_id)

    order.delete()
    request.session.pop("order_id", None)

    return JsonResponse(
        {
            "status": "success",
        }
    )
