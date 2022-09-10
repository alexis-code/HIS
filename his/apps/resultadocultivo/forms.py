from django import forms
from .models import ResultadoCultivo

class ResultadoCultivoForms(forms.ModelForm):
    class Meta:
        model = ResultadoCultivo
        fields = '__all__'