from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import Item, Order


def get_order(request: HttpRequest) -> Order | None:
    order_id = request.session.get("order_id")
    if not order_id:
        return None
    return Order.objects.filter(
        id=order_id,
        status=Order.Status.PENDING,
    ).first()


def get_or_create_order(request: HttpRequest) -> Order:
    order = get_order(request)

    if order is not None:
        return order

    order = Order.objects.create(status=Order.Status.PENDING)

    request.session["order_id"] = order.id

    return order


def get_item(item_id: int) -> Item | None:
    return get_object_or_404(Item, id=item_id)
