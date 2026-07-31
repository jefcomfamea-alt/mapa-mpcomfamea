from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Region(models.Model):

    id_ubigeo = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    codigo_ubigeo = models.CharField(
        max_length=10,
        blank=True
    )

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.nombre


class Provincia(models.Model):

    id_ubigeo = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    codigo_ubigeo = models.CharField(
        max_length=10,
        blank=True
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="provincias"
    )

    nombre = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.nombre


class Distrito(models.Model):

    id_ubigeo = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    codigo_ubigeo = models.CharField(
        max_length=10,
        blank=True
    )

    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name="distritos"
    )

    nombre = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.nombre

class Caso(models.Model):

    RIESGOS = [
        ("LEVE", "Leve"),
        ("MODERADO", "Moderado"),
        ("SEVERO", "Severo"),
        ("SEVERO EXTREMO", "Severo extremo"),
        ("NO DETERMINADO", "No determinado"),
    ]

    NOTIFICACION = [
        ("PENDIENTE", "Pendiente"),
        ("NOTIFICADO", "Notificado"),
    ]

    TIPO_VIOLENCIA = [
        ("FISICA", "Física"),
        ("PSICOLOGICA", "Psicológica"),
        ("SEXUAL", "Sexual"),
        ("ECONOMICA", "Económica o Patrimonial"),
    ]

    ESTADO_UBICACION_AGRESOR = [
        ("UBICADO", "Ubicado"),
        ("NO UBICADO", "No ubicado"),
    ]


    beneficiario = models.CharField(max_length=200, blank=True)

    dni_beneficiario = models.CharField(
        max_length=8,
        blank=True
    )

    domicilio = models.CharField(max_length=300, blank=True)

    nivel_riesgo = models.CharField(
        max_length=30,
        choices=RIESGOS,
        blank=True
    )

    # Ubicación de la denuncia
    region_denuncia = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="casos_denuncia_region",
        null=True,
        blank=True,
    )

    provincia_denuncia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        related_name="casos_denuncia_provincia",
        null=True,
        blank=True,
    )

    distrito_denuncia = models.ForeignKey(
        Distrito,
        on_delete=models.PROTECT,
        related_name="casos_denuncia_distrito",
        null=True,
        blank=True,
    )

    # Ubicación de la medida
    region_medida = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="casos_medida_region",
        null=True,
        blank=True,
    )

    provincia_medida = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        related_name="casos_medida_provincia",
        null=True,
        blank=True,
    )

    distrito_medida = models.ForeignKey(
        Distrito,
        on_delete=models.PROTECT,
        related_name="casos_medida_distrito",
        null=True,
        blank=True,
)
    
    comisaria_denuncia = models.CharField(
        max_length=150,
        verbose_name="Comisaría donde se interpuso la denuncia"
    )

    comisaria_medida = models.CharField(
        max_length=150,
        verbose_name="Comisaría de Familia responsable"
    )

    efectivo = models.CharField(max_length=100, blank=True)

    responsable = models.ForeignKey(
    User,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="casos_asignados"
    )

    folder = models.CharField(max_length=100, blank=True)

    expediente = models.CharField(max_length=100, blank=True)

    agresor = models.CharField(
        max_length=200,
        blank=True
    )
    
    dni_agresor = models.CharField(
        max_length=8,
        blank=True
    )

    telefono_agresor = models.CharField(
        "Teléfono del agresor",
        max_length=50,
        blank=True
    )

    direccion_agresor = models.CharField(
        "Dirección del agresor",
        max_length=300,
        blank=True
    )

    estado_ubicacion_agresor = models.CharField(
        "Estado de ubicación del agresor",
        max_length=15,
        choices=ESTADO_UBICACION_AGRESOR,
        default="NO UBICADO"
    )

    latitud_agresor = models.FloatField(
        null=True,
        blank=True
    )

    longitud_agresor = models.FloatField(
        null=True,
        blank=True
    )

    telefono = models.CharField(
        "Teléfono de la beneficiaria",
        max_length=50,
        blank=True
    )

    fecha_denuncia = models.DateField(
        "Fecha de la denuncia",
        null=True,
        blank=True
    )

    violencia_fisica = models.BooleanField(
        "Violencia física",
        default=False
    )

    violencia_psicologica = models.BooleanField(
        "Violencia psicológica",
        default=False
    )

    violencia_sexual = models.BooleanField(
        "Violencia sexual",
        default=False
    ) 

    violencia_economica = models.BooleanField(
        "Violencia económica o patrimonial",
        default=False
    )
    
    fecha_registro = models.DateField(
        null=True,
        blank=True
    )

    ultima_visita = models.DateField(
        null=True,
        blank=True
    )

    fecha_limite = models.DateField(
        "Próximo seguimiento",
        null=True,
        blank=True
)

    notificacion_beneficiario = models.CharField(
        max_length=15,
        choices=NOTIFICACION,
        default="PENDIENTE"
    )

    fecha_notificacion_beneficiario = models.DateField(
        null=True,
        blank=True
    )

    motivo_notificacion_beneficiario_pendiente = models.TextField(
        "Motivo de notificación pendiente de la persona beneficiaria",
        blank=True
    )

    notificacion_agresor = models.CharField(
        max_length=15,
        choices=NOTIFICACION,
        default="PENDIENTE"
    )

    fecha_notificacion_agresor = models.DateField(
        null=True,
        blank=True
    )

    motivo_notificacion_agresor_pendiente = models.TextField(
        "Motivo de notificación pendiente de la persona agresora",
        blank=True
    )

    estado = models.CharField(
        max_length=15,
        default="ACTIVO"
    )

    latitud = models.FloatField(
        null=True,
        blank=True
    )

    longitud = models.FloatField(
        null=True,
        blank=True
    )

    edicion_autorizada = models.BooleanField(
        default=False
    )

    agresor_registro = models.ForeignKey(
        "Agresor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="casos"
    )

    def save(self, *args, **kwargs):

        # Beneficiaria
        if self.notificacion_beneficiario == "NOTIFICADO":
            self.motivo_notificacion_beneficiario_pendiente = ""
            self.fecha_notificacion_beneficiario = (
                self.fecha_notificacion_beneficiario
                or timezone.now().date()
            )

        # Agresor
        if self.notificacion_agresor == "NOTIFICADO":
            self.motivo_notificacion_agresor_pendiente = ""
            self.fecha_notificacion_agresor = (
                self.fecha_notificacion_agresor
                or timezone.now().date()
            )

        if self.ultima_visita:

            if self.nivel_riesgo in ["SEVERO", "SEVERO EXTREMO"]:
                self.fecha_limite = self.ultima_visita + relativedelta(months=3)

            else:
                self.fecha_limite = self.ultima_visita + relativedelta(months=6)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.beneficiario

    class Meta:
        permissions = [
            ("modificar_directo", "Puede modificar casos directamente"),
            ("aprobar_modificacion", "Puede aprobar modificaciones"),
            ("archivar_directo", "Puede archivar casos directamente"),
            ("aprobar_archivado", "Puede aprobar archivados"),
            ("eliminar_directo", "Puede eliminar casos directamente"),
            ("aprobar_eliminacion", "Puede aprobar eliminaciones"),
            ("administrar_usuarios", "Puede administrar usuarios"),
        ]

