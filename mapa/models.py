from django.db import models


class Caso(models.Model):

    RIESGOS = [
        ("LEVE", "LEVE"),
        ("MODERADO", "MODERADO"),
        ("SEVERO1", "SEVERO1"),
        ("SEVERO2", "SEVERO2"),
        ("NO DETERMINADO", "NO DETERMINADO"),
    ]

    NOTIFICACION = [
        ("SI", "SI"),
        ("NO", "NO"),
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

    telefono = models.CharField(max_length=50, blank=True)

    fecha_registro = models.DateField(null=True, blank=True)

    ultima_visita = models.DateField(null=True, blank=True)

    fecha_limite = models.DateField(null=True, blank=True)

    notificacion = models.CharField(max_length=100)

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

    def __str__(self):
        return self.beneficiario