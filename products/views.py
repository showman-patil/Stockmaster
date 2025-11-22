from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Product, StockAdjustment, MovementHistory


# ======================
# PRODUCT LIST
# ======================
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


# ======================
# ADD PRODUCT
# ======================
def product_add(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST['name'],
            sku=request.POST['sku'],
            category=request.POST['category'],
            unit=request.POST['unit'],
            stock=request.POST['stock'],
            description=request.POST.get('description'),
            reorder_level=request.POST.get('reorder_level', 0)
        )
        return redirect('products:product_list')

    return render(request, 'products/product_add.html')


# ======================
# PRODUCT DETAIL + EDIT
# ======================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.sku = request.POST['sku']
        product.category = request.POST['category']
        product.unit = request.POST['unit']
        product.stock = request.POST['stock']
        product.description = request.POST.get('description')
        product.reorder_level = request.POST.get('reorder_level', 0)
        product.save()

        return redirect('products:product_list')

    return render(request, 'products/product_detail.html', {'product': product})


# ========================================================
#            STOCK ADJUSTMENT — ADD
# ========================================================
def adjustment_add(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        adj_type = request.POST.get("adjustment_type")
        qty = int(request.POST.get("quantity"))
        note = request.POST.get("note", "")

        product = get_object_or_404(Product, id=product_id)
        prev = product.stock

        # ---------- LOGIC ----------
        if adj_type in ["Decrease", "Damage", "Lost", "Mismatch"]:
            if qty > prev:
                messages.error(request, "Quantity cannot be more than available stock!")
                return redirect("products:adjustment_add")
            new_stock = prev - qty
        else:
            new_stock = prev + qty

        # ---------- SAVE ADJUSTMENT ----------
        StockAdjustment.objects.create(
            product=product,
            adjustment_type=adj_type,
            quantity=qty,
            previous_stock=prev,
            new_stock=new_stock,
            note=note,
            date=timezone.now()
        )

        # ---------- MOVEMENT HISTORY ----------
        MovementHistory.objects.create(
            product=product,
            movement_type="Adjustment",
            quantity=qty,
            previous_stock=prev,
            new_stock=new_stock,
            from_location=None,
            to_location=None,
            note=f"Stock adjustment: {adj_type}. {note}",
        )

        # ---------- UPDATE PRODUCT STOCK ----------
        product.stock = new_stock
        product.save()

        messages.success(request, "Stock adjustment applied successfully!")
        return redirect("products:adjustment_list")

    return render(request, "products/adjustment_add.html", {"products": products})


# ========================================================
#            STOCK ADJUSTMENT — LIST
# ========================================================
def adjustment_list(request):
    adjustments = StockAdjustment.objects.all().order_by('-date')
    return render(request, "products/adjustment_list.html", {"adjustments": adjustments})


# ========================================================
#            MOVEMENT HISTORY PAGE
# ========================================================
def movement_history(request):
    history = MovementHistory.objects.all().order_by('-date')
    return render(request, "products/move_history.html", {"history": history})
