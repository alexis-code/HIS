from django import forms
from django.forms import fields
from .models import HistoriaClinica

class HistoriCForms(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'
        exclude = ['id_pacienteFK']
