from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta


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

    folder = models.CharField(max_length=100, blank=True)

    expediente = models.CharField(max_length=100, blank=True)

    agresor = models.CharField(max_length=200, blank=True)

    dni_agresor = models.CharField(
        max_length=8,
        blank=True
    )

    telefono = models.CharField(max_length=50, blank=True)

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

    notificacion_agresor = models.CharField(
        max_length=15,
        choices=NOTIFICACION,
        default="PENDIENTE"
    )

    fecha_notificacion_agresor = models.DateField(
        null=True,
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

    def save(self, *args, **kwargs):

        if self.ultima_visita:

            if self.nivel_riesgo in ["SEVERO", "SEVERO EXTREMO"]:
                self.fecha_limite = self.ultima_visita + relativedelta(months=3)

            else:
                self.fecha_limite = self.ultima_visita + relativedelta(months=6)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.beneficiario


class SolicitudModificacion(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("APROBADA", "Aprobada"),
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

    def __str__(self):
        return f"Solicitud #{self.id} - Caso {self.caso.id}"