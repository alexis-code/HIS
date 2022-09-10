from django import forms
from .models import Evolucion

class EvolucionForms(forms.ModelForm):
    class Meta:
        model = Evolucion
        fields = '__all__'
        widgets = {
            'dias_area': forms.NumberInput(attrs={'class':'form-control', 'readonly':'true'}),
            'nro_cama': forms.NumberInput(attrs={'class':'form-control','required':'true'}),
            'diagnostico_evolucion': forms.Textarea(attrs={'class':'form-control','rows':'5','required':'true'}),
            'analisis': forms.Textarea(attrs={'class':'form-control','rows':'5','required':'true'}),
            'plan': forms.Textarea(attrs={'class':'form-control','rows':'5','required':'true'}),
        }
