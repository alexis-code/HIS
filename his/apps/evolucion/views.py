from django.forms.models import model_to_dict
from django.http import response, JsonResponse
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from datetime import date, datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from .forms import EvolucionForms
from ..resultadocultivo.forms import ResultadoCultivoForms
from django.views.generic import ListView, DetailView, View
from ..historiaclinica.models import HistoriaClinica
from .models import Evolucion, det_cultivo_evolucion, det_tratmiento_evolucion
from ..cultivo.models import Cultivo
from ..medicamento.models import Medicamento
from ..examenfisico.models import ExamenFisico
from ..resultadolaboratorio.models import ResultadoLab
from ..resultadocultivo.models import ResultadoCultivo
import json
#import django_excel as excel

#Lista de las evoluciones pertenecientes a una historia clinica (fk)
class EvolucionListFilterbyHC(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("evolucion.view_evolucion")
    model = Evolucion
    template_name = 'evolucionapp/index.html'
    paginate_by = 6

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_historiaclinicaFK = fk, estado = 'Activo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_historia'] = self.kwargs['fk']
        evolucionU = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('-id_evolucionPK')[0]
        context['id_evolucionU'] = evolucionU.id_evolucionPK
        evolucionP = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('id_evolucionPK')[0]
        context['id_evolucionP'] = evolucionP.id_evolucionPK
        return context

