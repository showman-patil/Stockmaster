from django.urls import path
from . import views
app_name = "receipts"  
urlpatterns = [
    path('', views.receipt_list, name='receipt_list'),
    path('add/', views.receipt_add, name='receipt_add'),
    path('<int:id>/', views.receipt_detail, name='receipt_detail'),   # NEW
]
