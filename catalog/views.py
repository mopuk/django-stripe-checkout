from django.shortcuts import render


def catalog(request):
    items = {
        "items": [
            {"id": 1, "name": "Item 1", "description": "Item 1 is awldlwadw"},
            {"id": 2, "name": "Item 2", "description": "Item 2 is awldlwadw"},
            {"id": 3, "name": "Item 3", "description": "Item 3 is awldlwadw"},
            {"id": 4, "name": "Item 4", "description": "Item 4 is awldlwadw"},
        ]
    }
    return render(request, "catalog/items.html", items)


def item(request, item_id):
    return render(request, "catalog/item.html", {"id": item_id})
