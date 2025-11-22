from django.contrib import admin
from .models import Product, StockAdjustment, MovementHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "category", "stock", "reorder_level")
    search_fields = ("name", "sku", "category")

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "adjustment_type", "quantity", "previous_stock", "new_stock", "date")
    search_fields = ("product__name", "adjustment_type")

@admin.register(MovementHistory)
class MovementHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "movement_type", "quantity", "source", "destination", "date")

