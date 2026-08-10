import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def catalog(request: HttpRequest) -> HttpResponse:
    items = {
        "items": [
            {"id": 1, "name": "Item 1", "description": "Item 1 is awldlwadw"},
            {"id": 2, "name": "Item 2", "description": "Item 2 is awldlwadw"},
            {"id": 3, "name": "Item 3", "description": "Item 3 is awldlwadw"},
            {"id": 4, "name": "Item 4", "description": "Item 4 is awldlwadw"},
        ]
    }
    return render(request, "catalog/catalog.html", items)


def item(request: HttpRequest, item_id) -> HttpResponse:
    return render(
        request,
        "catalog/item.html",
        {"id": item_id, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY},
    )


def buy(request: HttpRequest, item_id: int) -> JsonResponse:
    item = get_object_or_404(Item, id=item_id)

    session = client.v1.checkout.sessions.create(
        params={
            "line_items": [
                {
                    "price_data": {
                        "currency": "rub",
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                        },
                        "unit_amount": 1,
                    },
                    "quantity": 1,
                }
            ],
            "mode": "payment",
        },
    )
    return JsonResponse({id: session.id})
