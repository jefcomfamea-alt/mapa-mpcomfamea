from django.urls import path
from . import views


urlpatterns = [

    # ===============================
    # PÁGINA PRINCIPAL
    # ===============================

    path(
        "",
        views.inicio,
        name="inicio"
    ),


    # ===============================
    # MAPA DE AGRESORES
    # ===============================

    path(
        "mapa-agresores/",
        views.mapa_agresores,
        name="mapa_agresores"
    ),


    # ===============================
    # CASOS
    # ===============================

    path(
        "nuevo-caso/",
        views.nuevo_caso,
        name="nuevo_caso"
    ),

    path(
        "gestion-casos/",
        views.gestion_casos,
        name="gestion_casos"
    ),

    path(
        "casos-preliminares/",
        views.casos_preliminares,
        name="casos_preliminares"
    ),

    path(
        "eliminar-caso-preliminar/<int:id>/",
        views.eliminar_caso_preliminar,
        name="eliminar_caso_preliminar"
    ),

    path(
        "casos-json/",
        views.casos_json,
        name="casos_json"
    ),


    # ===============================
    # EDITAR / ARCHIVAR
    # ===============================

    path(
        "editar-caso/<int:id>/",
        views.editar_caso,
        name="editar_caso"
    ),

    path(
        "casos/<int:id>/actualizar-ubicacion/",
        views.actualizar_ubicacion_caso,
        name="actualizar_ubicacion_caso"
    ),

    path(
        "archivar-caso/<int:id>/",
        views.archivar_caso,
        name="archivar_caso"
    ),

    path(
        "casos-archivados/",
        views.casos_archivados,
        name="casos_archivados"
    ),

    path(
        "restaurar-caso/<int:id>/",
        views.restaurar_caso,
        name="restaurar_caso"
    ),


    # ===============================
# CASOS ELIMINADOS
# ===============================

path(
    "eliminar-caso/<int:id>/",
    views.eliminar_caso,
    name="eliminar_caso"
),

path(
    "casos-eliminados/",
    views.casos_eliminados,
    name="casos_eliminados"
),

path(
    "casos-eliminados/restaurar/<int:id>/",
    views.restaurar_caso_eliminado,
    name="restaurar_caso_eliminado"
),

path(
    "casos-eliminados/eliminar-definitivamente/<int:id>/",
    views.eliminar_caso_definitivamente,
    name="eliminar_caso_definitivamente"
),


    # ===============================
    # SOLICITUDES DE MODIFICACIÓN
    # ===============================

    path(
        "solicitar-modificacion/<int:id>/",
        views.solicitar_modificacion,
        name="solicitar_modificacion"
    ),

    path(
        "aprobar-solicitud/<int:id>/",
        views.aprobar_solicitud,
        name="aprobar_solicitud"
    ),

    path(
        "rechazar-solicitud/<int:id>/",
        views.rechazar_solicitud,
        name="rechazar_solicitud"
    ),


    # ===============================
    # MENSAJES
    # ===============================

    path(
        "mensajes/",
        views.mensajes,
        name="mensajes"
    ),


    # ===============================
    # NOTIFICACIONES
    # ===============================

    path(
        "notificaciones/",
        views.notificaciones,
        name="notificaciones"
    ),


    # ===============================
    # BUSCAR CASOS
    # ===============================

    path(
        "buscar-caso/",
        views.buscar_caso,
        name="buscar_caso"
    ),


    # ===============================
    # CERRAR SESIÓN
    # ===============================

    path(
        "cerrar-sesion/",
        views.cerrar_sesion,
        name="cerrar_sesion"
    ),


# ===============================
# UBIGEO
# ===============================

path(
    "cargar-regiones/",
    views.cargar_regiones,
    name="cargar_regiones"
),

path(
    "cargar-provincias/",
    views.cargar_provincias,
    name="cargar_provincias"
),

path(
    "cargar-distritos/",
    views.cargar_distritos,
    name="cargar_distritos"
),

    # ===============================
    # UBICACIÓN PRELIMINAR
    # ===============================

    path(
        "ubicaciones-preliminares-json/",
        views.ubicaciones_preliminares_json,
        name="ubicaciones_preliminares_json"
    ),

    path(
        "registrar-ubicacion-preliminar/",
        views.registrar_ubicacion_preliminar,
        name="registrar_ubicacion_preliminar"
    ),

    path(
        "seleccionar-rol-preliminar/<int:id>/",
        views.seleccionar_rol_preliminar,
        name="seleccionar_rol_preliminar"
    ),


    # ===============================
    # ADMINISTRACIÓN DE USUARIOS
    # ===============================

    path(
        "administrar-usuarios/",
        views.administrar_usuarios,
        name="administrar_usuarios"
    ),

    path(
        "administrar-usuarios/nuevo/",
        views.nuevo_usuario,
        name="nuevo_usuario"
    ),

    path(
        "administrar-usuarios/editar/<int:pk>/",
        views.editar_usuario,
        name="editar_usuario"
    ),

    path(
        "administrar-usuarios/desactivar/<int:pk>/",
        views.desactivar_usuario,
        name="desactivar_usuario"
    ),

    path(
        "estadistica/",
        views.estadistica,
        name="estadistica"
    ),

    path(
        "descargar-estadistica/",
        views.descargar_estadistica,
        name="descargar_estadistica"
    ),

    path(
        "corregir-niveles-riesgo/",
        views.corregir_niveles_riesgo,
        name="corregir_niveles_riesgo"
    ),

    path(
        "casos-por-efectivo/<int:id>/",
        views.casos_por_efectivo,
        name="casos_por_efectivo"
    ),

]