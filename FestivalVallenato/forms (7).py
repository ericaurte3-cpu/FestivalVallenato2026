"""Formularios de la interfaz de gestión de ediciones (CU-05, RF-02)."""
from django import forms

from .models import Edicion


class EdicionForm(forms.ModelForm):
    class Meta:
        model = Edicion
        fields = ["nombre", "anio", "descripcion", "fecha_inicio", "fecha_fin", "activa"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-check-input" if isinstance(campo.widget, forms.CheckboxInput) else "form-control"
