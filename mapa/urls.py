from django.urls import path

from .views import (
    inicio,
    nuevo_caso,
    casos_json,
    cerrar_sesion,
    gestion_casos,
    editar_caso,
    archivar_caso,
    casos_archivados,
    restaurar_caso,
    solicitar_modificacion,
    mensajes,
)

urlpatterns = [

    path("", inicio, name="inicio"),

    path("nuevo-caso/", nuevo_caso, name="nuevo_caso"),

    path("casos-json/", casos_json, name="casos_json"),

    path("cerrar-sesion/", cerrar_sesion, name="cerrar_sesion"),

    path("gestion-casos/", gestion_casos, name="gestion_casos"),

    path("editar-caso/<int:id>/", editar_caso, name="editar_caso"),

    path("archivar-caso/<int:id>/", archivar_caso, name="archivar_caso"),

    path("casos-archivados/", casos_archivados, name="casos_archivados"),

    path("restaurar-caso/<int:id>/", restaurar_caso, name="restaurar_caso"),

    path(
        "solicitar-modificacion/<int:id>/",
        solicitar_modificacion,
        name="solicitar_modificacion"
    ),

    path(
        "mensajes/",
        mensajes,
        name="mensajes"
    ),
]