from django import forms
from .models import SolicitudModificacion


class SolicitudModificacionForm(forms.ModelForm):

    class Meta:
        model = SolicitudModificacion
        fields = ["motivo"]

        widgets = {
            "motivo": forms.Textarea(attrs={
                "rows": 5,
                "class": "form-control",
                "placeholder": "Explique por qué necesita modificar el caso..."
            })
        }