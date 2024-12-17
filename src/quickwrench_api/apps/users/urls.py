from django.urls import URLPattern, URLResolver, path

from . import views

app_name: str = "users"

urlpatterns: list[URLPattern | URLResolver] = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("<int:id>/", views.UserDetailsAPIView.as_view(), name="user-details"),
]
