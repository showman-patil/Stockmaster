from django.db import models
from django.utils import timezone


# ======================
# PRODUCT MODEL
# ======================
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    stock = models.IntegerField()

    description = models.TextField(blank=True, null=True)
    reorder_level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# ======================
# STOCK ADJUSTMENT MODEL
# ======================
class StockAdjustment(models.Model):

    ADJUST_TYPES = [
        ("Increase", "Increase"),
        ("Decrease", "Decrease"),
        ("Damage", "Damage"),
        ("Lost", "Lost"),
        ("Mismatch", "Mismatch"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=30, choices=ADJUST_TYPES)
    quantity = models.PositiveIntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()

    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} - {self.adjustment_type}"


# ======================
# MOVEMENT HISTORY MODEL
# ======================
class MovementHistory(models.Model):
    MOVEMENT_TYPES = [
        ("Receipt", "Receipt"),
        ("Delivery", "Delivery"),
        ("Adjustment", "Adjustment"),
        ("Transfer", "Transfer"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)

    quantity = models.IntegerField()
    source = models.CharField(max_length=100, blank=True, null=True)  
    destination = models.CharField(max_length=100, blank=True, null=True)

    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
