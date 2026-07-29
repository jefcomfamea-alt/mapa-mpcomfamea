from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

from .forms import CasoForm
from .models import Caso, SolicitudModificacion, Mensaje
from .decorators import grupo_requerido
from .forms_solicitudes import SolicitudModificacionForm


@login_required
def inicio(request):

    pendientes_mensajes = Mensaje.objects.filter(
        destinatario=request.user,
        leido=False
    ).count()

    hoy = timezone.now().date()
    limite = hoy + timedelta(days=3)

    if (
        request.user.is_superuser
        or request.user.groups.filter(
            name__in=["Administrador", "Jefe_MP"]
        ).exists()
    ):

        notificaciones = Caso.objects.filter(
            estado="ACTIVO",
            fecha_limite__isnull=False,
            fecha_limite__lte=limite
        ).filter(
            Q(fecha_registro__year__gte=2026) |
            Q(ultima_visita__year__gte=2026)
        ).order_by("fecha_limite")

    else:

        notificaciones = Caso.objects.filter(
            estado="ACTIVO",
            responsable=request.user,
            fecha_limite__isnull=False,
            fecha_limite__lte=limite
        ).filter(
            Q(fecha_registro__year__gte=2026) |
            Q(ultima_visita__year__gte=2026)
        ).order_by("fecha_limite")


    pendientes_casos = notificaciones.count()

    pendientes = pendientes_mensajes + pendientes_casos


    es_admin = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )


    return render(
        request,
        "mapa/inicio.html",
        {
            "pendientes": pendientes,
            "es_admin": es_admin,
            "notificaciones": notificaciones,
        }
    )

@login_required
def notificaciones(request):

    hoy = timezone.now().date()
    limite = hoy + timedelta(days=3)

    if (
        request.user.is_superuser
        or request.user.groups.filter(
            name__in=["Administrador", "Jefe_MP"]
        ).exists()
    ):

        notificaciones = Caso.objects.filter(
            estado="ACTIVO",
            fecha_limite__isnull=False,
            fecha_limite__lte=limite
        ).filter(
            Q(fecha_registro__year__gte=2026) |
            Q(ultima_visita__year__gte=2026)
        ).order_by("fecha_limite")

    else:

        notificaciones = Caso.objects.filter(
            estado="ACTIVO",
            responsable=request.user,
            fecha_limite__isnull=False,
            fecha_limite__lte=limite
        ).filter(
            Q(fecha_registro__year__gte=2026) |
            Q(ultima_visita__year__gte=2026)
        ).order_by("fecha_limite")

    return render(
        request,
        "mapa/notificaciones.html",
        {
            "notificaciones": notificaciones,
            "hoy": hoy,
        }
    )

@login_required
@grupo_requerido("Administrador")
def administrar_usuarios(request):

    usuarios = User.objects.all().order_by("username")

    grupos = Group.objects.all().order_by("name")

    return render(
        request,
        "mapa/administrar_usuarios.html",
        {
            "usuarios": usuarios,
            "grupos": grupos
        }
    )

@login_required
@grupo_requerido("Administrador")
def editar_usuario(request, pk):

    usuario = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        usuario.username = request.POST.get("username")
        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")
        usuario.email = request.POST.get("email")

        password = request.POST.get("password")

        if password:
            usuario.set_password(password)

        usuario.save()

        rol = request.POST.get("rol")

        if rol:

            grupo = Group.objects.get(name=rol)

            usuario.groups.clear()

            usuario.groups.add(grupo)

        return redirect("administrar_usuarios")

    grupo_actual = usuario.groups.first()

    return render(
        request,
        "mapa/editar_usuario.html",
        {
            "usuario": usuario,
            "grupo_actual": grupo_actual,
        }
    )

@login_required
@grupo_requerido("Administrador")
def nuevo_usuario(request):

    if request.method == "POST":

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rol = request.POST.get("rol")

        usuario = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        grupo = Group.objects.get(name=rol)

        usuario.groups.add(grupo)

        return redirect("administrar_usuarios")

    return render(
        request,
        "mapa/nuevo_usuario.html"
    )

@login_required
@grupo_requerido("Administrador")
def desactivar_usuario(request, pk):

    usuario = get_object_or_404(User, pk=pk)

    usuario.is_active = False
    usuario.save()

    return redirect("administrar_usuarios")

