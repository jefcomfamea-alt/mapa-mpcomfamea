from django import forms
from django.contrib.auth.models import User
from .models import Caso


class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso
        fields = [
            "beneficiario",
            "dni_beneficiario",
            "domicilio",
            "nivel_riesgo",
            "distrito",
            "comisaria",
            "responsable",
            "folder",
            "expediente",
            "agresor",
            "dni_agresor",
            "telefono",
            "telefono_agresor",
            "direccion_agresor",
            "fecha_registro",
            "ultima_visita",
            "notificacion_beneficiario",
            "fecha_notificacion_beneficiario",
            "notificacion_agresor",
            "fecha_notificacion_agresor",
            "estado",
            "latitud",
            "longitud",
        ]

        widgets = {
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
            "latitud": forms.HiddenInput(),
            "longitud": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):

        self.usuario = kwargs.pop("usuario", None)

        super().__init__(*args, **kwargs)

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

        self.fields["fecha_registro"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["ultima_visita"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_beneficiario"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_agresor"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]