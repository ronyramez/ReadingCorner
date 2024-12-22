from django.urls import path
from .views import top_rated_books

urlpatterns = [
    path('', top_rated_books),
]
