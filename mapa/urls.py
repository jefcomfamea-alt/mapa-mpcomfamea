from django.urls import path
from .views import nuevo_caso, casos_json

urlpatterns = [
    path("nuevo-caso/", nuevo_caso, name="nuevo_caso"),
    path("casos-json/", casos_json, name="casos_json"),
]