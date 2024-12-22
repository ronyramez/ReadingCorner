from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),  # Default route for welcome page
    # path('signup/', views.signup, name='signup'),  # Signup route (ensure this view is defined)
    # path('login/', views.login, name='login'),  # Login route (ensure this view is defined)
]
