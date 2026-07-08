from django import forms
from .models import Caso


class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso
        fields = "__all__"

        widgets = {
            "fecha_registro": forms.DateInput(
                attrs={"type": "date"}
            ),
            "ultima_visita": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_limite": forms.DateInput(
                attrs={"type": "date"}
            ),
        }