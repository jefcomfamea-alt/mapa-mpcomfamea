from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from django.utils import timezone


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

    DISTRITOS = [
        ("EL AGUSTINO", "EL AGUSTINO"),
        ("ATE", "ATE"),
        ("SANTA ANITA", "SANTA ANITA"),
        ("SAN LUIS", "SAN LUIS"),
        ("LA VICTORIA", "LA VICTORIA"),
        ("RIMAC", "RIMAC"),
        ("CERCADO DE LIMA", "CERCADO DE LIMA"),
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

    distrito = models.CharField(
        max_length=100,
        choices=DISTRITOS,
        blank=True
    )

    comisaria = models.CharField(max_length=200, blank=True)

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

    telefono = models.CharField(
        "Teléfono de la beneficiaria",
        max_length=50,
        blank=True
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