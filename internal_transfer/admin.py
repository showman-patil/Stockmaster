from django.contrib import admin
from .models import InternalTransfer

@admin.register(InternalTransfer)
class InternalTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "from_location", "to_location", "quantity", "date")
    search_fields = ("product__name",)
