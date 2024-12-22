from django.urls import path
from .views import get_all_books, get_book

urlpatterns = [
    path('', get_all_books),
    path('<int:id>', get_book),
]
