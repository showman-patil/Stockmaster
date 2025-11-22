from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
        return redirect('login')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect('dashboard')

    return render(request, 'signin.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')

def dashboard(request):
    context = {
        "total_products": 128,
        "low_stock": 12,
        "out_of_stock": 4,
        "pending_receipts": 5,
        "pending_deliveries": 3,
        "internal_transfers": 2,
    }
    return render(request, "dashboard.html", context)


def profile_view(request):
   
    return render(request, "profile.html")  
