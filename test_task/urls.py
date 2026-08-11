"""
URL configuration for test_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from catalog import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="catalog", permanent=False)),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("buy/<int:order_id>/", views.buy, name="buy"),
    path("order/success/<int:order_id>", views.order_success, name="success"),
    path("order/add/<int:item_id>", views.add_item_to_order, name="add_item_to_order"),
    path(
        "order/remove/<int:item_id>",
        views.remove_item_from_order,
        name="remove_item_to_order",
    ),
    path("order/details/<int:order_id>", views.order_detail, name="order_details"),
    path("order/remove", views.remove_order, name="remove_order"),
]
