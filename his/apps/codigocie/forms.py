from django import forms
from django.forms import fields
from .models import CodigoCie

class CodigocieForms(forms.ModelForm):
    class Meta:
        model = CodigoCie
        fields = '__all__'
        exclude = ['id_codigo']