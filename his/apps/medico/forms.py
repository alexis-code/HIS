from django.db.models.base import Model
from django import forms
from .models import Medico
from django.contrib.auth.forms import AuthenticationForm

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class FormCreateMedico(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'