from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.db.models import F, Q

# Import models for dashboard metrics
from products.models import Product, MovementHistory
from receipts.models import Receipt
from delivery_app.models import Delivery
from internal_transfer.models import InternalTransfer
from django.http import HttpResponse
import csv
from django.utils import timezone


def login(request):
    # Allow login by username OR email
    if request.method == 'POST':
        identifier = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')

        username = identifier
        # if identifier looks like an email, try to resolve to username
        if identifier and '@' in identifier:
            try:
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    username = user_obj.username
            except Exception:
                username = identifier

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Account is disabled.')
                return redirect('login')
            auth_login(request, user)
            return redirect(next_url or 'dashboard')

        messages.error(request, 'Invalid credentials')
        return redirect('login')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username') or ''
        email = request.POST.get('email') or ''
        password1 = request.POST.get('password') or ''
        password2 = request.POST.get('password2') or ''

        # Basic validation
        if not email:
            messages.error(request, 'Email is required')
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # If username not provided, derive from email local-part
        if not username:
            username = email.split('@')[0]

        # Ensure username uniqueness
        base_username = username
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        # Ensure unique email
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists')
            return redirect('signup')

        # Validate password strength with Django validators
        try:
            password_validation.validate_password(password1, user=None)
        except ValidationError as e:
            messages.error(request, ' '.join(e.messages))
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        auth_login(request, user)
        return redirect('dashboard')

    return render(request, 'signin.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Dynamic dashboard metrics
    total_products = Product.objects.count()

    # Low stock: stock less than or equal to reorder level
    low_stock = Product.objects.filter(stock__lte=F('reorder_level')).count()

    # Out of stock: stock equal to zero
    out_of_stock = Product.objects.filter(stock__lte=0).count()

    # Pending receipts: status == 'Pending'
    pending_receipts = Receipt.objects.filter(status__iexact='Pending').count()

    # Pending deliveries: consider Waiting or Dispatched as pending
    pending_deliveries = Delivery.objects.filter(status__in=['Waiting', 'Dispatched']).count()

    # Internal transfers count
    internal_transfers = InternalTransfer.objects.count()

    context = {
        "total_products": total_products,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "pending_receipts": pending_receipts,
        "pending_deliveries": pending_deliveries,
        "internal_transfers": internal_transfers,
    }

    return render(request, "dashboard.html", context)


@login_required
def export_report(request):
    """Generate a CSV report containing current inventory and recent activity."""
    now = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f"stockmaster_report_{now}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Products section
    writer.writerow(["Products Inventory"]) 
    writer.writerow(["id", "name", "sku", "category", "unit", "stock", "reorder_level"])
    for p in Product.objects.all().order_by('id'):
        writer.writerow([p.id, p.name, p.sku, p.category, p.unit, p.stock, p.reorder_level])

    writer.writerow([])

    # Receipts (recent)
    writer.writerow(["Recent Receipts (last 50)"])
    writer.writerow(["id", "vendor", "product", "quantity", "status", "date"])
    for r in Receipt.objects.select_related('product').order_by('-date')[:50]:
        writer.writerow([r.id, r.vendor, r.product.name, r.quantity, r.status, r.date.isoformat()])

    writer.writerow([])

    # Deliveries (recent)
    writer.writerow(["Recent Deliveries (last 50)"])
    writer.writerow(["id", "customer", "product", "quantity", "status", "created_at"])
    for d in Delivery.objects.select_related('product').order_by('-created_at')[:50]:
        writer.writerow([d.id, d.customer_name, d.product.name, d.quantity, d.status, d.created_at.isoformat()])

    writer.writerow([])

    # Internal transfers (recent)
    writer.writerow(["Recent Internal Transfers (last 50)"])
    writer.writerow(["id", "product", "from_location", "to_location", "quantity", "date"])
    for t in InternalTransfer.objects.select_related('product').order_by('-date')[:50]:
        writer.writerow([t.id, t.product.name, t.from_location, t.to_location, t.quantity, t.date.isoformat()])

    writer.writerow([])

    # Movement history (recent)
    writer.writerow(["Recent Movement History (last 50)"])
    writer.writerow(["id", "product", "movement_type", "quantity", "note", "date"])
    for m in MovementHistory.objects.select_related('product').order_by('-date')[:50]:
        writer.writerow([m.id, m.product.name, m.movement_type, m.quantity, (m.note or ''), m.date.isoformat()])

    return response


@login_required
def profile_view(request):
    return render(request, "profile.html")
