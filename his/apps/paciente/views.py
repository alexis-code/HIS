from django.shortcuts import render
from django.views.generic import ListView
from .models import Paciente
from ..historiaclinica.models import HistoriaClinica
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PacienteList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('paciente.view_paciente')
    model = HistoriaClinica
    template_name = 'indexpaciente.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
