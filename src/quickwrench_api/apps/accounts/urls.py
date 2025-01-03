from django.urls import URLPattern, URLResolver, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AccountDetailsAPIView

app_name: str = "accounts"

urlpatterns: list[URLPattern | URLResolver] = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("me/", AccountDetailsAPIView.as_view(), name="account-details"),
]
