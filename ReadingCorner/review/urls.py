from django.urls import path
from .views import add_review, list_reviews_for_book, list_reviews_for_user, delete_review

urlpatterns = [
    path('add/', add_review),
    path('<int:id>', list_reviews_for_book),
    path('delete/', delete_review),
    path('', list_reviews_for_user),

]