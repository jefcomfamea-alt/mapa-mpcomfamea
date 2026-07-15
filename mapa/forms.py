from django import forms
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
    "efectivo",
    "folder",
    "expediente",
    "agresor",
    "dni_agresor",
    "telefono",
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
        super().__init__(*args, **kwargs)

        self.fields["fecha_registro"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["ultima_visita"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_beneficiario"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_agresor"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]