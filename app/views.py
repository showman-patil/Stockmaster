from django.shortcuts import render

# Create your views here.
def login(request):  
    return render(request, 'login.html')

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
