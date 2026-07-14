from django.contrib import admin
from django.urls import path, include
from mapa.views import inicio

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),

    path("", inicio, name="inicio"),

    path("", include("mapa.urls")),
]