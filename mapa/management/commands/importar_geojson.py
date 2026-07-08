import json
from datetime import datetime

from django.core.management.base import BaseCommand
from mapa.models import Caso


def texto(valor):
    """Convierte None en cadena vacía."""
    if valor is None:
        return ""
    return str(valor).strip()


def fecha(valor):
    """Convierte YYYY-MM-DD a date. Si no puede, devuelve None."""
    valor = texto(valor)

    if valor == "" or valor.upper() == "SIN FECHA":
        return None

    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except:
        return None


class Command(BaseCommand):
    help = "Importa los casos desde un archivo GeoJSON"

    def handle(self, *args, **options):

        ruta = "mapa/static/mapa/monitoreo_casos.geojson"

        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        print("Eliminando registros anteriores...")
        Caso.objects.all().delete()

        importados = 0
        errores = 0

        for i, feature in enumerate(datos["features"], start=1):

            try:

                propiedades = feature.get("properties", {})
                geometria = feature.get("geometry") or {}

                if geometria.get("type") != "Point":
                    print(f"Registro {i}: geometría inválida.")
                    errores += 1
                    continue

                coordenadas = geometria.get("coordinates", [])

                if len(coordenadas) < 2:
                    print(f"Registro {i}: sin coordenadas.")
                    errores += 1
                    continue

                Caso.objects.create(

                    beneficiario=texto(propiedades.get("BENEFICIARIO")),
                    domicilio=texto(propiedades.get("DOMICILIO")),
                    nivel_riesgo=texto(propiedades.get("NIVEL RIESGO")).upper(),
                    distrito=texto(propiedades.get("Distrito")).upper(),
                    comisaria=texto(propiedades.get("COMISARIA DE LA JURISDICCIÓN")),
                    efectivo=texto(propiedades.get("EFECTIVO")),
                    folder=texto(propiedades.get("FOLDER")),
                    expediente=texto(propiedades.get("EXP.")),
                    agresor=texto(propiedades.get("AGRES.")),
                    telefono=texto(propiedades.get("TELEFONO")),

                    fecha_registro=fecha(propiedades.get("fecha_registro")),
                    ultima_visita=fecha(propiedades.get("ULTIMA VISITA")),
                    fecha_limite=fecha(propiedades.get("FECHA LIMITE DE SEGUIMIENTO")),

                    notificacion=(
                        "SI"
                        if texto(propiedades.get("NOTIFICACIÓN")).upper() == "SI"
                        else "NO"
                    ),

                    latitud=float(coordenadas[1]),
                    longitud=float(coordenadas[0]),
                )

                importados += 1

            except Exception as e:

                errores += 1
                print(f"\nError en el registro {i}")
                print(e)
                print(propiedades)
                print("-" * 60)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImportación finalizada.\n"
                f"Casos importados: {importados}\n"
                f"Errores: {errores}"
            )
        )