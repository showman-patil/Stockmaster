from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "product", "quantity", "status", "created_at")
    search_fields = ("customer_name", "product__name")
