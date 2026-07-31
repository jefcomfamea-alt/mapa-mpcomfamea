from django.contrib import admin
from .models import (
    Caso,
    SolicitudModificacion,
    UbicacionPreliminar,
)
from .models import Agresor

admin.site.register(Caso)
admin.site.register(SolicitudModificacion)
admin.site.register(UbicacionPreliminar)
@admin.register(Agresor)
class AgresorAdmin(admin.ModelAdmin):

    list_display = (
        "nombres",
        "dni",
        "domicilio",
        "activo",
        "fecha_registro",
    )

    search_fields = (
        "nombres",
        "dni",
    )