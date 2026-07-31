from django.contrib import admin
from .models import (
    Caso,
    SolicitudModificacion,
    UbicacionPreliminar,
)

admin.site.register(Caso)
admin.site.register(SolicitudModificacion)
admin.site.register(UbicacionPreliminar)