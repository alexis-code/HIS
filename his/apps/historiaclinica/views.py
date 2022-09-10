from datetime import date, datetime, time
from django.contrib.auth.decorators import permission_required
from django.http import request, response
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateResponseMixin, View
from ..historiaclinica.models import HistoriaClinica
from .forms import HistoriCForms
from ..paciente.models import Paciente
from ..evolucion.models import Evolucion
from .models import HistoriaClinica
from django.db import transaction
from his.settings import base
from django.urls.base import reverse_lazy
from django.contrib import messages

class IndexHistoriaClinicaActivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('historiaclinica.view_historiaclinica')
    model = HistoriaClinica
    template_name = "historiaapp/index.html"
    paginate_by = 6
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(estado = "Activo")
    
class IndexHistoriaClinicaByCod(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('historiaclinica.view_historiaclinica')
    model = HistoriaClinica
    template_name = "historiaapp/index.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        cod = self.kwargs['cod']
        return self.model.objects.filter(cod_historiaclinica = cod)

class FilterbyFecha(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("historiaclinica.view_historiaclinica")
    model = HistoriaClinica
    template_name = "historiaapp/index.html"

    def get_queryset(self):
        fecha_desde = self.request.GET['fecha_desde']
        fecha_hasta = self.request.GET['fecha_hasta']
        if fecha_desde > fecha_hasta:
            messages.error(self.request,"El rango de fecha es incorrecto!")
        return self.model.objects.filter(estado="Activo",fecha_ingresohospital__range=(fecha_desde,fecha_hasta))

@permission_required("historiaclinica.change_historiaclinica")
def change_status(request):
    id = request.POST.get('pk')
    historiaC = HistoriaClinica.objects.get(id_historiaPK = id)
    if historiaC.estado == 'Activo':
        historiaC.estado = 'Inactivo'
        historiaC.save()
    else:
        historiaC.estado = 'Activo'
        historiaC.save()
    messages.success(request,"Se cambio de estado.")
    return response.HttpResponse({'msg':'Exito!'}) 
    
def redirectToEvolucionCreate(request):
    data = {}
    print("entre")
    try:
        ci = request.POST.get('nro_documento')
        print(ci)
        id_HC = HistoriaClinica.objects.get(id_pacienteFK__nro_documento = ci)
        print("hola" + str(id_HC.id_historiaPK))
        if id_HC.estado == "Inactivo":
            id_HC.estado = "Activo"
            id_HC.save()
        data['id_HC'] = id_HC.id_historiaPK
    except Exception as e:
        print(str(e))
        data['error'] = str(e)
    return JsonResponse(data)

class CreateHistoriaClinica(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ("historiaclinica.add_historiaclinica")
    model = HistoriaClinica
    form_class = HistoriCForms
    template_name = "historiaapp/create.html"
    success_url = reverse_lazy("indexHistoriaC")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        
        if action == 'search_nro_ci':
            try:
                data = []
                for i in Paciente.objects.filter(nro_documento__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nro_documento
                    data.append(item)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data,safe=False)
        if action == "historia_add":
            try:
                with transaction.atomic():
                    paciente = Paciente()
                    paciente.nro_documento = request.POST['nro_documento']
                    paciente.complementario_ci = request.POST['complementario_ci']
                    paciente.nombre = request.POST['nombre']
                    paciente.apellido_paterno = request.POST['apellido_paterno']
                    paciente.apellido_materno = request.POST['apellido_materno']
                    paciente.sexo = request.POST['sexo']
                    paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
                    edad = datetime.now().year - datetime.strptime(paciente.fecha_nacimiento,"%Y-%m-%d").year
                    paciente.edad = edad
                    paciente.ocupacion = request.POST['ocupacion']
                    paciente.estado_civil = request.POST['estado_civil']
                    paciente.residencia = request.POST['residencia']
                    paciente.procedencia = request.POST['procedencia']
                    paciente.domicilio = request.POST['domicilio']
                    paciente.telefono = request.POST['telefono']
                    paciente.nombre_referencia = request.POST['nombre_referencia']
                    paciente.telefono_referencia = request.POST['telefono_referencia']
                    paciente.vacuna_covid = request.POST['vacuna_covid']
                    
                    num_result_hc = HistoriaClinica.objects.filter(cod_historiaclinica = request.POST['cod_historiaclinica']).count()
                    if num_result_hc > 0:
                        messages.error(request,"El código de H.C. "+request.POST['cod_historiaclinica']+" ya se encuentra registrado!")
                    else:
                        paciente.save()
                        historia = HistoriaClinica()
                        historia.cod_historiaclinica = request.POST['cod_historiaclinica']
                        historia.id_pacienteFK_id = paciente.id_pacientePK
                        historia.id_medicoFK_id = request.POST['id_medicoFK']
                        historia.fecha_ingresohospital = request.POST['fecha_ingresohospital']
                        historia.fecha_ingresoarea = request.POST['fecha_ingresoarea']
                        historia.grado_instruccion = request.POST['grado_instruccion']
                        historia.nro_cama = request.POST['nro_cama']
                        historia.proviene = request.POST['proviene']
                        historia.antecedente = request.POST['antecedente']
                        historia.historia_enfermedad_actual = request.POST['historia_enfermedad_actual']
                        historia.tension_arterial = request.POST['tension_arterial']
                        historia.frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
                        historia.temp_ax = request.POST['temp_ax']
                        historia.frecuencia_respiratoria = request.POST['frecuencia_respiratoria']
                        historia.sindrome_at = request.POST['sindrome_at']
                        historia.peso = request.POST['peso']
                        historia.piel_mucosa = request.POST['piel_mucosa']
                        historia.neurologico = request.POST['neurologico']
                        historia.cardiopulmonar = request.POST['cardiopulmonar']
                        historia.abdomen = request.POST['abdomen']
                        historia.genitourinario = request.POST['genitourinario']
                        historia.musculoesqueletico = request.POST['musculoesqueletico']
                        historia.impresion_diagnostica = request.POST['impresion_diagnostica']
                        historia.estado="Activo"
                        historia.save()
                        evolucion = Evolucion()
                        evolucion.id_historiaclinicaFK_id = historia.id_historiaPK
                        evolucion.id_medicoFK_id = historia.id_medicoFK_id
                        evolucion.nro_cama = historia.nro_cama
                        evolucion.fecha_hora = datetime.now()
                        evolucion.save()
                        messages.success(request,"La historia clínica "+historia.cod_historiaclinica+", fue registrada exitosamente!")
            except Exception as e:
                if "tb_paciente" in str(e):
                    messages.error(request,"El nro. de documento " +request.POST["nro_documento"]+", ya se encuentra registrado!")
                elif "tb_historiaclinica" in str(e):
                    messages.error(request,"El código de historia clínica "+request.POST['cod_historiaclinica']+" ya existe!")
                else:
                     messages.error(request, "error: "+str(e)+", contacte con su administrador")
        return HttpResponseRedirect('/historia/index',data)
        
                    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['action'] = "historia_add"
        return context

class UpdateHistoriaClinica(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ("historiaclinica.change_historiaclinica")
    model = HistoriaClinica
    form_class = HistoriCForms
    template_name = 'historiaapp/update.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label_boton'] = 'Confirmar los datos nuevos'
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'search_nro_ci':
            try:
                data = []
                for i in Paciente.objects.filter(nro_documento__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nro_documento
                    data.append(item)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data,safe=False)
        if action == 'historia_edit':
            try:
                with transaction.atomic():
                   
                    paciente = Paciente.objects.get(pk = self.get_object().id_pacienteFK_id)
                    paciente.nombre = request.POST['nombre']
                    paciente.nro_documento = request.POST['nro_documento']
                    paciente.apellido_paterno = request.POST['apellido_paterno']
                    paciente.apellido_materno = request.POST['apellido_materno']
                    paciente.complementario_ci = request.POST['complementario_ci']
                    paciente.sexo = request.POST['sexo']
                    paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
                    edad = datetime.now().year - datetime.strptime(paciente.fecha_nacimiento,"%Y-%m-%d").year
                    paciente.edad = edad
                    paciente.ocupacion = request.POST['ocupacion']
                    paciente.estado_civil = request.POST['estado_civil']
                    paciente.residencia = request.POST['residencia']
                    paciente.procedencia = request.POST['procedencia']
                    paciente.domicilio = request.POST['domicilio']
                    paciente.telefono = request.POST['telefono']
                    paciente.nombre_referencia = request.POST['nombre_referencia']
                    paciente.telefono_referencia = request.POST['telefono_referencia']
                    paciente.vacuna_covid = request.POST['vacuna_covid']
                    paciente.save()
                    historia = self.get_object()
                    historia.cod_historiaclinica = request.POST['cod_historiaclinica']
                    historia.id_pacienteFK_id = paciente.id_pacientePK
                    historia.medico_updated = request.POST['medico_updated']
                    historia.fecha_ingresohospital = request.POST['fecha_ingresohospital']
                    historia.fecha_ingresoarea = request.POST['fecha_ingresoarea']
                    historia.grado_instruccion = request.POST['grado_instruccion']
                    historia.nro_cama = request.POST['nro_cama']
                    historia.proviene = request.POST['proviene']
                    historia.antecedente = request.POST['antecedente']
                    historia.historia_enfermedad_actual = request.POST['historia_enfermedad_actual']
                    historia.tension_arterial = request.POST['tension_arterial']
                    historia.frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
                    historia.temp_ax = request.POST['temp_ax']
                    historia.frecuencia_respiratoria = request.POST['frecuencia_respiratoria']
                    historia.sindrome_at = request.POST['sindrome_at']
                    historia.peso = request.POST['peso']
                    historia.piel_mucosa = request.POST['piel_mucosa']
                    historia.neurologico = request.POST['neurologico']
                    historia.cardiopulmonar = request.POST['cardiopulmonar']
                    historia.abdomen = request.POST['abdomen']
                    historia.genitourinario = request.POST['genitourinario']
                    historia.musculoesqueletico = request.POST['musculoesqueletico']
                    historia.impresion_diagnostica = request.POST['impresion_diagnostica']
                    historia.save()
                    messages.success(request,"La historia clínica " + historia.cod_historiaclinica + ", ha sido actualizada correctamente!")
            except Exception as e:
                if "tb_paciente" in str(e):
                    messages.error(request,"El nro. de documento " +request.POST["nro_documento"]+", ya se encuentra registrado!")
                elif "tb_historiaclinica" in str(e):
                        messages.error(request,"El código de historia clínica "+request.POST['cod_historiaclinica']+" ya existe!")
                else:
                     messages.error(request, "error: "+str(e)+", contacte con su administrador")

        return HttpResponseRedirect('/historia/index',data)

#DetalleHistoria
class DetalleHistoria(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = ("historiaclinica.view_historiaclinica")
    def get(self, request, *args, **kwargs):
        data = {}
        try:
            context = {
                'historia': HistoriaClinica.objects.get(id_historiaPK=self.kwargs['pk']),
                'nro_area':2,
                'logohospital': '{}{}'.format(base.STATIC_URL, 'assets/img/logo-his.png'),
                'logogobernacion': '{}{}'.format(base.STATIC_URL, 'assets/img/logo-gobernacion.png'),
                'direccion': 'Av. San Martin de Porres',
                'ciudad': 'Comarapa - Santa Cruz - Bolivia',
            }
            return render(request,'historiaapp/detalle.html',context)
        except Exception as e:
            data['error']= str(e)
        return response.HttpResponseRedirect(reverse_lazy('indexHistoriaC'))