class UbicacionPreliminar(models.Model):

    TIPO_UBICACION = [
        ("CONOCIDO", "Agresor con domicilio conocido"),
        ("DESCONOCIDO", "Agresor sin domicilio conocido"),
    ]

    ESTADO = [
        ("PRELIMINAR", "Preliminar"),
        ("CONVERTIDA", "Convertida en medida"),
        ("VENCIDA", "Vencida"),
    ]


    # DATOS BENEFICIARIA

    beneficiaria = models.CharField(
        max_length=200
    )

    dni_beneficiaria = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    domicilio = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    referencia = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    tipo_ubicacion = models.CharField(
        max_length=20,
        choices=TIPO_UBICACION,
        default="CONOCIDO"
    )


    # DATOS AGRESOR

    agresor = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    dni_agresor = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    direccion_agresor = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )


    estado_ubicacion_agresor = models.CharField(
        max_length=20,
        choices=TIPO_UBICACION,
        default="CONOCIDO"
    )


    latitud_agresor = models.FloatField(
        null=True,
        blank=True
    )

    longitud_agresor = models.FloatField(
        null=True,
        blank=True
    )


    # UBICACIÓN BENEFICIARIA

    latitud = models.FloatField(
        null=True,
        blank=True
    )

    longitud = models.FloatField(
        null=True,
        blank=True
    )


    # CONTROL

    estado = models.CharField(
        max_length=20,
        choices=ESTADO,
        default="PRELIMINAR"
    )


    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )


    fecha_vencimiento = models.DateField(
        null=True,
        blank=True
    )


    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def save(self, *args, **kwargs):

        if not self.fecha_vencimiento:
            from datetime import timedelta

            self.fecha_vencimiento = (
                timezone.now().date()
                + timedelta(days=30)
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return self.beneficiaria
    
    def clean(self):

        estado = self.estado_ubicacion_agresor

        direccion = self.direccion_agresor

        latitud_agresor = self.latitud_agresor

        longitud_agresor = self.longitud_agresor

        from django.core.exceptions import ValidationError

        if estado == "CONOCIDO":

            if not direccion:
                raise ValidationError({
                    "direccion_agresor":
                    "Debe registrar la dirección del agresor cuando se encuentra ubicado."
                })

            if latitud_agresor is None or longitud_agresor is None:
                raise ValidationError({
                    "latitud_agresor":
                    "Debe ubicar al agresor en el mapa."
                })

        if estado == "DESCONOCIDO":

            self.direccion_agresor = ""
            self.latitud_agresor = None
            self.longitud_agresor = None

class SolicitudModificacion(models.Model):

    ESTADOS = [
    ("PENDIENTE", "Pendiente"),
    ("APROBADA", "Aprobada"),
    ("UTILIZADA", "Utilizada"),
    ("RECHAZADA", "Rechazada"),
]

    caso = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE
    )

    solicitante = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    motivo = models.TextField()

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default="PENDIENTE"
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    autorizado_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="autorizaciones_modificacion"
    )

    fecha_autorizacion = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_utilizacion = models.DateTimeField(
    null=True,
    blank=True
    )

    def __str__(self):
        return f"Solicitud #{self.id} - Caso {self.caso.id}"
    
class Mensaje(models.Model):

    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mensajes_recibidos"
    )

    caso = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE,
        related_name="mensajes"
    )

    asunto = models.CharField(
        max_length=200
    )

    contenido = models.TextField()

    leido = models.BooleanField(
        default=False
    )

    fecha_lectura = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.asunto} - {self.destinatario.username}"
    
class Agresor(models.Model):

    nombres = models.CharField(
        max_length=150
    )

    dni = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    alias = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    domicilio = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    latitud = models.FloatField(
        blank=True,
        null=True
    )

    longitud = models.FloatField(
        blank=True,
        null=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    activo = models.BooleanField(
        default=True
    )


    def __str__(self):
        return self.nombres