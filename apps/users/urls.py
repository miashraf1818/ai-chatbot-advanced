"""
Users URL Configuration
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.api.views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView
)
from apps.users.api.google_auth import GoogleLoginView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
]

