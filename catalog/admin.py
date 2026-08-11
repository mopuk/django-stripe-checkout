from django.contrib import admin

from .models import Discount, Item, Order, OrderItem, Tax

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
admin.site.register(Tax)
