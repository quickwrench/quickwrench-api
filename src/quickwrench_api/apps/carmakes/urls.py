from django.urls import URLPattern, URLResolver, path

from .views import CarMakeAPIView

app_name: str = "carmakes"

urlpatterns: list[URLPattern | URLResolver] = [
    path("", CarMakeAPIView.as_view(), name="index")
]
