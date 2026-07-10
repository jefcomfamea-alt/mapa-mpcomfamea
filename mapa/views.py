from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import CasoForm
from .models import Caso


@login_required
def inicio(request):
    return render(request, "mapa/inicio.html")


@login_required
def nuevo_caso(request):

    if request.method == "POST":

        form = CasoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("inicio")
        else:
            print(form.errors)

    else:

        lat = request.GET.get("lat")
        lng = request.GET.get("lng")

        form = CasoForm(initial={
            "latitud": lat,
            "longitud": lng,
        })

    return render(request, "mapa/nuevo_caso.html", {
        "form": form
    })

@login_required
def gestion_casos(request):

    casos = Caso.objects.filter(estado="ACTIVO").order_by("-id")

    return render(
        request,
        "mapa/gestion_casos.html",
        {
            "casos": casos
        }
    )


@login_required
def casos_json(request):

    features = []

    for caso in Caso.objects.all():

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [caso.longitud, caso.latitud]
            },
            "properties": {
                "BENEFICIARIO": caso.beneficiario,
                "DOMICILIO": caso.domicilio,
                "NIVEL RIESGO": caso.nivel_riesgo,
                "DISTRITO": caso.distrito,
                "COMISARIA DE LA JURISDICCIÓN": caso.comisaria,
                "EFECTIVO": caso.efectivo,
                "FOLDER": caso.folder,
                "EXP.": caso.expediente,
                "AGRESOR": caso.agresor,
                "TELEFONO": caso.telefono,
                "fecha_registro": str(caso.fecha_registro) if caso.fecha_registro else "",
                "ULTIMA VISITA": str(caso.ultima_visita) if caso.ultima_visita else "",
                "FECHA LIMITE DE SEGUIMIENTO": str(caso.fecha_limite) if caso.fecha_limite else "",
                "NOTIFICACIÓN": caso.notificacion,
            }
            })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })

@login_required
def editar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    if request.method == "POST":

        form = CasoForm(request.POST, instance=caso)

        if form.is_valid():
            form.save()
            return redirect("gestion_casos")

    else:

        form = CasoForm(instance=caso)

    return render(request, "mapa/nuevo_caso.html", {
        "form": form
    })

def cerrar_sesion(request):
    logout(request)
    return redirect("/accounts/login/")

def archivar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    caso.estado = "ARCHIVADO"
    caso.save()

    return redirect("gestion_casos")

@login_required
def restaurar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    caso.estado = "ACTIVO"
    caso.save()

    return redirect("casos_archivados")

@login_required
def casos_archivados(request):

    casos = Caso.objects.filter(estado="ARCHIVADO").order_by("-id")

    return render(request, "mapa/casos_archivados.html", {
        "casos": casos
    })