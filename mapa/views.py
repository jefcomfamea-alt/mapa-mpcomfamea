from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

from .forms import (
    CasoForm,
    UbicacionPreliminarForm
)
from .models import (
    Caso,
    SolicitudModificacion,
    Mensaje,
    Region,
    Provincia,
    Distrito,
    UbicacionPreliminar,
    PersonaPreliminar,
    RolPersonaPreliminar,
    Agresor
)
from .decorators import grupo_requerido
from .forms_solicitudes import SolicitudModificacionForm

def cargar_provincias(request):
    region_id = request.GET.get("region_id")

    provincias = Provincia.objects.filter(
        region_id=region_id
    ).order_by("nombre")

    data = [
        {
            "id": provincia.id,
            "nombre": provincia.nombre
        }
        for provincia in provincias
    ]

    return JsonResponse(data, safe=False)

def cargar_distritos(request):
    provincia_id = request.GET.get("provincia_id")

    distritos = Distrito.objects.filter(
        provincia_id=provincia_id
    ).order_by("nombre")

    data = [
        {
            "id": distrito.id,
            "nombre": distrito.nombre
        }
        for distrito in distritos
    ]

    return JsonResponse(data, safe=False)

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

    es_jefe = request.user.groups.filter(
        name="Jefe_MP"
    ).exists()

    es_usuario_mp = request.user.groups.filter(
        name="Usuario_MP"
    ).exists()

    es_efectivo_comfamea = request.user.groups.filter(
        name="Efectivo_COMFAMEA"
    ).exists()

    es_usuario_investigacion = request.user.groups.filter(
        name="Usuario_Investigacion"
    ).exists()

    return render(
        request,
        "mapa/inicio.html",
        {
            "pendientes": pendientes,
            "es_admin": es_admin,
            "es_jefe": es_jefe,
            "es_usuario_mp": es_usuario_mp,
            "es_efectivo_comfamea": es_efectivo_comfamea,
            "es_usuario_investigacion": es_usuario_investigacion,
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

    grupos = Group.objects.all().order_by("name")

    return render(
        request,
        "mapa/nuevo_usuario.html",
        {
            "grupos": grupos
        }
    )

@login_required
@grupo_requerido("Administrador")
def desactivar_usuario(request, pk):

    usuario = get_object_or_404(User, pk=pk)

    usuario.is_active = False
    usuario.save()

    return redirect("administrar_usuarios")

@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def seleccionar_rol_preliminar(request, id):

    persona = get_object_or_404(
        PersonaPreliminar,
        id=id
    )

    ubicacion = persona.ubicacion_preliminar


    personas = ubicacion.personas.prefetch_related(
        "roles"
    ).all()



    if request.method == "POST":

        rol = request.POST.get("rol")

        if rol:

            return redirect(
                f"/nuevo-caso/?preliminar={id}&rol={rol}"
            )


    return render(
        request,
        "mapa/seleccionar_rol_preliminar.html",
        {
            "ubicacion": ubicacion,
            "personas": personas,
            "persona_seleccionada": persona
        }
    )

@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def nuevo_caso(request):

    preliminar_id = request.GET.get("preliminar")
    rol = request.GET.get("rol")

    preliminar = None

    if preliminar_id:

        preliminar = get_object_or_404(
            PersonaPreliminar,
            id=preliminar_id
        )


    if request.method == "POST":

        form = CasoForm(
            request.POST,
            usuario=request.user
        )


        if form.is_valid():

            caso = form.save(commit=False)


            # =====================================
            # CARGAR DATOS DESDE PERSONA PRELIMINAR
            # =====================================

            if preliminar:


                if rol == "beneficiaria":

                    caso.beneficiario = preliminar.nombres
                    caso.dni_beneficiario = preliminar.dni
                    caso.telefono = preliminar.telefono
                    caso.domicilio = preliminar.direccion


                elif rol == "agresora":

                    caso.agresor = preliminar.nombres
                    caso.dni_agresor = preliminar.dni
                    caso.direccion_agresor = preliminar.direccion


                elif rol == "ambas":

                    caso.beneficiario = preliminar.nombres
                    caso.dni_beneficiario = preliminar.dni

                    caso.agresor = preliminar.nombres
                    caso.dni_agresor = preliminar.dni


                caso.latitud = preliminar.latitud
                caso.longitud = preliminar.longitud



            # =====================================
            # ASIGNACIÓN DE EFECTIVO RESPONSABLE
            # =====================================

            if caso.responsable:

                nombre = (
                    f"{caso.responsable.first_name} "
                    f"{caso.responsable.last_name}"
                ).strip()


                caso.efectivo = (
                    nombre
                    if nombre
                    else caso.responsable.username
                )


                caso.edicion_autorizada = False



            caso.save()


            form.save_m2m()



            # =====================================
            # MARCAR PERSONA PRELIMINAR CONVERTIDA
            # =====================================

            if preliminar:

                preliminar.convertida = True

                if rol:
                    preliminar.condicion_actual = rol.upper()

                preliminar.fecha_actualizacion_condicion = (
                    timezone.now()
                )

                preliminar.save()



            # =====================================
            # NOTIFICAR RESPONSABLE
            # =====================================

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


        datos_iniciales = {

            "latitud": lat,
            "longitud": lng,

        }



        # =====================================
        # CARGAR DATOS AL FORMULARIO
        # =====================================

        if preliminar:


            if rol == "beneficiaria":

                datos_iniciales.update({

                    "beneficiario": preliminar.nombres,

                    "dni_beneficiario": preliminar.dni,

                    "telefono": preliminar.telefono,

                    "domicilio": preliminar.direccion,

                })



            elif rol == "agresora":

                datos_iniciales.update({

                    "agresor": preliminar.nombres,

                    "dni_agresor": preliminar.dni,

                    "direccion_agresor": preliminar.direccion,

                })



            elif rol == "ambas":

                datos_iniciales.update({

                    "beneficiario": preliminar.nombres,

                    "dni_beneficiario": preliminar.dni,

                    "agresor": preliminar.nombres,

                    "dni_agresor": preliminar.dni,

                })



            datos_iniciales.update({

                "latitud": preliminar.latitud,

                "longitud": preliminar.longitud,

            })



        form = CasoForm(

            usuario=request.user,

            initial=datos_iniciales

        )



    return render(

        request,

        "mapa/nuevo_caso.html",

        {

            "form": form,

            "preliminar": preliminar,

            "rol": rol,

        }

    )

@login_required
@grupo_requerido(
    "Administrador",
    "Jefe_MP",
    "Usuario_Investigacion"
)
def registrar_ubicacion_preliminar(request):

    UbicacionPreliminar.objects.filter(
        estado="PRELIMINAR",
        fecha_vencimiento__lt=timezone.now().date()
    ).delete()


    if request.method == "POST":

        form = UbicacionPreliminarForm(request.POST)

        if form.is_valid():

            ubicacion = form.save(commit=False)

            ubicacion.registrado_por = request.user

            ubicacion.latitud = form.cleaned_data["latitud"]
            ubicacion.longitud = form.cleaned_data["longitud"]

            ubicacion.save()


                        # ==============================
            # GUARDAR PERSONAS INVOLUCRADAS
            # ==============================

            nombres = request.POST.getlist("nombres")
            dni = request.POST.getlist("dni")
            telefono = request.POST.getlist("telefono")
            direccion = request.POST.getlist("direccion")
            roles = request.POST.getlist("rol")
            latitudes = request.POST.getlist("latitud_persona")
            longitudes = request.POST.getlist("longitud_persona")


            for i in range(len(nombres)):

                if nombres[i]:

                    persona = PersonaPreliminar.objects.create(

                        ubicacion_preliminar=ubicacion,

                        nombres=nombres[i],

                        dni=dni[i] if i < len(dni) else "",

                        telefono=telefono[i] if i < len(telefono) else "",

                        direccion=direccion[i] if i < len(direccion) else "",

                        latitud=(
                            latitudes[i]
                            if i < len(latitudes) and latitudes[i]
                            else None
                        ),

                        longitud=(
                            longitudes[i]
                            if i < len(longitudes) and longitudes[i]
                            else None
                        )

                    )


                    if i < len(roles) and roles[i]:

                        RolPersonaPreliminar.objects.create(

                            persona=persona,

                            rol=roles[i]

                        )


            return redirect("inicio")


    else:

        form = UbicacionPreliminarForm()


    return render(
        request,
        "mapa/registrar_ubicacion_preliminar.html",
        {
            "form": form
        }
    )

@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def convertir_preliminar_caso(request, id):

    ubicacion = get_object_or_404(
        UbicacionPreliminar,
        pk=id
    )


    if ubicacion.estado == "CONVERTIDA":

        return redirect(
            "gestion_casos"
        )


    personas = ubicacion.personas.prefetch_related(
        "roles"
    ).all()


    if (
        request.method == "POST"
        and request.POST.get("confirmar_conversion") == "SI"
    ):


        beneficiarios = []

        agresores = []

        primer_agresor_registro = None



        # =====================================
        # CLASIFICAR PERSONAS
        # =====================================

        for persona in personas:


            seleccion = request.POST.get(
                f"persona_{persona.id}"
            )


            if seleccion not in [
                "BENEFICIARIO",
                "AGRESOR",
                "AMBOS"
            ]:

                continue



            persona.condicion_actual = seleccion

            persona.rol_confirmado = True

            persona.convertida = True

            persona.fecha_actualizacion_condicion = (
                timezone.now()
            )

            persona.motivo_actualizacion_condicion = (
                request.POST.get(
                    "motivo_condicion",
                    ""
                ).strip()
            )

            persona.save()



            if seleccion in [
                "BENEFICIARIO",
                "AMBOS"
            ]:

                beneficiarios.append(
                    persona
                )



            if seleccion in [
                "AGRESOR",
                "AMBOS"
            ]:

                agresores.append(
                    persona
                )



        # =====================================
        # VALIDAR BENEFICIARIO
        # =====================================

        if not beneficiarios:


            return render(

                request,

                "mapa/convertir_preliminar.html",

                {

                    "ubicacion": ubicacion,

                    "personas": personas,

                    "error":
                    "Debe seleccionar por lo menos una persona beneficiaria."

                }

            )



        alcance_medida = request.POST.get(
            "alcance_medida"
        )


        if alcance_medida not in [
            "UNA_PERSONA",
            "AMBAS_PERSONAS"
        ]:

            alcance_medida = "UNA_PERSONA"



        beneficiario_principal = (
            beneficiarios[0]
        )



        # =====================================
        # CREAR CASO
        # =====================================

        caso = Caso.objects.create(

            beneficiario=(
                beneficiario_principal.nombres
            ),

            dni_beneficiario=(
                beneficiario_principal.dni or ""
            ),

            domicilio=(
                beneficiario_principal.direccion or ""
            ),

            telefono=(
                beneficiario_principal.telefono or ""
            ),

            latitud=(
                beneficiario_principal.latitud
                if beneficiario_principal.latitud is not None
                else ubicacion.latitud
            ),

            longitud=(
                beneficiario_principal.longitud
                if beneficiario_principal.longitud is not None
                else ubicacion.longitud
            ),

            estado="ACTIVO",

            fecha_registro=(
                timezone.now().date()
            )

        )

                # =====================================
        # CREAR O VINCULAR AGRESOR(ES)
        # =====================================

        for persona in agresores:


            agresor_registro, creado = (
                Agresor.objects.get_or_create(

                    dni=persona.dni,

                    defaults={

                        "nombres": (
                            persona.nombres
                        ),

                        "alias": "",

                        "domicilio": (
                            persona.direccion or ""
                        ),

                        "latitud": (

                            persona.latitud
                            if persona.latitud is not None
                            else ubicacion.latitud

                        ),

                        "longitud": (

                            persona.longitud
                            if persona.longitud is not None
                            else ubicacion.longitud

                        ),

                        "activo": True

                    }

                )
            )



            # =====================================
            # SI YA EXISTÍA ACTUALIZAR DATOS
            # =====================================

            if not creado:


                agresor_registro.nombres = (
                    persona.nombres
                )


                agresor_registro.domicilio = (
                    persona.direccion or ""
                )


                agresor_registro.latitud = (

                    persona.latitud
                    if persona.latitud is not None
                    else ubicacion.latitud

                )


                agresor_registro.longitud = (

                    persona.longitud
                    if persona.longitud is not None
                    else ubicacion.longitud

                )


                agresor_registro.activo = True


                agresor_registro.save()



            # Guardar primer agresor encontrado

            if primer_agresor_registro is None:

                primer_agresor_registro = (
                    agresor_registro
                )



        # =====================================
        # VINCULAR AGRESOR AL CASO
        # =====================================

        if primer_agresor_registro:


            caso.agresor = (
                primer_agresor_registro.nombres
            )


            caso.dni_agresor = (
                primer_agresor_registro.dni or ""
            )


            caso.direccion_agresor = (
                primer_agresor_registro.domicilio or ""
            )


            caso.latitud_agresor = (
                primer_agresor_registro.latitud
            )


            caso.longitud_agresor = (
                primer_agresor_registro.longitud
            )


            caso.agresor_registro = (
                primer_agresor_registro
            )


            caso.save()



        # =====================================
        # FINALIZAR CONVERSIÓN
        # =====================================

        ubicacion.estado = "CONVERTIDA"


        ubicacion.alcance_medida = (
            alcance_medida
        )


        ubicacion.caso_generado = (
            caso
        )


        ubicacion.convertida_por = (
            request.user
        )


        ubicacion.fecha_conversion = (
            timezone.now()
        )


        ubicacion.save()



        return redirect(
            "gestion_casos"
        )



    # =====================================
    # MOSTRAR FORMULARIO
    # =====================================

    return render(

        request,

        "mapa/convertir_preliminar.html",

        {

            "ubicacion": ubicacion,

            "personas": personas,

        }

    )

@login_required
@grupo_requerido("Administrador", "Jefe_MP")
def convertir_agresor(request, id):

    persona = get_object_or_404(
        PersonaPreliminar,
        id=id
    )

    # Crear agresor definitivo

    Agresor.objects.create(

        nombres=persona.nombres,

        dni=persona.dni,

        alias="",

        domicilio=persona.direccion,

        latitud=persona.latitud,

        longitud=persona.longitud,

        activo=True

    )


    # Eliminar rol de agresor preliminar
    RolPersonaPreliminar.objects.filter(
        persona=persona,
        rol="DENUNCIADO"
    ).delete()


    return redirect("mapa_agresores")

@login_required
def gestion_casos(request):

    from django.core.paginator import Paginator
    from django.db.models import Q

    busqueda = request.GET.get("q", "")

    casos = Caso.objects.filter(
        estado="ACTIVO"
    )

    if busqueda:
        casos = casos.filter(
            Q(beneficiario__icontains=busqueda) |
            Q(dni_beneficiario__icontains=busqueda) |
            Q(expediente__icontains=busqueda)
        )

    casos = casos.order_by("-id")

    paginador = Paginator(casos, 20)

    pagina = request.GET.get("page")

    casos = paginador.get_page(pagina)

    return render(
        request,
        "mapa/gestion_casos.html",
        {
            "casos": casos,
            "busqueda": busqueda
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
                "id": caso.id,
                "BENEFICIARIO": caso.beneficiario,
                "DOMICILIO": caso.domicilio,
                "NIVEL RIESGO": caso.nivel_riesgo,
                "DISTRITO": str(caso.distrito_denuncia) if caso.distrito_denuncia else "",

                "COMISARIA DENUNCIA": caso.comisaria_denuncia,
                "COMISARIA MEDIDA": caso.comisaria_medida,

                "EFECTIVO": caso.efectivo,
                "RESPONSABLE_ID": caso.responsable.id if caso.responsable else None,
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
def ubicaciones_preliminares_json(request):

    features = []

    personas = PersonaPreliminar.objects.filter(
        latitud__isnull=False,
        longitud__isnull=False,
        ubicacion_preliminar__estado="PRELIMINAR"
    ).prefetch_related(
        "roles"
    )


    for persona in personas:

        roles = list(
            persona.roles.values_list(
                "rol",
                flat=True
            )
        )


        # ==================================
        # DETERMINAR TIPO DE PERSONA
        # ==================================

        tipo_color = None
        tipo_persona = None


        # Denunciante solo no aparece
        if (
            "DENUNCIANTE" in roles
            and len(roles) == 1
        ):
            continue


        # Presunta víctima
        if "PRESUNTA_VICTIMA" in roles:

            tipo_color = "AZUL"
            tipo_persona = "PRESUNTA VICTIMA"



        # Denunciado / presunto agresor
        if "DENUNCIADO" in roles:

            if tipo_color:

                tipo_color = "AMBOS"
                tipo_persona = "PARTICIPANTE"

            else:

                tipo_color = "MARRON"
                tipo_persona = "PRESUNTO AGRESOR"



        # Participante
        if "PARTICIPANTE" in roles:

            tipo_color = "AMBOS"
            tipo_persona = "PARTICIPANTE"



        # Si no tiene clasificación no mostrar
        if not tipo_color:
            continue



        features.append({

            "type": "Feature",

            "geometry": {

                "type": "Point",

                "coordinates": [

                    float(persona.longitud),

                    float(persona.latitud)

                ]

            },


            "properties": {

                "id": persona.id,

                "NOMBRE": persona.nombres,

                "DNI": persona.dni,

                "TELEFONO": persona.telefono,

                "DIRECCION": persona.direccion,

                "ROLES": roles,

                "TIPO": tipo_persona,

                "COLOR": tipo_color,

                "CONDICION_ACTUAL": persona.condicion_actual,

                "CONVERTIDA": persona.convertida,

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

    es_efectivo_comfamea = request.user.groups.filter(
        name="Efectivo_COMFAMEA"
    ).exists()

    es_usuario_investigacion = request.user.groups.filter(
        name="Usuario_Investigacion"
    ).exists()

    es_responsable = (
        caso.responsable == request.user
    )

    if es_efectivo_comfamea:
        return redirect("gestion_casos")
    
    # Administrador y Jefe siempre pueden editar
    if es_admin or es_jefe:
        pass

    # El responsable puede editar si tiene autorización
    elif es_responsable and caso.edicion_autorizada:
        pass

    # Si llegó desde un mensaje que le pertenece, se habilita la primera edición
    elif es_responsable:

        return redirect("solicitar_modificacion", id=caso.id)

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
    tipo = request.GET.get("tipo", "").strip()

    if texto == "":
        return JsonResponse({
            "encontrado": False,
            "casos": []
        })

    filtros = {
        "beneficiario": Q(beneficiario__icontains=texto),
        "agresor": Q(agresor__icontains=texto),
        "dni": Q(dni_beneficiario__icontains=texto),
        "expediente": Q(expediente__icontains=texto),
        "folder": Q(folder__icontains=texto),
    }

    if tipo in filtros:
        casos = Caso.objects.filter(
            filtros[tipo]
        ).order_by("beneficiario")
    else:
        casos = Caso.objects.filter(
            Q(beneficiario__icontains=texto) |
            Q(agresor__icontains=texto) |
            Q(dni_beneficiario__icontains=texto) |
            Q(dni_agresor__icontains=texto) |
            Q(expediente__icontains=texto) |
            Q(folder__icontains=texto)
        ).order_by("beneficiario")

    resultados = []

    for caso in casos:

        resultados.append({
            "id": caso.id,
            "beneficiario": caso.beneficiario,
            "agresor": caso.agresor,
            "expediente": caso.expediente,
            "folder": caso.folder,
            "latitud": caso.latitud,
            "longitud": caso.longitud,
            "riesgo": caso.nivel_riesgo,
        })

    return JsonResponse({
        "encontrado": len(resultados) > 0,
        "casos": resultados
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

@login_required
def mapa_agresores(request):

    agresores = Agresor.objects.filter(
        activo=True,
        latitud__isnull=False,
        longitud__isnull=False
    )

    fecha_limite = timezone.now() - timedelta(days=30)

    agresores_preliminares = PersonaPreliminar.objects.filter(
        ubicacion_preliminar__estado="PRELIMINAR",
        latitud__isnull=False,
        longitud__isnull=False,
        roles__rol__in=[
            "DENUNCIADO",
            "PARTICIPANTE"
        ]
    ).distinct()

    return render(
        request,
        "mapa/mapa_agresores.html",
        {
            "agresores": agresores,
            "agresores_preliminares": agresores_preliminares,
        }
    )