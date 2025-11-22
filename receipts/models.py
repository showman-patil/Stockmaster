from django.db import models
from products.models import Product

class Receipt(models.Model):
    vendor = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Received", "Received"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Received")

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receipt #{self.id}"
