from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.backends import LoginAPIView
from core.views.get_users import UsersView
from core.views.authentication import RegisterAPI

urlpatterns = [
    path('login',LoginAPIView.as_view(), name='login'),
    path('refresh_token',TokenRefreshView.as_view(), name='refresh_token'),
    path('all_users',UsersView.as_view(),name = 'all_users'),
    path("register", RegisterAPI.as_view(), name="register_user"),
]