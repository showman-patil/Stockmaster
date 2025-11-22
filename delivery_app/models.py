from django.db import models
from products.models import Product

class Delivery(models.Model):

    STATUS_CHOICES = [
        ("Waiting", "Waiting"),
        ("Dispatched", "Dispatched"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Waiting")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery {self.id} - {self.customer_name}"