class EvolucionListbyFecha(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("evolucion.view_evolucion")
    model = Evolucion
    template_name = 'evolucionapp/index.html'

    def get_queryset(self):
        fecha_desde = self.request.GET['fecha_desde']
        fecha_hasta = self.request.GET['fecha_hasta']
        if fecha_desde > fecha_hasta:
            messages.error(self.request,"El rango de fecha es incorrecto!")
        fecha_desde = fecha_desde + " 00:00:00"
        fecha_hasta = fecha_hasta + " 23:59:59"
        cod_hc = self.request.GET['cod_hc']
        return self.model.objects.filter(id_historiaclinicaFK = cod_hc, estado = "Activo",fecha_hora__range = (fecha_desde,fecha_hasta))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_historia'] = self.request.GET['cod_hc']
        evolucionU = Evolucion.objects.filter(id_historiaclinicaFK = self.request.GET['cod_hc']).order_by('-id_evolucionPK')[0]
        context['id_evolucionU'] = evolucionU.id_evolucionPK
        evolucionP = Evolucion.objects.filter(id_historiaclinicaFK = self.request.GET['cod_hc']).order_by('id_evolucionPK')[0]
        context['id_evolucionP'] = evolucionP.id_evolucionPK
        return context

class EvolucionListFilterbyHCActivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("evolucion.view_evolucion")
    model = Evolucion
    template_name = 'evolucionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_historiaclinicaFK = fk, estado = 'Activo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_historia'] = self.kwargs['fk']
        evolucionU = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('-id_evolucionPK')[0]
        context['id_evolucionU'] = evolucionU.id_evolucionPK
        evolucionP = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('id_evolucionPK')[0]
        context['id_evolucionP'] = evolucionP.id_evolucionPK
        context['id'] = self.kwargs['fk']
        return context

class EvolucionListFilterbyHCAnulado(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("evolucion.view_evolucion")
    model = Evolucion
    template_name = 'evolucionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_historiaclinicaFK = fk, estado = 'Anulado')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_historia'] = self.kwargs['fk']
        evolucionU = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('-id_evolucionPK')[0]
        context['id_evolucionU'] = evolucionU.id_evolucionPK
        evolucionP = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('id_evolucionPK')[0]
        context['id_evolucionP'] = evolucionP.id_evolucionPK
        context['id'] = self.kwargs['fk']
        return context

class EvolucionListFilterbyHCAll(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("evolucion.view_evolucion")
    model = Evolucion
    template_name = 'evolucionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_historiaclinicaFK = fk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_historia'] = self.kwargs['fk']
        evolucionU = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('-id_evolucionPK')[0]
        context['id_evolucionU'] = evolucionU.id_evolucionPK
        evolucionP = Evolucion.objects.filter(id_historiaclinicaFK = self.kwargs['fk']).order_by('id_evolucionPK')[0]
        context['id_evolucionP'] = evolucionP.id_evolucionPK
        context['id'] = self.kwargs['fk']
        return context


@login_required
@permission_required("evolucion.change_evolucion")
def change_status(request):
    pk = request.POST.get('pk')
    evolucion = Evolucion.objects.get(id_evolucionPK=pk)
    if evolucion.estado == 'Activo':
        evolucion.estado = 'Anulado'
        evolucion.save()
    else:
        evolucion.estado = 'Activo'
        evolucion.save()
    id = evolucion.id_historiaclinicaFK_id
    data = id
    messages.success(request,"Se cambio de estado.")
    return response.HttpResponse(data)



#Crear Nueva Evolucion asociada a una historia clinica (fk)
class EvolucionDetailCreate(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required=("evolucion.add_evolucion")
    model = Evolucion
    form_class = EvolucionForms
    template_name = 'evolucionapp/create.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(HistoriaClinica, id_historiaPK=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk = self.kwargs['id']
        historiaclinica = HistoriaClinica.objects.get(id_historiaPK = fk)
        fecha_ingreso = historiaclinica.fecha_ingresoarea
        fecha_actual = datetime.now()
        resultado = (fecha_actual - fecha_ingreso).days
        context['diasArea'] = resultado
        context['label_button'] = "Registrar Evolución"
        return context
        
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "search_medicamentos":
                data = []
                for i in Medicamento.objects.filter(nombre__icontains=request.POST['term'], estado="Activo"):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "search_cultivos":
                data = []
                for i in Cultivo.objects.filter(nombre__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "evolucion_add":
                try:
                    with transaction.atomic():
                        
                        cultivo_list = json.loads(request.POST['cultivos_list'])
                        medicamento_list = json.loads(request.POST['medicamento_list'])

                        examenfisico = ExamenFisico()
                        examenfisico.tension_arterial = request.POST['tension_arterial']
                        examenfisico.frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
                        examenfisico.frecuencia_respiratoria = request.POST['frecuencia_respiratoria']
                        examenfisico.temp_ax = request.POST['temp_ax']
                        examenfisico.sindrome_at = request.POST['sindrome_at']
                        examenfisico.fio = request.POST['fio']
                        examenfisico.pao = request.POST['pao']
                        examenfisico.pas = request.POST['pas']
                        examenfisico.pad = request.POST['pad']
                        if float(examenfisico.pas) != 0.00 and float(examenfisico.pad) != 0.00:
                            pam_resultado = round((float(examenfisico.pas) + float(examenfisico.pad)*2)/3,2)
                            print(pam_resultado)
                            examenfisico.pam = pam_resultado
                        else:
                            examenfisico.pam = 0.00
                        examenfisico.avm = request.POST['avm']
                        examenfisico.modo = request.POST['modo']
                        examenfisico.pao = request.POST['pao']
                        examenfisico.noradrenalina = request.POST['noradrenalina']
                        examenfisico.atracurio = request.POST['atracurio']
                        examenfisico.vc = request.POST['vc']
                        examenfisico.peep = request.POST['peep']
                        examenfisico.prono_dias = request.POST['prono_dias']
                        if float(examenfisico.pao) != 0.00 and float(examenfisico.fio) != 0.00:
                            pao_fio = round(float(examenfisico.pao)/(float(examenfisico.fio)/100),2)
                            examenfisico.pao_fio = pao_fio
                        else:
                            examenfisico.pao_fio = 0.00
                        examenfisico.pi = request.POST['pi']
                        examenfisico.peso = request.POST['peso']
                        examenfisico.piel_mucosa = request.POST['piel_mucosa']
                        examenfisico.neurologico = request.POST['neurologico']
                        examenfisico.cardiopulmonar = request.POST['cardiopulmonar']
                        examenfisico.abdomen = request.POST['abdomen']
                        examenfisico.genitourinario = request.POST['genitourinario']
                        examenfisico.musculoesqueletico = request.POST['musculoesqueletico']
                        examenfisico.save()

                        laboratorio = ResultadoLab()
                        laboratorio.lab_gb = request.POST['lab_gb']
                        laboratorio.lab_hb = request.POST['lab_hb']
                        laboratorio.lab_ph = request.POST['lab_ph']
                        laboratorio.lab_got = request.POST['lab_got']
                        laboratorio.lab_neu = request.POST['lab_neu']
                        laboratorio.lab_htco = request.POST['lab_htco']
                        laboratorio.lab_pco = request.POST['lab_pco']
                        laboratorio.lab_gpt = request.POST['lab_gpt']
                        laboratorio.lab_lin = request.POST['lab_lin']
                        laboratorio.lab_cr = request.POST['lab_cr']
                        laboratorio.lab_hco = request.POST['lab_hco']
                        laboratorio.lab_pt = request.POST['lab_pt']
                        laboratorio.lab_cay = request.POST['lab_cay']
                        laboratorio.lab_urea = request.POST['lab_urea']
                        laboratorio.lab_alb = request.POST['lab_alb']
                        laboratorio.lab_po = request.POST['lab_po']
                        laboratorio.lab_plq = request.POST['lab_plq']
                        laboratorio.lab_na = request.POST['lab_na']
                        laboratorio.lab_eb = request.POST['lab_eb']
                        laboratorio.lab_cl = request.POST['lab_cl']
                        laboratorio.lab_k = request.POST['lab_k']
                        laboratorio.lab_lact = request.POST['lab_lact']
                        laboratorio.lab_dd = request.POST['lab_dd']
                        laboratorio.save()

                        evolucion = Evolucion()
                        evolucion.id_historiaclinicaFK_id = request.POST['id_historiaclinicaFK']
                        evolucion.id_medicoFK_id = request.POST['id_medicoPK']
                        evolucion.id_examenfisicoFK_id = examenfisico.id_examenfisicoPK
                        evolucion.id_resultadolabFK_id = laboratorio.id_resultadolabPK
                        evolucion.fecha_hora = datetime.now()
                        evolucion.nro_cama = request.POST['nro_cama']
                        evolucion.dias_area = request.POST['dias_area']
                        evolucion.diagnostico_evolucion = request.POST['diagnostico_evolucion']
                        evolucion.analisis = request.POST['analisis']
                        evolucion.plan = request.POST['plan']
                        evolucion.save()

                        historia = HistoriaClinica.objects.get(id_historiaPK = evolucion.id_historiaclinicaFK_id)
                        if historia.estado == "Inactivo":
                            historia.estado = "Activo"
                            historia.save()

                        for i in cultivo_list['cultivos']:
                            cultivo = Cultivo()
                            cultivo.nombre = i['nombre']
                            cultivo.save()

                            det = det_cultivo_evolucion()
                            det.id_cultivoFK_id = cultivo.id_cultivoPK
                            det.id_evolucionFK_id = evolucion.id_evolucionPK
                            det.fecha = i['fecha']
                            det.estado = "En curso"
                            det.save()

                        for i in medicamento_list['tratamiento']:
                            det_tratamiento = det_tratmiento_evolucion()
                            det_tratamiento.id_evolucionFK_id = evolucion.id_evolucionPK
                            det_tratamiento.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_tratamiento.cantidad = i['cant']
                            det_tratamiento.indicacion = i['indicacion']
                            det_tratamiento.save()
                        data = {'id':evolucion.id_historiaclinicaFK_id}
                        messages.success(request,"Se registro una evolución correctamente!")
                except Exception as e:
                    messages.error(request,"Ha ocurrido un error: " + str(e) + ", contacte a su administrador del sistema.")
        except Exception as e:
            messages.error(request,"Ha ocurrido un error: " + str(e) + ", contacte a su administrador del sistema.")
        return JsonResponse(data,safe=False)


#Edita la evolucion seleccionada
class EvolucionUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required=("evolucion.change_evolucion")
    model = Evolucion
    form_class = EvolucionForms
    template_name = 'evolucionapp/update.html'

    fecha_cultivo = ""
    

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "search_medicamentos":
                data = []
                for i in Medicamento.objects.filter(nombre__icontains=request.POST['term'],estado="Activo"):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "search_cultivos":
                data = []
                for i in Cultivo.objects.filter(nombre__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "evolucion_edit":
                try:
                    with transaction.atomic():
                        
                        cultivo_list = json.loads(request.POST['cultivos_list'])
                        medicamento_list = json.loads(request.POST['medicamento_list'])

                        examenfisico = ExamenFisico.objects.get(pk = self.get_object().id_examenfisicoFK_id)
                        examenfisico.tension_arterial = request.POST['tension_arterial']
                        examenfisico.frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
                        examenfisico.frecuencia_respiratoria = request.POST['frecuencia_respiratoria']
                        examenfisico.temp_ax = request.POST['temp_ax']
                        examenfisico.sindrome_at = request.POST['sindrome_at']
                        examenfisico.fio = request.POST['fio']
                        examenfisico.pao = request.POST['pao']
                        examenfisico.pas = request.POST['pas']
                        examenfisico.pad = request.POST['pad']
                        if float(examenfisico.pas) != 0.00 and float(examenfisico.pad) != 0.00:
                            pam_resultado = round((float(examenfisico.pas) + float(examenfisico.pad)*2)/3,2)
                            examenfisico.pam = pam_resultado
                        else:
                            examenfisico.pam = 0.00
                        examenfisico.avm = request.POST['avm']
                        examenfisico.modo = request.POST['modo']
                        examenfisico.noradrenalina = request.POST['noradrenalina']
                        examenfisico.atracurio = request.POST['atracurio']
                        examenfisico.vc = request.POST['vc']
                        examenfisico.peep = request.POST['peep']
                        examenfisico.prono_dias = request.POST['prono_dias']
                        if float(examenfisico.pao) != 0.00 and float(examenfisico.fio) != 0.00:
                            pao_fio = round(float(examenfisico.pao)/(float(examenfisico.fio)/100),2)
                            examenfisico.pao_fio = pao_fio
                        else:
                            examenfisico.pao_fio = 0.00
                        examenfisico.pi = request.POST['pi']
                        examenfisico.peso = request.POST['peso']
                        examenfisico.piel_mucosa = request.POST['piel_mucosa']
                        examenfisico.neurologico = request.POST['neurologico']
                        examenfisico.cardiopulmonar = request.POST['cardiopulmonar']
                        examenfisico.abdomen = request.POST['abdomen']
                        examenfisico.genitourinario = request.POST['genitourinario']
                        examenfisico.musculoesqueletico = request.POST['musculoesqueletico']
                        examenfisico.save()

                        laboratorio = ResultadoLab.objects.get(pk = self.get_object().id_resultadolabFK_id)
                        laboratorio.lab_gb = request.POST['lab_gb']
                        laboratorio.lab_hb = request.POST['lab_hb']
                        laboratorio.lab_ph = request.POST['lab_ph']
                        laboratorio.lab_got = request.POST['lab_got']
                        laboratorio.lab_neu = request.POST['lab_neu']
                        laboratorio.lab_htco = request.POST['lab_htco']
                        laboratorio.lab_pco = request.POST['lab_pco']
                        laboratorio.lab_gpt = request.POST['lab_gpt']
                        laboratorio.lab_lin = request.POST['lab_lin']
                        laboratorio.lab_cr = request.POST['lab_cr']
                        laboratorio.lab_hco = request.POST['lab_hco']
                        laboratorio.lab_pt = request.POST['lab_pt']
                        laboratorio.lab_cay = request.POST['lab_cay']
                        laboratorio.lab_urea = request.POST['lab_urea']
                        laboratorio.lab_alb = request.POST['lab_alb']
                        laboratorio.lab_po = request.POST['lab_po']
                        laboratorio.lab_plq = request.POST['lab_plq']
                        laboratorio.lab_na = request.POST['lab_na']
                        laboratorio.lab_eb = request.POST['lab_eb']
                        laboratorio.lab_cl = request.POST['lab_cl']
                        laboratorio.lab_k = request.POST['lab_k']
                        laboratorio.lab_lact = request.POST['lab_lact']
                        laboratorio.lab_dd = request.POST['lab_dd']
                        laboratorio.save()

                        evolucion = self.get_object()
                        evolucion.id_historiaclinicaFK_id = request.POST['id_historiaclinicaFK']
                        evolucion.medico_updated = request.POST['medico_updated']
                        evolucion.id_examenfisicoFK_id = examenfisico.id_examenfisicoPK
                        evolucion.id_resultadolabFK_id = laboratorio.id_resultadolabPK
                        evolucion.nro_cama = request.POST['nro_cama']
                        evolucion.dias_area = request.POST['dias_area']
                        evolucion.diagnostico_evolucion = request.POST['diagnostico_evolucion']
                        evolucion.analisis = request.POST['analisis']
                        evolucion.plan = request.POST['plan']
                        evolucion.save()

                        evolucion.det_cultivo_evolucion_set.all().delete()
                        for i in cultivo_list['cultivos']:
                            if i['id_cultivoPK'] == '':
                                cultivo = Cultivo()
                                cultivo.nombre = i['nombre']
                                cultivo.save()
                                det = det_cultivo_evolucion()
                                det.id_cultivoFK_id = cultivo.id_cultivoPK
                                det.id_evolucionFK_id = evolucion.id_evolucionPK
                                det.fecha = i['fecha']
                                det.estado = i['estado']
                                det.save()
                            elif i['id_cultivoPK'] != '':
                                det = det_cultivo_evolucion()
                                det.id_cultivoFK_id = i['id_cultivoPK']
                                det.id_evolucionFK_id = evolucion.id_evolucionPK
                                det.fecha = i['fecha']
                                det.estado = i['estado']
                                det.save()

                        evolucion.det_tratmiento_evolucion_set.all().delete()
                        for i in medicamento_list['tratamiento']:
                            det_tratamiento = det_tratmiento_evolucion()
                            det_tratamiento.id_evolucionFK_id = evolucion.id_evolucionPK
                            det_tratamiento.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_tratamiento.cantidad = i['cant']
                            det_tratamiento.indicacion = i['indicacion']
                            det_tratamiento.save()
                        data = {'id':evolucion.id_historiaclinicaFK_id}
                        messages.success(request,"La evolución se edito correctamente!")
                except Exception as e:
                    messages.error(request,"Ha ocurrido un error: " + str(e) + ", contacte a su administrador del sistema.")
            if action == "add_resultcultivo":
                try:
                    resultado = ResultadoCultivo()
                    resultado.id_cultivoFK_id = request.POST['id_cultivoFK']
                    resultado.id_evolucionFK_id = request.POST['id_evolucionFK']
                    if request.POST['resultado_probable'] == '1':
                        resultado.resultado_probable = "No se aislo ningun patogeno"
                    elif request.POST['resultado_probable'] == '2':
                        resultado.resultado_probable = "Se asilo patogeno"
                    resultado.patogeno = request.POST['patogeno']
                    resultado.sensible = request.POST['sensible']
                    resultado.resistente = request.POST['resistente']
                    resultado.parcial_sensible = request.POST['parcial_sensible']
                    resultado.comentario = request.POST['comentario']
                    resultado.medico = request.POST['medico']
                    resultado.estado = 'Activo'
                    resultado.save()

                    cultivo = det_cultivo_evolucion.objects.get(id_cultivoFK_id = resultado.id_cultivoFK_id)
                    cultivo.estado = "Registrado"
                    cultivo.save()
                    id_cultivo = resultado.id_cultivoFK_id
                    estado = cultivo.estado
                    data = {
                        'id_cultivo':id_cultivo,
                        'estado':estado
                    }
                except Exception as e:
                    messages.error(request,"Ha ocurrido un error: " + str(e) + ", contacte a su administrador del sistema.")
        except Exception as e:
            messages.error(request,"Ha ocurrido un error: " + str(e) + ", contacte a su administrador del sistema.")
        return JsonResponse(data,safe=False)

    def get_detail_cultivo(self):
        data = []
        try:
            for i in det_cultivo_evolucion.objects.filter(id_evolucionFK_id=self.get_object().id_evolucionPK):
                item = i.id_cultivoFK.toJSON()
                item['id_evolucionFK'] = i.id_evolucionFK_id
                item['fecha'] = str(i.fecha.strftime('%Y-%m-%d'))
                item['estado'] = i.estado
                data.append(item)
        except Exception as e:
            print(str(e))
        return data

    def get_detail_tratamiento(self):
        data = []
        try:
            for i in det_tratmiento_evolucion.objects.filter(id_evolucionFK_id=self.get_object().id_evolucionPK):
                item = i.id_medicamentoFK.toJSON()
                item['cant'] = i.cantidad
                item['indicacion'] = i.indicacion
                data.append(item)
        except Exception as e:
            print(str(e))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['det_cultivo'] = json.dumps(self.get_detail_cultivo())
        context['det_tratamiento'] = json.dumps(self.get_detail_tratamiento())
        context['label_button'] = "Confirmar Nuevos Datos"
        return context


class DetalleEvolucion(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required=("evolucion.view_evolucion")
    def get(self, request, *args, **kwargs):
        try:
            context = {
                'evolucion':Evolucion.objects.get(id_evolucionPK=self.kwargs['pk']),
                'nro_area': 2,
                'direccion': 'Av. San Martin de Porres',
                'ciudad': 'Comarapa - Santa Cruz - Bolivia',
            }
            return render(request,'evolucionapp/detalle.html',context)
        except Exception as e:
            print(str(e))
        return response.HttpResponseRedirect(reverse_lazy('indexHistoriaC'))

class CultivoSolicitadoListEnCurso(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("cultivo.view_cultivo")
    model = det_cultivo_evolucion
    template_name = 'evolucionapp/indexCultivo.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK=fk, estado="En Curso")
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       id = self.kwargs['fk']
       context['id'] = id
       return context

class CultivoSolicitadoListRegistrado(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("cultivo.view_cultivo")
    model = det_cultivo_evolucion
    template_name = 'evolucionapp/indexCultivo.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK=fk, estado="Registrado")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['fk']
        context['id'] = id
        return context

def registrar_result_cultivo(request):
    try:
        resultado = ResultadoCultivo()
        resultado.id_cultivoFK_id = request.POST['id_cultivoFK']
        resultado.id_evolucionFK_id = request.POST['id_evolucionFK']
        if request.POST['resultado_probable'] == '1':
            resultado.resultado_probable = "No se aislo ningun patogeno"
        elif request.POST['resultado_probable'] == '2':
            resultado.resultado_probable = "Se asilo patogeno"
        resultado.patogeno = request.POST['patogeno']
        resultado.sensible = request.POST['sensible']
        resultado.resistente = request.POST['resistente']
        resultado.parcial_sensible = request.POST['parcial_sensible']
        resultado.comentario = request.POST['comentario']
        resultado.medico = request.POST['medico']
        resultado.estado = 'Activo'
        print(resultado.comentario)
        resultado.save()

        cultivo = det_cultivo_evolucion.objects.get(id_cultivoFK_id = resultado.id_cultivoFK_id)
        cultivo.estado = "Registrado"
        cultivo.save()
        id_cultivo = resultado.id_cultivoFK_id
        estado = cultivo.estado
        data = {
            'id_cultivo':id_cultivo,
            'estado':estado
        }
        messages.success(request,"Los resultados fueron registrados exitosamente!")
    except Exception as e:
        messages.error(request,"error:"+str(e))
    return JsonResponse(data,safe=False)


class ResultadoCultivoList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("resultadocultivo.view_resultadocultivo")
    model = ResultadoCultivo
    template_name = 'resultadocultapp/index.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK = fk,estado = 'Activo')

class DetalleResultCultivo(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required=("resultadocultivo.view_resultadocultivo")
    model = ResultadoCultivo
    template_name = 'resultadocultapp/detalle.html'
    
class UpdateResultCultivo(UpdateView,PermissionRequiredMixin,LoginRequiredMixin):
    permission_required=("resultado.change.resultadocultivo")
    model = ResultadoCultivo
    form_class = ResultadoCultivoForms
    template_name = 'resultadocultapp/update.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['label_boton'] = 'Confirmar Nuevos Datos'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit_resultCultivo':
                result_cultivo = ResultadoCultivo.objects.get(pk = self.get_object().id_resultCultivoPK)
                result_cultivo.medico_updated = request.POST['medico_updatedC']
                if request.POST['resultado_probable'] == '1':
                        result_cultivo.resultado_probable = "No se aislo ningun patogeno"
                elif request.POST['resultado_probable'] == '2':
                    result_cultivo.resultado_probable = "Se asilo patogeno" 
                result_cultivo.patogeno = request.POST['patogeno'] 
                result_cultivo.sensible = request.POST['sensible'] 
                result_cultivo.resistente = request.POST['resistente'] 
                result_cultivo.parcial_sensible = request.POST['parcial_sensible'] 
                result_cultivo.comentario = request.POST['comentario']
                result_cultivo.save()
        except Exception as e:
            data['error'] = str(e)
        return redirect('/evolucion/cultivo/resultados/'+ request.POST['id_evolucionFK'])

@login_required
@permission_required("resultadocultivo.change_resultadocultivo")
def change_status_cultivo(request):
    data = {}
    try:
        pk = request.POST.get('pk')
        resultCultivo = ResultadoCultivo.objects.get(id_resultCultivoPK=pk)
        if resultCultivo.estado == 'Activo':
            resultCultivo.estado = 'Anulado'
            resultCultivo.save()
        else:
            resultCultivo.estado = 'Activo'
            resultCultivo.save()
        messages.success(request,"Se cambio de estado.")
        return JsonResponse(data)
    except Exception as e:
        data = str(e)
    return JsonResponse(data)

@login_required
@csrf_exempt
def generar_estadistica_fisico(request):
    fecha_desde = request.POST['fecha_desde']
    fecha_hasta = request.POST['fecha_hasta']
    if fecha_desde > fecha_hasta:
        messages.error(request,"El rango de fecha solicitado es incorrecto!")
    pk = request.POST['pk']
    data = {}
    datos_fc = []
    datos_fr = []
    datos_tempax = []
    datos_sat = []
    datos_pao = []
    datos_fio = []
    datos_paofio = []
    datos_pas = []
    datos_pad = []
    datos_pam = []
    datos_avm = []
    datos_modo = []
    datos_vc = []
    datos_peep = []
    datos_pi = []
    datos_peso = []
    dias = []
    try:
        for exam in Evolucion.objects.filter(id_historiaclinicaFK = pk, estado = 'Activo', fecha_hora__range=(str(fecha_desde + " 00:00:00"),str(fecha_hasta + " 23:59:59")) ,id_examenfisicoFK__isnull=False).order_by('fecha_hora'):
            datos_fc.append(float(exam.id_examenfisicoFK.frecuencia_cardiaca))
            datos_fr.append(float(exam.id_examenfisicoFK.frecuencia_respiratoria))
            datos_tempax.append(float(exam.id_examenfisicoFK.temp_ax))
            datos_sat.append(float(exam.id_examenfisicoFK.sindrome_at))
            datos_pao.append(float(exam.id_examenfisicoFK.pao))
            datos_fio.append(float(exam.id_examenfisicoFK.fio))
            datos_paofio.append(float(exam.id_examenfisicoFK.pao_fio))
            datos_pas.append(float(exam.id_examenfisicoFK.pas))
            datos_pad.append(float(exam.id_examenfisicoFK.pad))
            datos_pam.append(float(exam.id_examenfisicoFK.pam))
            datos_avm.append(float(exam.id_examenfisicoFK.avm))
            datos_modo.append(float(exam.id_examenfisicoFK.modo))
            datos_vc.append(float(exam.id_examenfisicoFK.vc))
            datos_peep.append(float(exam.id_examenfisicoFK.peep))
            datos_pi.append(float(exam.id_examenfisicoFK.pi))
            datos_peso.append(float(exam.id_examenfisicoFK.peso))
            fecha_str = date.strftime(exam.fecha_hora,"%Y-%m-%d")
            dias.append(str(fecha_str))
        data['datos_fc'] = datos_fc
        data['datos_fr'] = datos_fr
        data['datos_tempax'] = datos_tempax
        data['datos_pao'] = datos_pao
        data['datos_fio'] = datos_fio
        data['datos_paofio'] = datos_paofio
        data['datos_pas'] = datos_pas
        data['datos_pad'] = datos_pad
        data['datos_pam'] = datos_pam
        data['datos_avm'] = datos_avm
        data['datos_modo'] = datos_modo
        data['datos_vc'] = datos_vc
        data['datos_peep'] = datos_peep
        data['datos_pi'] = datos_pi
        data['datos_peso'] = datos_peso
        data['id_historia'] = pk
        data['fecha'] = dias
        data['fechadesde'] = fecha_desde
        data['fechahasta'] = fecha_hasta
        return render(request,'evolucionapp/estadistica_fisica.html',data)
    except Exception as e:
        data['error'] = str(e)
    return response.HttpResponse(reverse_lazy('indexHistoriaC'))
@login_required
@csrf_exempt
def generar_estadistica(request):
    fecha_desde = request.POST['fecha_desde']
    fecha_hasta = request.POST['fecha_hasta']
    if fecha_desde > fecha_hasta:
        messages.error(request,"El rango de fecha solicitado es incorrecto!")
    pk = request.POST['pk']
    data = {}
    datos_gb = []
    datos_hb = []
    datos_ph = []
    datos_got = []
    datos_neu = []
    datos_htco = []
    datos_pco = []
    datos_gpt = []
    datos_lin = []
    datos_cr = []
    datos_hco = []
    datos_pt = []
    datos_cay = []
    datos_urea = []
    datos_alb = []
    datos_po = []
    datos_plq = []
    datos_na = []
    datos_eb = []
    datos_cl = []
    datos_k = []
    datos_lact = []
    datos_dd = []
    dias = []
    try:
        for labs in Evolucion.objects.filter(id_historiaclinicaFK = pk, estado = 'Activo', fecha_hora__range=(str(fecha_desde+" 00:00:00"),str(fecha_hasta+" 23:59:59")) ,id_resultadolabFK__isnull=False).order_by('fecha_hora'):
            datos_gb.append(float(labs.id_resultadolabFK.lab_gb))
            datos_hb.append(float(labs.id_resultadolabFK.lab_hb))
            datos_ph.append(float(labs.id_resultadolabFK.lab_ph))
            datos_got.append(float(labs.id_resultadolabFK.lab_got))
            datos_neu.append(float(labs.id_resultadolabFK.lab_neu))
            datos_htco.append(float(labs.id_resultadolabFK.lab_htco))
            datos_pco.append(float(labs.id_resultadolabFK.lab_pco))
            datos_gpt.append(float(labs.id_resultadolabFK.lab_gpt))
            datos_lin.append(float(labs.id_resultadolabFK.lab_lin))
            datos_cr.append(float(labs.id_resultadolabFK.lab_cr))
            datos_hco.append(float(labs.id_resultadolabFK.lab_hco))
            datos_pt.append(float(labs.id_resultadolabFK.lab_pt))
            datos_cay.append(float(labs.id_resultadolabFK.lab_cay))
            datos_urea.append(float(labs.id_resultadolabFK.lab_urea))
            datos_alb.append(float(labs.id_resultadolabFK.lab_alb))
            datos_po.append(float(labs.id_resultadolabFK.lab_po))
            datos_plq.append(float(labs.id_resultadolabFK.lab_plq))
            datos_na.append(float(labs.id_resultadolabFK.lab_na))
            datos_eb.append(float(labs.id_resultadolabFK.lab_eb))
            datos_cl.append(float(labs.id_resultadolabFK.lab_cl))
            datos_k.append(float(labs.id_resultadolabFK.lab_k))
            datos_lact.append(float(labs.id_resultadolabFK.lab_lact))
            datos_dd.append(float(labs.id_resultadolabFK.lab_dd))
            fecha_str = date.strftime(labs.fecha_hora,"%Y-%m-%d")
            dias.append(str(fecha_str))
        data['datos_gb'] = datos_gb
        data['datos_hb'] = datos_hb
        data['datos_ph'] = datos_ph
        data['datos_got'] = datos_got
        data['datos_neu'] = datos_neu
        data['datos_htco'] = datos_htco
        data['datos_pco'] = datos_pco
        data['datos_gpt'] = datos_gpt
        data['datos_lin'] = datos_lin
        data['datos_cr'] = datos_cr
        data['datos_hco'] = datos_hco
        data['datos_pt'] = datos_pt
        data['datos_cay'] = datos_cay
        data['datos_urea'] = datos_urea
        data['datos_alb'] = datos_alb
        data['datos_po'] = datos_po
        data['datos_plq'] = datos_plq
        data['datos_na'] = datos_na
        data['datos_eb'] = datos_eb
        data['datos_cl'] = datos_cl
        data['datos_k'] = datos_k
        data['datos_lact'] = datos_lact
        data['datos_dd'] = datos_dd
        data['id_historia'] = pk
        data['fecha'] = dias
        data['fechadesde'] = fecha_desde
        data['fechahasta'] = fecha_hasta
        return render(request,'evolucionapp/estadistica.html',data)
    except Exception as e:
        data['error'] = str(e)
    return response.HttpResponse(reverse_lazy('indexHistoriaC'))

# def importar_excel(request):
#     export = []

