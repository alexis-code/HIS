from django import forms
from django.forms import fields
from .models import Medicamento

class MedicamentoForms(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        exclude = ['id_medicamentoPK']