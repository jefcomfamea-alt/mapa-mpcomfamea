from django import forms
from django.contrib.auth.models import User

from .models import (
    Caso,
    Region,
    Provincia,
    Distrito,
    UbicacionPreliminar,
    PersonaPreliminar,
    RolPersonaPreliminar
)

class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso
        fields = [
            "beneficiario",
            "dni_beneficiario",
            "domicilio",
            "nivel_riesgo",

            "region_denuncia",
            "provincia_denuncia",
            "distrito_denuncia",

            "region_medida",
            "provincia_medida",
            "distrito_medida",

            "comisaria_denuncia",
            "comisaria_medida",

            "responsable",
            "folder",
            "expediente",
            "agresor",
            "dni_agresor",
            "telefono",
            "telefono_agresor",
            "direccion_agresor",
            "estado_ubicacion_agresor",
            "latitud_agresor",
            "longitud_agresor",

            "fecha_denuncia",

            "violencia_fisica",
            "violencia_psicologica",
            "violencia_sexual",
            "violencia_economica",

            "fecha_registro",
            "ultima_visita",
            "notificacion_beneficiario",
            "fecha_notificacion_beneficiario",
            "motivo_notificacion_beneficiario_pendiente",

            "notificacion_agresor",
            "fecha_notificacion_agresor",
            "motivo_notificacion_agresor_pendiente",
            "estado",
            "latitud",
            "longitud",
        ]

        widgets = {

            "fecha_denuncia": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
            
            "fecha_registro": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),

            "ultima_visita": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),

            "fecha_notificacion_beneficiario": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),

            "fecha_notificacion_agresor": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),

            "motivo_notificacion_beneficiario_pendiente": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Indique por qué no se logró la notificación de la persona beneficiaria",
                    "id": "motivo_beneficiario"
                }
            ),

            "motivo_notificacion_agresor_pendiente": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Indique por qué no se logró la notificación de la persona agresora",
                    "id": "motivo_agresor"
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),

            "latitud_agresor": forms.HiddenInput(),

            "longitud_agresor": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):

        self.usuario = kwargs.pop("usuario", None)

        super().__init__(*args, **kwargs)
        self.fields["comisaria_medida"].label = "Comisaría del sector"

                # ==================================
        # UBIGEOS EN CASCADA
        # ==================================

        # Regiones
        self.fields["region_denuncia"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        self.fields["region_medida"].queryset = (
            Region.objects.all().order_by("nombre")
        )

        # Inicialmente no mostrar todas las provincias
        self.fields["provincia_denuncia"].queryset = (
            Provincia.objects.none()
        )

        self.fields["provincia_medida"].queryset = (
            Provincia.objects.none()
        )

        # Inicialmente no mostrar todos los distritos
        self.fields["distrito_denuncia"].queryset = (
            Distrito.objects.none()
        )

        self.fields["distrito_medida"].queryset = (
            Distrito.objects.none()
        )

        # ==================================
        # UBICACIÓN DE LA DENUNCIA
        # ==================================

        if "region_denuncia" in self.data:

            try:

                region_id = int(
                    self.data.get(
                        "region_denuncia"
                    )
                )

                self.fields[
                    "provincia_denuncia"
                ].queryset = (
                    Provincia.objects.filter(
                        region_id=region_id
                    ).order_by("nombre")
                )

            except (
                ValueError,
                TypeError
            ):

                pass

        elif self.instance.pk and (
            self.instance.region_denuncia
        ):

            self.fields[
                "provincia_denuncia"
            ].queryset = (
                Provincia.objects.filter(
                    region=self.instance.region_denuncia
                ).order_by("nombre")
            )

        if "provincia_denuncia" in self.data:

            try:

                provincia_id = int(
                    self.data.get(
                        "provincia_denuncia"
                    )
                )

                self.fields[
                    "distrito_denuncia"
                ].queryset = (
                    Distrito.objects.filter(
                        provincia_id=provincia_id
                    ).order_by("nombre")
                )

            except (
                ValueError,
                TypeError
            ):

                pass

        elif self.instance.pk and (
            self.instance.provincia_denuncia
        ):

            self.fields[
                "distrito_denuncia"
            ].queryset = (
                Distrito.objects.filter(
                    provincia=self.instance.provincia_denuncia
                ).order_by("nombre")
            )

        # ==================================
        # UBICACIÓN DE LA MEDIDA
        # ==================================

        if "region_medida" in self.data:

            try:

                region_id = int(
                    self.data.get(
                        "region_medida"
                    )
                )

                self.fields[
                    "provincia_medida"
                ].queryset = (
                    Provincia.objects.filter(
                        region_id=region_id
                    ).order_by("nombre")
                )

            except (
                ValueError,
                TypeError
            ):

                pass

        elif self.instance.pk and (
            self.instance.region_medida
        ):

            self.fields[
                "provincia_medida"
            ].queryset = (
                Provincia.objects.filter(
                    region=self.instance.region_medida
                ).order_by("nombre")
            )

        if "provincia_medida" in self.data:

            try:

                provincia_id = int(
                    self.data.get(
                        "provincia_medida"
                    )
                )

                self.fields[
                    "distrito_medida"
                ].queryset = (
                    Distrito.objects.filter(
                        provincia_id=provincia_id
                    ).order_by("nombre")
                )

            except (
                ValueError,
                TypeError
            ):

                pass

        elif self.instance.pk and (
            self.instance.provincia_medida
        ):

            self.fields[
                "distrito_medida"
            ].queryset = (
                Distrito.objects.filter(
                    provincia=self.instance.provincia_medida
                ).order_by("nombre")
            )

        self.fields["responsable"].queryset = User.objects.filter(
            groups__name="Usuario_MP",
            is_active=True
        ).order_by("first_name", "last_name", "username")

        self.fields["responsable"].label_from_instance = lambda obj: (
            f"{obj.first_name} {obj.last_name}".strip()
            if obj.first_name or obj.last_name
            else obj.username
        )

        self.fields["responsable"].required = False

        if (
            self.usuario
            and self.usuario.groups.filter(name="Usuario_MP").exists()
        ):
            self.fields.pop("responsable")

        self.fields["fecha_denuncia"].input_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y"
        ]
        self.fields["fecha_registro"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["ultima_visita"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_beneficiario"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_agresor"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]

    def clean(self):

        cleaned_data = super().clean()

        notificacion_beneficiario = cleaned_data.get(
            "notificacion_beneficiario"
        )  

        motivo_beneficiario = cleaned_data.get(
            "motivo_notificacion_beneficiario_pendiente"
        )

        notificacion_agresor = cleaned_data.get(
            "notificacion_agresor"
        )

        motivo_agresor = cleaned_data.get(
            "motivo_notificacion_agresor_pendiente"
        )

        if (
            notificacion_beneficiario == "PENDIENTE"
            and not motivo_beneficiario
        ):
            self.add_error(
                "motivo_notificacion_beneficiario_pendiente",
                "Debe indicar el motivo de la notificación pendiente."
            )

        if (
            notificacion_agresor == "PENDIENTE"
            and not motivo_agresor
        ):
            self.add_error(
            "motivo_notificacion_agresor_pendiente",
                "Debe indicar el motivo de la notificación pendiente."
            )

        return cleaned_data
    
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
                    "class": "form-control"
                }
            ),

            "tipo_intervencion": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),

        }

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
                    "placeholder": "Nombres completos"
                }
            ),

            "dni": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "DNI"
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Teléfono"
                }
            ),

            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección"
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),

            "requiere_ubicacion": forms.CheckboxInput(),

        }


class RolPersonaPreliminarForm(forms.ModelForm):

    class Meta:

        model = RolPersonaPreliminar

        fields = [
            "rol"
        ]

        widgets = {

            "rol": forms.Select(
                attrs={
                    "class": "form-control"
                }
            )

        }