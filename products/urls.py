from django.urls import path
from . import views

app_name = "products"   # ← IMPORTANT

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_add, name='product_add'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('adjustments/', views.adjustment_list, name='adjustment_list'),
    path('adjustments/add/', views.adjustment_add, name='adjustment_add'),
    path('history/', views.movement_history, name='movement_history'),
]
