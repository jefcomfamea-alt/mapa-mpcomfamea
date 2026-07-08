from django.contrib import admin
from django.urls import path, include
from mapa.views import inicio

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login y logout
    path("accounts/", include("django.contrib.auth.urls")),

    # Página principal
    path("", inicio, name="inicio"),

    # Rutas de la aplicación mapa
    path("", include("mapa.urls")),
]