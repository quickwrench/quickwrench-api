from django.urls import URLPattern, URLResolver, path

from ..workshops import views


app_name: str = "workshops"
urlpatterns: list[URLPattern | URLResolver] = [
    path("register/", views.WorkshopAPIView.as_view(), name="register"),
    path("categories/", views.CategoryAPIView.as_view(), name="category-list"),
    path("<int:id>/", views.WorkshopDetailsAPIView.as_view(), name="workshop-details"),
    path("search/", views.WorkshopListView.as_view(), name="search"),
]
