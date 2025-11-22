from django.contrib import admin
from .models import Receipt

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "product", "quantity", "status", "date")
    search_fields = ("vendor", "product__name")
