from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..paciente.models import Paciente
from ..historiaclinica.models import HistoriaClinica

@login_required
def home(request):
    data = {}
    data['total_pacientes'] = Paciente.objects.filter().count()
    data['total_pacientes_si'] = Paciente.objects.filter(vacuna_covid = "Si").count()
    data['total_pacientes_no'] = Paciente.objects.filter(vacuna_covid = "No").count()
    data['total_pacientes_primera'] = Paciente.objects.filter(vacuna_covid = "Primera dosis").count()
    data['total_pacientes_segunda'] = Paciente.objects.filter(vacuna_covid = "Segunda dosis").count()
    data['total_hc'] = HistoriaClinica.objects.filter().count()
    data['total_hc_activas'] = HistoriaClinica.objects.filter(estado = "Activo").count()
    return render(request,"hospitalapp/base.html",data)

def handler403(request,exception):
    return render(request,'hospitalapp/403.html')
