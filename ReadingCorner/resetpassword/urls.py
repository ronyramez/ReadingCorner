from django.urls import path
from .views import reset_password_view

urlpatterns = [
    path('', reset_password_view),
]
