from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Configura los permisos de los grupos del SIGESMP"

    def handle(self, *args, **kwargs):

        admin = Group.objects.get(name="Administrador")
        jefe = Group.objects.get(name="Jefe_MP")
        usuario = Group.objects.get(name="Usuario_MP")
        consulta = Group.objects.get(name="COMFAM_EA")

        # Limpiar permisos anteriores
        admin.permissions.clear()
        jefe.permissions.clear()
        usuario.permissions.clear()
        consulta.permissions.clear()

        # -----------------------------
        # ADMINISTRADOR
        # -----------------------------
        admin.permissions.set(Permission.objects.all())

        # -----------------------------
        # JEFE_MP
        # -----------------------------
        permisos_jefe = [
            "view_caso",
            "add_caso",
            "aprobar_modificacion",
            "aprobar_archivado",
            "change_solicitudmodificacion",
            "view_solicitudmodificacion",
        ]

        for codename in permisos_jefe:
            try:
                jefe.permissions.add(
                    Permission.objects.get(codename=codename)
                )
            except Permission.DoesNotExist:
                pass

        # -----------------------------
        # USUARIO_MP
        # -----------------------------
        permisos_usuario = [
            "view_caso",
            "add_caso",
            "add_solicitudmodificacion",
            "view_solicitudmodificacion",
        ]

        for codename in permisos_usuario:
            try:
                usuario.permissions.add(
                    Permission.objects.get(codename=codename)
                )
            except Permission.DoesNotExist:
                pass

        # -----------------------------
        # COMFAM_EA
        # -----------------------------
        consulta.permissions.add(
            Permission.objects.get(codename="view_caso")
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Permisos configurados correctamente."
            )
        )