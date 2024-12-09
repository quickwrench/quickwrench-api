from django.urls import URLPattern, URLResolver, path

from quickwrench_api.apps.workshops import views


app_name: str = "workshops"
urlpatterns: list[URLPattern | URLResolver] = [
    path("register/", views.WorkshopAPIView.as_view(), name="register")
]
