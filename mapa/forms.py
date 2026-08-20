from django import forms
from django.contrib.auth.models import User

from .models import (
    Caso,
    Region,
    Provincia,
    Distrito,
    UbicacionPreliminar,
    PersonaPreliminar,
    RolPersonaPreliminar,
)


# ==========================================================
# CASO
# ==========================================================

class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso

        fields = [
            "beneficiario",
            "dni_beneficiario",
            "domicilio",

            # ==============================
            # DOMICILIO BENEFICIARIA
            # ==============================
            "region_domicilio",
            "provincia_domicilio",
            "distrito_domicilio",
            "tipo_via",
            "nombre_via",
            "numero_via",
            "complemento_domicilio",

            "nivel_riesgo",

            # ==============================
            # UBICACIÓN DE LA DENUNCIA
            # ==============================
            "region_denuncia",
            "provincia_denuncia",
            "distrito_denuncia",

            # ==============================
            # UBICACIÓN DE LA MEDIDA
            # ==============================
            "region_medida",
            "provincia_medida",
            "distrito_medida",

            "comisaria_denuncia",
            "comisaria_medida",

            "responsable",
            "folder",
            "expediente",

            # ==============================
            # AGRESOR
            # ==============================
            "agresor",
            "dni_agresor",
            "telefono_agresor",

            "region_agresor",
            "provincia_agresor",
            "distrito_agresor",

            "tipo_via_agresor",
            "nombre_via_agresor",
            "numero_via_agresor",
            "complemento_domicilio_agresor",
            "direccion_agresor",

            "estado_ubicacion_agresor",
            "latitud_agresor",
            "longitud_agresor",

            # ==============================
            # DENUNCIA
            # ==============================
            "fecha_denuncia",

            "violencia_fisica",
            "violencia_psicologica",
            "violencia_sexual",
            "violencia_economica",

            # ==============================
            # MEDIDA
            # ==============================
            "fecha_registro",
            "ultima_visita",

            # ==============================
            # NOTIFICACIÓN BENEFICIARIO
            # ==============================
            "notificacion_beneficiario",
            "fecha_notificacion_beneficiario",
            "motivo_notificacion_beneficiario_pendiente",

            # ==============================
            # NOTIFICACIÓN AGRESOR
            # ==============================
            "notificacion_agresor",
            "fecha_notificacion_agresor",
            "motivo_notificacion_agresor_pendiente",

            "estado",

            # ==============================
            # COORDENADAS
            # ==============================
            "latitud",
            "longitud",
        ]

        widgets = {

            # ==================================================
            # FECHAS
            # ==================================================

            "fecha_denuncia": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "fecha_registro": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "ultima_visita": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "fecha_notificacion_beneficiario": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "fecha_notificacion_agresor": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            # ==================================================
            # MOTIVOS DE NOTIFICACIÓN
            # ==================================================

            "motivo_notificacion_beneficiario_pendiente": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Indique por qué no se logró la notificación "
                        "de la persona beneficiaria"
                    ),
                    "id": "motivo_beneficiario",
                }
            ),

            "motivo_notificacion_agresor_pendiente": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Indique por qué no se logró la notificación "
                        "de la persona agresora"
                    ),
                    "id": "motivo_agresor",
                }
            ),

            # ==================================================
            # COORDENADAS
            # ==================================================

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),

            "latitud_agresor": forms.HiddenInput(),

            "longitud_agresor": forms.HiddenInput(),

            # ==================================================
            # TIPOS DE VÍA
            # ==================================================

            "tipo_via": forms.Select(
                choices=[
                    ("", "Seleccione tipo de vía"),
                    ("AV.", "Avenida"),
                    ("JR.", "Jirón"),
                    ("CALLE", "Calle"),
                    ("PASAJE", "Pasaje"),
                    ("PROLONGACION", "Prolongación"),
                    ("CARRETERA", "Carretera"),
                    ("AUTOPISTA", "Autopista"),
                    ("MALECON", "Malecón"),
                    ("ALAMEDA", "Alameda"),
                    ("OVALO", "Óvalo"),
                    ("PLAZA", "Plaza"),
                    ("PARQUE", "Parque"),
                    ("CAMINO", "Camino"),
                    ("ASOCIACION", "Asociación"),
                    ("COOPERATIVA", "Cooperativa"),
                    ("URBANIZACION", "Urbanización"),
                    ("OTRO", "Otro"),
                ],
                attrs={
                    "class": "form-control",
                },
            ),

            "tipo_via_agresor": forms.Select(
                choices=[
                    ("", "Seleccione tipo de vía"),
                    ("AV.", "Avenida"),
                    ("JR.", "Jirón"),
                    ("CALLE", "Calle"),
                    ("PASAJE", "Pasaje"),
                    ("PROLONGACION", "Prolongación"),
                    ("CARRETERA", "Carretera"),
                    ("AUTOPISTA", "Autopista"),
                    ("MALECON", "Malecón"),
                    ("ALAMEDA", "Alameda"),
                    ("OVALO", "Óvalo"),
                    ("PLAZA", "Plaza"),
                    ("PARQUE", "Parque"),
                    ("CAMINO", "Camino"),
                    ("ASOCIACION", "Asociación"),
                    ("COOPERATIVA", "Cooperativa"),
                    ("URBANIZACION", "Urbanización"),
                    ("OTRO", "Otro"),
                ],
                attrs={
                    "class": "form-control",
                },
            ),

            # ==================================================
            # DOMICILIO BENEFICIARIA
            # ==================================================

            "nombre_via": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Los Andes",
                }
            ),

            "numero_via": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 125 / Mz. 4 / Lote 8",
                }
            ),

            "complemento_domicilio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Interior, departamento, manzana, lote, "
                        "referencia, etc."
                    ),
                }
            ),

            # ==================================================
            # DOMICILIO AGRESOR
            # ==================================================

            "nombre_via_agresor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Los Andes",
                }
            ),

            "numero_via_agresor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 125 / Mz. 4 / Lote 8",
                }
            ),

            "complemento_domicilio_agresor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Interior, departamento, manzana, lote, "
                        "referencia, etc."
                    ),
                }
            ),
        }

    # ==========================================================
    # INICIALIZACIÓN
    # ==========================================================

    def __init__(self, *args, **kwargs):

        self.usuario = kwargs.pop("usuario", None)

        super().__init__(*args, **kwargs)

        # ==================================================
        # CONFIGURACIÓN GENERAL
        # ==================================================

        self.fields["nivel_riesgo"].required = True

        self.fields["comisaria_medida"].label = (
            "Comisaría del sector"
        )

        self.fields["estado_ubicacion_agresor"].required = False

        self.fields["estado_ubicacion_agresor"].initial = (
            "NO UBICADO"
        )

        # ==================================================
        # REGIONES
        # ==================================================

        self.fields["region_domicilio"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        self.fields["region_denuncia"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        self.fields["region_medida"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        self.fields["region_agresor"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        # ==================================================
        # QUERYSETS INICIALES
        # ==================================================

        self.fields["provincia_domicilio"].queryset = (
            Provincia.objects.none()
        )

        self.fields["distrito_domicilio"].queryset = (
            Distrito.objects.none()
        )

        self.fields["provincia_denuncia"].queryset = (
            Provincia.objects.none()
        )

        self.fields["distrito_denuncia"].queryset = (
            Distrito.objects.none()
        )

        self.fields["provincia_medida"].queryset = (
            Provincia.objects.none()
        )

        self.fields["distrito_medida"].queryset = (
            Distrito.objects.none()
        )

        self.fields["provincia_agresor"].queryset = (
            Provincia.objects.none()
        )

        self.fields["distrito_agresor"].queryset = (
            Distrito.objects.none()
        )

        # ==================================================
        # DOMICILIO BENEFICIARIA
        # ==================================================

        if "region_domicilio" in self.data:

            try:

                region_id = int(
                    self.data.get("region_domicilio")
                )

                self.fields["provincia_domicilio"].queryset = (
                    Provincia.objects
                    .filter(region_id=region_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.region_domicilio
        ):

            self.fields["provincia_domicilio"].queryset = (
                Provincia.objects
                .filter(
                    region=self.instance.region_domicilio
                )
                .order_by("nombre")
            )

        if "provincia_domicilio" in self.data:

            try:

                provincia_id = int(
                    self.data.get("provincia_domicilio")
                )

                self.fields["distrito_domicilio"].queryset = (
                    Distrito.objects
                    .filter(provincia_id=provincia_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.provincia_domicilio
        ):

            self.fields["distrito_domicilio"].queryset = (
                Distrito.objects
                .filter(
                    provincia=self.instance.provincia_domicilio
                )
                .order_by("nombre")
            )

        # ==================================================
        # DOMICILIO AGRESOR
        # ==================================================

        if "region_agresor" in self.data:

            try:

                region_id = int(
                    self.data.get("region_agresor")
                )

                self.fields["provincia_agresor"].queryset = (
                    Provincia.objects
                    .filter(region_id=region_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.region_agresor
        ):

            self.fields["provincia_agresor"].queryset = (
                Provincia.objects
                .filter(
                    region=self.instance.region_agresor
                )
                .order_by("nombre")
            )

        if "provincia_agresor" in self.data:

            try:

                provincia_id = int(
                    self.data.get("provincia_agresor")
                )

                self.fields["distrito_agresor"].queryset = (
                    Distrito.objects
                    .filter(provincia_id=provincia_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.provincia_agresor
        ):

            self.fields["distrito_agresor"].queryset = (
                Distrito.objects
                .filter(
                    provincia=self.instance.provincia_agresor
                )
                .order_by("nombre")
            )

        # ==================================================
        # UBICACIÓN DENUNCIA
        # ==================================================

        if "region_denuncia" in self.data:

            try:

                region_id = int(
                    self.data.get("region_denuncia")
                )

                self.fields["provincia_denuncia"].queryset = (
                    Provincia.objects
                    .filter(region_id=region_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.region_denuncia
        ):

            self.fields["provincia_denuncia"].queryset = (
                Provincia.objects
                .filter(
                    region=self.instance.region_denuncia
                )
                .order_by("nombre")
            )

        if "provincia_denuncia" in self.data:

            try:

                provincia_id = int(
                    self.data.get("provincia_denuncia")
                )

                self.fields["distrito_denuncia"].queryset = (
                    Distrito.objects
                    .filter(provincia_id=provincia_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.provincia_denuncia
        ):

            self.fields["distrito_denuncia"].queryset = (
                Distrito.objects
                .filter(
                    provincia=self.instance.provincia_denuncia
                )
                .order_by("nombre")
            )

        # ==================================================
        # UBICACIÓN MEDIDA
        # ==================================================

        if "region_medida" in self.data:

            try:

                region_id = int(
                    self.data.get("region_medida")
                )

                self.fields["provincia_medida"].queryset = (
                    Provincia.objects
                    .filter(region_id=region_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.region_medida
        ):

            self.fields["provincia_medida"].queryset = (
                Provincia.objects
                .filter(
                    region=self.instance.region_medida
                )
                .order_by("nombre")
            )

        if "provincia_medida" in self.data:

            try:

                provincia_id = int(
                    self.data.get("provincia_medida")
                )

                self.fields["distrito_medida"].queryset = (
                    Distrito.objects
                    .filter(provincia_id=provincia_id)
                    .order_by("nombre")
                )

            except (ValueError, TypeError):
                pass

        elif (
            self.instance.pk
            and self.instance.provincia_medida
        ):

            self.fields["distrito_medida"].queryset = (
                Distrito.objects
                .filter(
                    provincia=self.instance.provincia_medida
                )
                .order_by("nombre")
            )

        # ==================================================
        # RESPONSABLE
        # ==================================================

        self.fields["responsable"].queryset = (
            User.objects
            .filter(
                groups__name="Usuario_MP",
                is_active=True
            )
            .order_by(
                "first_name",
                "last_name",
                "username"
            )
        )

        self.fields["responsable"].label_from_instance = (
            lambda obj: (
                f"{obj.first_name} {obj.last_name}".strip()
                if obj.first_name or obj.last_name
                else obj.username
            )
        )

        self.fields["responsable"].required = False

        if (
            self.usuario
            and self.usuario.groups.filter(
                name="Usuario_MP"
            ).exists()
        ):

            self.fields.pop("responsable")

        # ==================================================
        # FORMATOS DE FECHA
        # ==================================================

        self.fields["fecha_denuncia"].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]

        self.fields["fecha_registro"].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]

        self.fields["ultima_visita"].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]

        self.fields[
            "fecha_notificacion_beneficiario"
        ].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]

        self.fields[
            "fecha_notificacion_agresor"
        ].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]

    # ==========================================================
    # VALIDACIÓN
    # ==========================================================

    def clean(self):

        cleaned_data = super().clean()

        # ==================================================
        # NIVEL DE RIESGO
        # ==================================================

        nivel_riesgo = cleaned_data.get("nivel_riesgo")

        if not nivel_riesgo:

            self.add_error(
                "nivel_riesgo",
                "Debe seleccionar un nivel de riesgo."
            )

        # ==================================================
        # NOTIFICACIÓN BENEFICIARIO
        # ==================================================

        notificacion_beneficiario = cleaned_data.get(
            "notificacion_beneficiario"
        )

        motivo_beneficiario = cleaned_data.get(
            "motivo_notificacion_beneficiario_pendiente"
        )

        if (
            notificacion_beneficiario == "PENDIENTE"
            and not motivo_beneficiario
        ):

            self.add_error(
                "motivo_notificacion_beneficiario_pendiente",
                "Debe indicar el motivo de la notificación pendiente."
            )

        # ==================================================
        # NOTIFICACIÓN AGRESOR
        # ==================================================

        notificacion_agresor = cleaned_data.get(
            "notificacion_agresor"
        )

        motivo_agresor = cleaned_data.get(
            "motivo_notificacion_agresor_pendiente"
        )

        if (
            notificacion_agresor == "PENDIENTE"
            and not motivo_agresor
        ):

            self.add_error(
                "motivo_notificacion_agresor_pendiente",
                "Debe indicar el motivo de la notificación pendiente."
            )

        # ==================================================
        # AGRESOR SIN UBICACIÓN
        # ==================================================

        if not cleaned_data.get("estado_ubicacion_agresor"):

            cleaned_data["estado_ubicacion_agresor"] = (
                "NO UBICADO"
            )

        return cleaned_data


# ==========================================================
# UBICACIÓN PRELIMINAR
# ==========================================================

class UbicacionPreliminarForm(forms.ModelForm):

    class Meta:

        model = UbicacionPreliminar

        fields = [
            "tipo_registro",
            "tipo_intervencion",
            "latitud",
            "longitud",
        ]

        widgets = {

            "tipo_registro": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "tipo_intervencion": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),
        }


# ==========================================================
# PERSONA PRELIMINAR
# ==========================================================

class PersonaPreliminarForm(forms.ModelForm):

    class Meta:

        model = PersonaPreliminar

        fields = [
            "nombres",
            "dni",
            "telefono",
            "direccion",
            "latitud",
            "longitud",
            "requiere_ubicacion",
        ]

        widgets = {

            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres completos",
                }
            ),

            "dni": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "DNI",
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Teléfono",
                }
            ),

            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección",
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),

            "requiere_ubicacion": forms.CheckboxInput(),
        }


# ==========================================================
# ROL PERSONA PRELIMINAR
# ==========================================================

class RolPersonaPreliminarForm(forms.ModelForm):

    class Meta:

        model = RolPersonaPreliminar

        fields = [
            "rol",
        ]

        widgets = {

            "rol": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }