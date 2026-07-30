import json
from pathlib import Path

from django.core.management.base import BaseCommand
from mapa.models import Region, Provincia, Distrito


class Command(BaseCommand):

    help = "Carga los ubigeos nacionales del Perú"

    def handle(self, *args, **kwargs):

        # Ruta principal del proyecto
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

        # Carpeta donde están los archivos JSON
        UBIGEOS_DIR = BASE_DIR / "ubigeos"

        departamentos_file = UBIGEOS_DIR / "departamentos.json"
        provincias_file = UBIGEOS_DIR / "provincias.json"
        distritos_file = UBIGEOS_DIR / "distritos.json"

        # Verificar que existan los tres archivos
        for archivo in [
            departamentos_file,
            provincias_file,
            distritos_file,
        ]:
            if not archivo.exists():
                self.stdout.write(
                    self.style.ERROR(
                        f"No se encontró el archivo: {archivo}"
                    )
                )
                return

        # Leer departamentos
        with open(
            departamentos_file,
            "r",
            encoding="utf-8"
        ) as archivo:
            departamentos = json.load(archivo)

        # Leer provincias
        with open(
            provincias_file,
            "r",
            encoding="utf-8"
        ) as archivo:
            provincias = json.load(archivo)

        # Leer distritos
        with open(
            distritos_file,
            "r",
            encoding="utf-8"
        ) as archivo:
            distritos = json.load(archivo)

        # ==================================
        # CARGAR REGIONES
        # ==================================

        regiones_procesadas = 0

        for dato in departamentos:

            nombre_region = dato["nombre_ubigeo"].upper()

            region = Region.objects.filter(
                id_ubigeo=dato["id_ubigeo"]
            ).first()

            if region is None:

                region = Region.objects.filter(
                    nombre=nombre_region
                ).first()

            if region:

                region.id_ubigeo = dato["id_ubigeo"]
                region.codigo_ubigeo = dato.get(
                    "codigo_ubigeo",
                    ""
                )
                region.nombre = nombre_region
                region.save()

            else:

                Region.objects.create(
                    id_ubigeo=dato["id_ubigeo"],
                    codigo_ubigeo=dato.get(
                        "codigo_ubigeo",
                        ""
            ),
        nombre=nombre_region,
    )

            regiones_procesadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Regiones procesadas: "
                f"{regiones_procesadas}"
            )
        )

        # ==================================
        # CARGAR PROVINCIAS
        # ==================================

        provincias_procesadas = 0

        for id_region, lista_provincias in provincias.items():

            try:
                region = Region.objects.get(
                    id_ubigeo=id_region
                )

            except Region.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"No se encontró la región "
                        f"con ID {id_region}"
                    )
                )

                continue

            for dato in lista_provincias:

                Provincia.objects.update_or_create(
                    id_ubigeo=dato["id_ubigeo"],
                    defaults={
                        "codigo_ubigeo": dato.get(
                            "codigo_ubigeo",
                            ""
                        ),
                        "nombre": dato[
                            "nombre_ubigeo"
                        ].upper(),
                        "region": region,
                    }
                )

                provincias_procesadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Provincias procesadas: "
                f"{provincias_procesadas}"
            )
        )

        # ==================================
        # CARGAR DISTRITOS
        # ==================================

        distritos_procesados = 0

        for id_provincia, lista_distritos in distritos.items():

            try:
                provincia = Provincia.objects.get(
                    id_ubigeo=id_provincia
                )

            except Provincia.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"No se encontró la provincia "
                        f"con ID {id_provincia}"
                    )
                )

                continue

            for dato in lista_distritos:

                Distrito.objects.update_or_create(
                    id_ubigeo=dato["id_ubigeo"],
                    defaults={
                        "codigo_ubigeo": dato.get(
                            "codigo_ubigeo",
                            ""
                        ),
                        "nombre": dato[
                            "nombre_ubigeo"
                        ].upper(),
                        "provincia": provincia,
                    }
                )

                distritos_procesados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Distritos procesados: "
                f"{distritos_procesados}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nUBIGEOS NACIONALES "
                "CARGADOS CORRECTAMENTE"
            )
        )