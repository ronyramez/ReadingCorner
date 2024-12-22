from django.urls import path
from .views import add_to_cart, remove_from_cart, list_cart

urlpatterns = [
    path('add/', add_to_cart),
    path('remove/', remove_from_cart),
    path('', list_cart),
]