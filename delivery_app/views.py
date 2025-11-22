from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Delivery
from products.models import Product, MovementHistory


# -----------------------------
# 1️⃣ Delivery List
# -----------------------------
def delivery_list(request):
    deliveries = Delivery.objects.all().order_by("-created_at")
    return render(request, "delivery/delivery_list.html", {"deliveries": deliveries})


# -----------------------------
# 2️⃣ Create Delivery Order
# -----------------------------
def delivery_create(request):
    products = Product.objects.all()

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        product_id = request.POST.get("product_id")
        note = request.POST.get("note", "")

        try:
            quantity = int(request.POST.get("quantity"))
        except:
            messages.error(request, "Invalid quantity!")
            return redirect("delivery_create")

        product = get_object_or_404(Product, id=product_id)

        if quantity <= 0:
            messages.error(request, "Quantity must be more than 0.")
            return redirect("delivery_create")

        if quantity > product.stock:
            messages.error(request, "Not enough stock!")
            return redirect("delivery_create")

        previous_stock = product.stock
        new_stock = previous_stock - quantity

        # CREATE DELIVERY
        delivery = Delivery.objects.create(
            customer_name=customer_name,
            product=product,
            quantity=quantity,
            note=note,
            status="Dispatched",
        )

        # UPDATE STOCK
        product.stock = new_stock
        product.save()

        # MOVEMENT HISTORY ENTRY
        MovementHistory.objects.create(
            product=product,
            movement_type="Delivery",
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            source="Warehouse",
            destination=customer_name,
            note=f"Delivery to {customer_name}. {note or ''}",
            date=timezone.now()
        )

        messages.success(request, "Delivery order created successfully!")
        return redirect("delivery_list")

    return render(request, "delivery/delivery_create.html", {"products": products})


# -----------------------------
# 3️⃣ Delivery Detail Page
# -----------------------------
def delivery_detail(request, id):
    delivery = get_object_or_404(Delivery, id=id)
    return render(request, "delivery/delivery_detail.html", {"delivery": delivery})
