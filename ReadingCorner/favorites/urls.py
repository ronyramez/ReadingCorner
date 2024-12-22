from django.urls import path
from .views import add_to_favorites, remove_from_favorites, list_favorites

urlpatterns = [
    path('add/', add_to_favorites),
    path('remove/', remove_from_favorites),
    path('', list_favorites),
]