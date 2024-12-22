from django.urls import path
from .views import forget_password_view

urlpatterns = [
    path('', forget_password_view),
]
