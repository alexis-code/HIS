from django import forms
from django.db import models
from .models import Indicacion

class FormIndicacion(forms.ModelForm):
    class Meta:
        model = Indicacion
        fields = '__all__'