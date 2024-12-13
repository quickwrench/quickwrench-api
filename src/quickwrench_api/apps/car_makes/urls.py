from django.urls import URLPattern, URLResolver, path
from .views import CarMakeAPI

app_name: str = "car_makes"

urlpatterns: list[URLPattern | URLResolver] = [
    path("index/", CarMakeAPI.as_view(), name="index")
]
