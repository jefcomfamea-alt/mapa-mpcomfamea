from django.contrib import admin
from django.urls import path, include
from mapa.views import inicio

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login y logout de Django
    path("accounts/", include("django.contrib.auth.urls")),

    # Página principal (mapa)
    path("", inicio, name="inicio"),
]