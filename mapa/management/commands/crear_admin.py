from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Crea un usuario administrador si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "Admin")
        password = os.environ.get("ADMIN_PASSWORD", "Admin123456")
        email = os.environ.get("ADMIN_EMAIL", "")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"El usuario '{username}' ya existe."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado correctamente."))