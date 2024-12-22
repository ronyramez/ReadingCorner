"""
URL configuration for ReadingCorner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from .views import SignUpView
from testapp import views
# from . import views
from profileUser.views import profileUser  # Correct import for UserProfile view
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('', include('welcome.urls')),
    path('admin/', admin.site.urls),
    # path('users/', views.user_list, name='users'),
    path('signup/', include('signup.urls')),    # path('books', views.user_list, name='books'),
    path('login/', include('login.urls')),    # path('books', views.user_list, name='books'),
    path('profile/', include('profileUser.urls')),
    path('logout/', include('logout.urls')),
    path('home/', include('home.urls')),
    path('search/', include('search.urls')),
    path('books/', include('Books.urls')), #Books for searching
    path('resetpassword/', include('resetpassword.urls')), #Books for searching
    path('forgetpassword/', include('forgetpassword.urls')), #Books for searching
    path('trendingbooks/', include('trendingbooks.urls')), #Books for searching
    path('recommendbooks/', include('recommend.urls')), #Books for searching
    path('favorites/', include('favorites.urls')), #Books for searching
    path('cart/', include('cart.urls')), #Books for searching
    path('review/', include('review.urls')), #Books for searching


    #Backend API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    path('accounts/', include('allauth.urls')),  # Allauth URLs // ignore for now
    # path('auth/', include('authentication.urls')),
    # path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),

]


