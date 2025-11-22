from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .models import InternalTransfer
from products.models import Product, MovementHistory


def transfer_list(request):
    transfers = InternalTransfer.objects.all().order_by("-id")
    return render(request, "internal_transfer/transfer_list.html", {"transfers": transfers})


def transfer_add(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        from_loc = request.POST.get("from_location")
        to_loc = request.POST.get("to_location")
        qty = int(request.POST.get("quantity"))
        note = request.POST.get("note", "")

        product = Product.objects.get(id=product_id)

        # ❌ SAME LOCATION CHECK
        if from_loc == to_loc:
            messages.error(request, "Cannot transfer to the same location.")
            return redirect("transfer_add")

        # ❌ STOCK CHECK
        if qty > product.stock:
            messages.error(request, "Not enough stock available!")
            return redirect("transfer_add")

        previous_stock = product.stock

        # 📌 STOCK UPDATE (Warehouse logic)
        product.stock -= qty
        product.save()

        new_stock = product.stock

        # 📌 SAVE TRANSFER ENTRY
        InternalTransfer.objects.create(
            product_id=product_id,
            from_location=from_loc,
            to_location=to_loc,
            quantity=qty,
            note=note,
            date=timezone.now()
        )

        # =============================
        # 📌 MOVEMENT HISTORY ENTRIES
        # =============================

        # 1️⃣ Transfer-Out
        MovementHistory.objects.create(
            product=product,
            movement_type="Transfer",
            quantity=qty,
            source=from_loc,
            destination=to_loc,
            note=f"Transfer OUT. prev={previous_stock} new={new_stock}. {note or ''}",
            date=timezone.now()
        )

        # 2️⃣ Transfer-In (Logical entry)
        MovementHistory.objects.create(
            product=product,
            movement_type="Transfer",
            quantity=qty,
            source=from_loc,
            destination=to_loc,
            note=f"Transfer IN. prev={new_stock} new={new_stock}. {note or ''}",
            date=timezone.now()
        )

        messages.success(request, "Internal transfer completed successfully!")
        return redirect("transfer_list")

    return render(request, "internal_transfer/transfer_add.html", {"products": products})
