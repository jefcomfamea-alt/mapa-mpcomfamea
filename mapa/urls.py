from django.urls import path

from .views import nuevo_caso, casos_json, cerrar_sesion


urlpatterns = [

    path("nuevo-caso/", nuevo_caso, name="nuevo_caso"),

    path("casos-json/", casos_json, name="casos_json"),

    path("cerrar-sesion/", cerrar_sesion, name="cerrar_sesion"),

]