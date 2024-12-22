from django.urls import path
from .views import recommend_books

urlpatterns = [
    path('', recommend_books),
]
