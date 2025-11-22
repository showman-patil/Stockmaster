from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from products.models import Product, MovementHistory
from django.utils import timezone


# ---------------------------------------
# 1) RECEIPT LIST
# ---------------------------------------
def receipt_list(request):
    receipts = Receipt.objects.all().order_by('-id')
    return render(request, "receipts/receipt_list.html", {"receipts": receipts})


# ---------------------------------------
# 2) CREATE NEW RECEIPT
# ---------------------------------------
def receipt_add(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        qty = int(request.POST.get("quantity"))
        vendor = request.POST.get("vendor")
        note = request.POST.get("note")

        product = get_object_or_404(Product, id=product_id)
        previous_stock = product.stock
        new_stock = previous_stock + qty

        # Save Receipt
        receipt = Receipt.objects.create(
            vendor=vendor,
            product=product,
            quantity=qty,
            note=note,
            status="Received",
            date=timezone.now()
        )

        # Update Stock
        product.stock = new_stock
        product.save()

        # -------------- MOVEMENT HISTORY ENTRY --------------
        MovementHistory.objects.create(
            product=product,
            movement_type="Receipt",
            quantity=qty,
            previous_stock=previous_stock,
            new_stock=new_stock,
            from_location=vendor,      # vendor = source
            to_location="Warehouse",   # default destination
            note=f"Receipt added from vendor {vendor}. {note or ''}"
        )

        return redirect("receipt_list")

    return render(request, "receipts/receipt_add.html", {"products": products})


# ---------------------------------------
# 3) RECEIPT DETAIL PAGE
# ---------------------------------------
def receipt_detail(request, id):
    receipt = get_object_or_404(Receipt, id=id)
    return render(request, "receipts/receipt_detail.html", {"receipt": receipt})
