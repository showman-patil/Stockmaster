from django.db import models
from products.models import Product
from django.utils import timezone

class InternalTransfer(models.Model):

    LOCATIONS = [
        ("Warehouse", "Warehouse"),
        ("Rack A", "Rack A"),
        ("Rack B", "Rack B"),
        ("Rack C", "Rack C"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100, choices=LOCATIONS)
    to_location = models.CharField(max_length=100, choices=LOCATIONS)
    quantity = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} ({self.from_location} → {self.to_location})"
