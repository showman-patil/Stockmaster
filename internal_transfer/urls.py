from django.urls import path
from . import views
app_name = "internal_transfer"  
urlpatterns = [
    path("", views.transfer_list, name="transfer_list"),
    path("add/", views.transfer_add, name="transfer_add"),
]
