from django import forms
from django.db import models
from django.forms import fields

from .models import Epicrisis

class FormEmpicrisis(forms.ModelForm):
    class Meta:
        model = Epicrisis
        fields = '__all__'