@login_required
@grupo_requerido("Administrador", "Jefe_MP", "Usuario_MP")
def nuevo_caso(request):

    if request.method == "POST":

        form = CasoForm(
            request.POST,
            usuario=request.user
        )

        if form.is_valid():

            caso = form.save(commit=False)

            if caso.responsable:

                nombre = f"{caso.responsable.first_name} {caso.responsable.last_name}".strip()
                caso.efectivo = nombre if nombre else caso.responsable.username

                caso.edicion_autorizada = False

            caso.save()

            form.save_m2m()

            if caso.responsable:

                Mensaje.objects.create(
                    destinatario=caso.responsable,
                    caso=caso,
                    asunto="🔔 Nuevo caso asignado",
                    contenido=(
                        f"Se le comunica que se le ha asignado "
                        f"el expediente N.° "
                        f"{caso.expediente or caso.folder} "
                        f"para realizar la ejecución y seguimiento "
                        f"de las medidas de protección."
        )
    )

            return redirect("inicio")

        else:
            print(form.errors)

    else:

        lat = request.GET.get("lat")
        lng = request.GET.get("lng")

        form = CasoForm(
            usuario=request.user,
            initial={
                "latitud": lat,
                "longitud": lng,
            }
        )

    return render(
        request,
        "mapa/nuevo_caso.html",
        {
            "form": form
        }
    )


@login_required
def gestion_casos(request):

    from django.core.paginator import Paginator

    casos = Caso.objects.filter(
        estado="ACTIVO"
    ).order_by("-id")

    paginador = Paginator(casos, 20)

    pagina = request.GET.get("page")

    casos = paginador.get_page(pagina)

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

    for caso in Caso.objects.filter(estado="ACTIVO"):

        if caso.latitud is None or caso.longitud is None:
            continue

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

                "NOTIFICACION BENEFICIARIO": caso.notificacion_beneficiario,
                "FECHA NOTIFICACION BENEFICIARIO": str(caso.fecha_notificacion_beneficiario) if caso.fecha_notificacion_beneficiario else "",

                "NOTIFICACION AGRESOR": caso.notificacion_agresor,
                "FECHA NOTIFICACION AGRESOR": str(caso.fecha_notificacion_agresor) if caso.fecha_notificacion_agresor else "",
            }
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })


@login_required
def editar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    # Marcar como leído el mensaje del usuario para este caso
    Mensaje.objects.filter(
        destinatario=request.user,
        caso=caso,
        leido=False
    ).update(
        leido=True,
        fecha_lectura=timezone.now()
    )

    es_admin = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )

    es_jefe = request.user.groups.filter(
        name="Jefe_MP"
    ).exists()

    es_usuario = request.user.groups.filter(
        name="Usuario_MP"
    ).exists()

    es_responsable = (
        caso.responsable == request.user
    )

    # Administrador y Jefe siempre pueden editar
    if es_admin or es_jefe:
        pass

    # El responsable puede editar si tiene autorización
    elif es_responsable and caso.edicion_autorizada:
        pass

    # Si llegó desde un mensaje que le pertenece, se habilita la primera edición
    elif Mensaje.objects.filter(
        caso=caso,
        destinatario=request.user
    ).exists():

        caso.edicion_autorizada = True
        caso.save()

    else:
        return redirect("gestion_casos")

    if request.method == "POST":

        form = CasoForm(
            request.POST,
            instance=caso,
            usuario=request.user
        )

        if form.is_valid():

            caso = form.save(commit=False)

            if caso.responsable:
                nombre = f"{caso.responsable.first_name} {caso.responsable.last_name}".strip()
                caso.efectivo = nombre if nombre else caso.responsable.username

            caso.save()

            if es_responsable:

                caso.edicion_autorizada = False
                caso.save()

            elif es_usuario:

                solicitud = SolicitudModificacion.objects.filter(
                    caso=caso,
                    solicitante=request.user,
                    estado="APROBADA"
                ).order_by("-fecha_autorizacion").first()

                if solicitud:

                    solicitud.estado = "UTILIZADA"
                    solicitud.fecha_utilizacion = timezone.now()
                    solicitud.save()

                    caso.edicion_autorizada = False
                    caso.save()

            return redirect("gestion_casos")

    else:

        form = CasoForm(
            instance=caso,
            usuario=request.user
        )

    return render(
        request,
        "mapa/nuevo_caso.html",
        {
            "form": form
        }
    )

@login_required
@grupo_requerido("Administrador")
def archivar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    caso.estado = "ARCHIVADO"
    caso.save()

    return redirect("gestion_casos")


