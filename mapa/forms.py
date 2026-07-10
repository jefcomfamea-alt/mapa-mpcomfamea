from django import forms
from .models import Caso


class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso
        fields = "__all__"

        widgets = {
            "fecha_registro": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
            "ultima_visita": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
            "fecha_limite": forms.DateInput(
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
        self.fields["fecha_limite"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_beneficiario"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["fecha_notificacion_agresor"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]