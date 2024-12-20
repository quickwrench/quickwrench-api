from django.conf import settings
from django.conf.urls.static import static
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns: list[URLPattern | URLResolver] = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(), name="docs"),
    path("accounts/", include("quickwrench_api.apps.accounts.urls")),
    path("users/", include("quickwrench_api.apps.users.urls")),
    path("workshops/", include("quickwrench_api.apps.workshops.urls")),
    path("carmakes/", include("quickwrench_api.apps.car_makes.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
