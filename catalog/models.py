from decimal import Decimal

from django.db import models


class Item(models.Model):
    class Currency(models.TextChoices):
        RUB = "rub", "Russian Ruble"
        USD = "usd", "US Dollar"

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=20, choices=Currency.choices, default=Currency.RUB
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESSFUL = "successful", "Successful"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def get_total_price(self):
        total = self.items.aggregate(
            total=models.Sum(
                models.F("quantity") * models.F("item__price"),
                output_field=models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                ),
            )
        )["total"] or Decimal("0.00")

        if hasattr(self, "discount") and self.discount:
            total = self.discount.apply_discount(total)

        if hasattr(self, "tax") and self.tax:
            total = self.tax.apply_tax(total)

        return total


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="order_items")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "item"],
                name="unique_item_per_order",
            ),
        ]

    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="discount"
    )

    def apply_discount(self, total):
        return total - total * (self.percentage / Decimal("100.00"))


class Tax(models.Model):
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="tax")

    def apply_tax(self, total):
        return total + total * (self.percentage / Decimal("100.00"))
