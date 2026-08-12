from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from mapa.models import Caso


class Command(BaseCommand):

    help = "Elimina definitivamente los casos que llevan 30 días en la papelera."

    def handle(self, *args, **options):

        fecha_limite = timezone.now() - timedelta(days=30)

        casos = Caso.objects.filter(
            estado="ELIMINADO",
            fecha_eliminacion__isnull=False,
            fecha_eliminacion__lte=fecha_limite
        )

        cantidad = casos.count()

        casos.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Se eliminaron definitivamente {cantidad} caso(s)."
            )
        )