@login_required
@grupo_requerido("Administrador")
def restaurar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)
    caso.estado = "ACTIVO"
    caso.save()

    return redirect("casos_archivados")

@login_required
@grupo_requerido("Administrador")
def archivar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    caso.estado = "ARCHIVADO"
    caso.save()

    return redirect("gestion_casos")


@login_required
@grupo_requerido("Administrador")
def casos_archivados(request):

    casos = Caso.objects.filter(
        estado="ARCHIVADO"
    ).order_by("-id")

    return render(
        request,
        "mapa/casos_archivados.html",
        {
            "casos": casos
        }
    )


@login_required
@grupo_requerido("Administrador")
def restaurar_caso(request, id):

    caso = get_object_or_404(Caso, pk=id)

    caso.estado = "ACTIVO"
    caso.save()

    return redirect("casos_archivados")

@login_required
@grupo_requerido("Jefe_MP", "Usuario_MP")
def solicitar_modificacion(request, id):

    caso = get_object_or_404(Caso, pk=id)

    if request.method == "POST":

        form = SolicitudModificacionForm(request.POST)

        if form.is_valid():

            solicitud = form.save(commit=False)
            solicitud.caso = caso
            solicitud.solicitante = request.user
            solicitud.save()

            return redirect("gestion_casos")

    else:

        form = SolicitudModificacionForm()

    return render(
        request,
        "mapa/solicitar_modificacion.html",
        {
            "form": form,
            "caso": caso
        }
    )

@login_required
@grupo_requerido(
    "Administrador",
    "Jefe_MP",
    "Usuario_MP"
)
def mensajes(request):

    mensajes_nuevos = Mensaje.objects.filter(
        destinatario=request.user,
        leido=False
    ).order_by("-fecha")

    historial_mensajes = Mensaje.objects.filter(
        destinatario=request.user,
        leido=True
    ).order_by("-fecha_lectura", "-fecha")

    solicitudes = SolicitudModificacion.objects.filter(
        estado="PENDIENTE"
    ).order_by("-fecha")


    hoy = timezone.now().date()
    limite = hoy + timedelta(days=3)

    casos_por_vencer = Caso.objects.filter(
        estado="ACTIVO",
        fecha_limite__isnull=False,
        fecha_limite__gte=hoy,
        fecha_limite__lte=limite
    ).filter(
        Q(fecha_registro__year__gte=2026) |
        Q(ultima_visita__year__gte=2026)
    ).order_by("fecha_limite")

    return render(
        request,
        "mapa/mensajes.html",
        {
            "mensajes_nuevos": mensajes_nuevos,
            "historial_mensajes": historial_mensajes,
            "solicitudes": solicitudes,
            "casos_por_vencer": casos_por_vencer,
        }
    )
def cerrar_sesion(request):
    logout(request)
    return redirect("/accounts/login/")

@login_required
def buscar_caso(request):

    texto = request.GET.get("q", "").strip()

    if texto == "":
        return JsonResponse({
            "encontrado": False
        })

    caso = Caso.objects.filter(

        Q(beneficiario__icontains=texto) |
        Q(expediente__icontains=texto) |
        Q(folder__icontains=texto) |
        Q(dni_beneficiario__icontains=texto) |
        Q(agresor__icontains=texto) |
        Q(dni_agresor__icontains=texto)

    ).first()

    if caso is None:
        return JsonResponse({
            "encontrado": False
        })

    return JsonResponse({

        "encontrado": True,

        "latitud": caso.latitud,
        "longitud": caso.longitud,

        "beneficiario": caso.beneficiario,
        "expediente": caso.expediente,
        "folder": caso.folder,
        "riesgo": caso.nivel_riesgo

    })


@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def aprobar_solicitud(request, id):

    solicitud = get_object_or_404(
        SolicitudModificacion,
        pk=id
    )

    solicitud.estado = "APROBADA"
    solicitud.autorizado_por = request.user
    solicitud.fecha_autorizacion = timezone.now()
    solicitud.save()

    caso = solicitud.caso
    caso.edicion_autorizada = True
    caso.save()

    return redirect("mensajes")

@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def rechazar_solicitud(request, id):

    solicitud = get_object_or_404(
        SolicitudModificacion,
        pk=id
    )

    solicitud.estado = "RECHAZADA"
    solicitud.autorizado_por = request.user
    solicitud.fecha_autorizacion = timezone.now()
    solicitud.save()

    return redirect("mensajes")