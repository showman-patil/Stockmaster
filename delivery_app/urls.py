from django.urls import path
from . import views

# namespacing for use in templates: {% url 'delivery:delivery_list' %}
app_name = 'delivery'

urlpatterns = [
    path("", views.delivery_list, name="delivery_list"),
    path("create/", views.delivery_create, name="delivery_create"),
    path("<int:id>/", views.delivery_detail, name="delivery_detail"),
]
