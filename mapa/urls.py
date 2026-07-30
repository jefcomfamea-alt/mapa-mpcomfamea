from django.urls import path
from . import views

urlpatterns = [

    # Página principal
    path("", views.inicio, name="inicio"),

    # Casos
    path("nuevo-caso/", views.nuevo_caso, name="nuevo_caso"),
    path("gestion-casos/", views.gestion_casos, name="gestion_casos"),
    path("casos-json/", views.casos_json, name="casos_json"),

    # Editar y archivar casos
    path("editar-caso/<int:id>/", views.editar_caso, name="editar_caso"),
    path("archivar-caso/<int:id>/", views.archivar_caso, name="archivar_caso"),
    path("casos-archivados/", views.casos_archivados, name="casos_archivados"),
    path("restaurar-caso/<int:id>/", views.restaurar_caso, name="restaurar_caso"),

    # Solicitudes
    path(
        "solicitar-modificacion/<int:id>/",
        views.solicitar_modificacion,
        name="solicitar_modificacion",
    ),
    path(
        "aprobar-solicitud/<int:id>/",
        views.aprobar_solicitud,
        name="aprobar_solicitud",
    ),
    path(
        "rechazar-solicitud/<int:id>/",
        views.rechazar_solicitud,
        name="rechazar_solicitud",
    ),

    # Buzón de mensajes
    path("mensajes/", views.mensajes, name="mensajes"),

    # Notificaciones de casos por vencer
    path(
        "notificaciones/",
        views.notificaciones,
        name="notificaciones",
    ),

    # Buscar casos
    path("buscar-caso/", views.buscar_caso, name="buscar_caso"),

    # Cerrar sesión
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),

    # Ubigeo
    path(
        "cargar-provincias/",
        views.cargar_provincias,
        name="cargar_provincias",
    ),

    path(
        "cargar-distritos/",
        views.cargar_distritos,
        name="cargar_distritos",
    ),

    # Administración de usuarios
path(
    "administrar-usuarios/",
    views.administrar_usuarios,
    name="administrar_usuarios",
),

path(
    "administrar-usuarios/nuevo/",
    views.nuevo_usuario,
    name="nuevo_usuario",
),

path(
    "administrar-usuarios/editar/<int:pk>/",
    views.editar_usuario,
    name="editar_usuario",
),

path(
    "administrar-usuarios/desactivar/<int:pk>/",
    views.desactivar_usuario,
    name="desactivar_usuario",
),
]