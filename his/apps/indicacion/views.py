from django.contrib.auth.decorators import login_required, permission_required
from django.http import response
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from .models import Indicacion, det_indicacion_medida_general, det_solicitud_indicacion, det_tratamiento_indicacion, det_solucion
from ..evolucion.models import Evolucion
from ..medicamento.models import Medicamento
from ..medidasgenerales.models import MedidasGenerales
from ..solicitudlaboratorio.models import SolicitudLaboratorio
from .forms import FormIndicacion
from django.db import connection, transaction
from his.settings import base
import json
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.contrib import messages


class CreateIndicacion(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required = ("indicacion.add_indicacion")
    model = Indicacion
    form_class = FormIndicacion
    template_name = 'indicacionapp/create.html'

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Evolucion, id_evolucionPK=id)

    
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
            if action == "search_solucion":
                data = []
                for i in Medicamento.objects.filter(nombre__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "indicacion_add":
                try:
                    with transaction.atomic():
                        medidageneral_list = json.loads(request.POST['medidageneral_list'])
                        tratamiento_list = json.loads(request.POST['tratamiento_list'])
                        solucion_list = json.loads(request.POST['solucion_list'])
                        solicitudlab_list = json.loads(request.POST['solicitudlab_list'])

                        indicacion = Indicacion()
                        indicacion.id_evolucionFK_id = request.POST['id_evolucionFK']
                        indicacion.id_medicoFK_id = request.POST['id_medicoFK']
                        indicacion.fecha_indicacion = date.today()
                        indicacion.dieta = request.POST['dieta']
                        indicacion.terapia_respiratoria = request.POST['terapia_respiratoria']
                        indicacion.save()

                        for i in medidageneral_list['medidasg']:
                            medida_general = MedidasGenerales()
                            medida_general.nombre = i['nombre']
                            medida_general.descripcion = i['descripcion']
                            medida_general.save()

                            det = det_indicacion_medida_general()
                            det.id_indicacionFK_id = indicacion.id_indicacionPK
                            det.id_medida_generalFK_id = medida_general.id_medidagPK
                            det.save()
                        
                        for i in tratamiento_list['tratamiento']:
                            det_tratamiento = det_tratamiento_indicacion()
                            det_tratamiento.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_tratamiento.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_tratamiento.cantidad = i['cant']
                            det_tratamiento.descripcion = i['descripcion']
                            det_tratamiento.indicacion = i['indicacion']
                            det_tratamiento.via_admin = i['via_admin']
                            det_tratamiento.save()

                        for i in solucion_list['solucion']:
                            det_sol = det_solucion()
                            det_sol.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_sol.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_sol.descripcion = i['descripcion']
                            det_sol.indicacion = i['indicacion']
                            det_sol.via_admin = i['via_admin']
                            det_sol.save()

                        for i in solicitudlab_list['solicitud']:
                            solicitud = SolicitudLaboratorio()
                            solicitud.descripcion = i['descripcion']
                            solicitud.estado = "En Curso"
                            solicitud.save()

                            det_solicitud = det_solicitud_indicacion()
                            det_solicitud.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_solicitud.id_solicitud_laboratioFK_id = solicitud.id_solicitudlabPK
                            det_solicitud.fecha_solicitud = i['fecha_solicitud']
                            det_solicitud.save()
                        messages.success(request,"La indicación se registró correctamente!")
                        data['id'] = indicacion.id_indicacionPK
                except Exception as e:
                    data['error'] = str(e)
                    messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        except Exception as e:
            data['error'] = str(e)
            messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label_button'] = "Registrar Indicación"
        return context

class UpdateIndicacion(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ("indicacion.change_indicacion")
    model = Indicacion
    form_class = FormIndicacion
    template_name = 'indicacionapp/update.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "search_medicamentos":
                data = []
                for i in Medicamento.objects.filter(nombre__icontains=request.POST['term'], estado="Activo"):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            if action == "search_solucion":
               data = []
               for i in Medicamento.objects.filter(nombre__icontains=request.POST['term'], estado="Activo"):
                   item = i.toJSON()
                   item['value'] = i.nombre
                   data.append(item)
            if action == "indicacion_edit":
                try:
                    with transaction.atomic():
                        medidageneral_list = json.loads(request.POST['medidageneral_list'])
                        tratamiento_list = json.loads(request.POST['tratamiento_list'])
                        solucion_list = json.loads(request.POST['solucion_list'])
                        solicitudlab_list = json.loads(request.POST['solicitudlab_list'])

                        indicacion = self.get_object()
                        indicacion.id_evolucionFK_id = request.POST['id_evolucionFK']
                        indicacion.medico_updated = request.POST['medico_updated']
                        indicacion.dieta = request.POST['dieta']
                        indicacion.terapia_respiratoria = request.POST['terapia_respiratoria']
                        indicacion.save()

                        indicacion.det_indicacion_medida_general_set.all().delete()
                        for i in medidageneral_list['medidasg']:
                            medida_general = MedidasGenerales()
                            medida_general.nombre = i['nombre']
                            medida_general.descripcion = i['descripcion']
                            medida_general.save()

                            det = det_indicacion_medida_general()
                            det.id_indicacionFK_id = indicacion.id_indicacionPK
                            det.id_medida_generalFK_id = medida_general.id_medidagPK
                            det.save()
                        
                        indicacion.det_tratamiento_indicacion_set.all().delete()
                        for i in tratamiento_list['tratamiento']:
                            det_tratamiento = det_tratamiento_indicacion()
                            det_tratamiento.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_tratamiento.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_tratamiento.cantidad = i['cant']
                            det_tratamiento.descripcion = i['descripcion']
                            det_tratamiento.indicacion = i['indicacion']
                            det_tratamiento.via_admin = i['via_admin']
                            det_tratamiento.save()

                        indicacion.det_solucion_set.all().delete()
                        for i in solucion_list['solucion']:
                            det_sol = det_solucion()
                            det_sol.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_sol.id_medicamentoFK_id = i['id_medicamentoPK']
                            det_sol.descripcion = i['descripcion']
                            det_sol.indicacion = i['indicacion']
                            det_sol.via_admin = i['via_admin']
                            det_sol.save()

                        indicacion.det_solicitud_indicacion_set.all().delete()
                        for i in solicitudlab_list['solicitud']:
                            solicitud = SolicitudLaboratorio()
                            solicitud.descripcion = i['descripcion']
                            solicitud.estado = i['estado']
                            solicitud.save()

                            det_solicitud = det_solicitud_indicacion()
                            det_solicitud.id_indicacionFK_id = indicacion.id_indicacionPK
                            det_solicitud.id_solicitud_laboratioFK_id = solicitud.id_solicitudlabPK
                            det_solicitud.fecha_solicitud = i['fecha_solicitud']
                            det_solicitud.save()
                        messages.success(request,"La indicación se edito correctamente!")
                except Exception as e:
                    data['error'] = str(e)
                    messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        except Exception as e:
            data['error'] = str(e)
            messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        return JsonResponse(data,safe=False)

    def get_detail_medidag(self):
        data = []
        try:
            for i in det_indicacion_medida_general.objects.filter(id_indicacionFK_id=self.get_object().id_indicacionPK):
                item = i.id_medida_generalFK.toJSON()
                data.append(item)
        except Exception as e:
            print(str(e))
        return data
    
    def get_detail_tratamiento(self):
        data = []
        try:
            for i in det_tratamiento_indicacion.objects.filter(id_indicacionFK_id=self.get_object().id_indicacionPK):
                item = i.id_medicamentoFK.toJSON()
                item['cant'] = i.cantidad
                item['descripcion'] = i.descripcion 
                item['indicacion'] = i.indicacion 
                item['via_admin'] = i.via_admin 
                data.append(item)
        except Exception as e:
            print(str(e))
        return data
    
    def get_detail_solucion(self):
        data = []
        try:
            for i in det_solucion.objects.filter(id_indicacionFK_id=self.get_object().id_indicacionPK):
                item = i.id_medicamentoFK.toJSON()
                item['descripcion'] = i.descripcion 
                item['indicacion'] = i.indicacion 
                item['via_admin'] = i.via_admin 
                data.append(item)
        except Exception as e:
            print(str(e))
        return data

    def get_detail_solicitud(self):
        data = []
        try:
            for i in det_solicitud_indicacion.objects.filter(id_indicacionFK_id=self.get_object().id_indicacionPK):
                item = i.id_solicitud_laboratioFK.toJSON()
                print(i.fecha_solicitud)
                item['fecha_solicitud'] = str(i.fecha_solicitud.strftime('%Y-%m-%d'))
                data.append(item)
        except Exception as e:
            print(str(e))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['det_medida'] = json.dumps(self.get_detail_medidag())
        context['det_tratamiento'] = json.dumps(self.get_detail_tratamiento())
        context['det_solucion'] = json.dumps(self.get_detail_solucion())
        context['det_solicitud'] = json.dumps(self.get_detail_solicitud())
        context['label_button'] = 'Confirmar Nuevos Datos'
        return context

#Listar la indicacion de la evolucion seleccionada
class IndicacionListFilterbyE(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("indicacion.view_indicacion")
    model = Indicacion
    template_name = 'indicacionapp/index.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK = fk, estado="Activo").order_by('-fecha_indicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_indicacionPK'] = self.kwargs['fk']
        return context

class IndicacionListFilterAll(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("indicacion.view_indicacion")
    model = Indicacion
    template_name = 'indicacionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK = fk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['fk']
        return context

class IndicacionListFilterActivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("indicacion.view_indicacion")
    model = Indicacion
    template_name = 'indicacionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK = fk,estado="Activo")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['fk']
        return context

class IndicacionListFilterAnulado(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("indicacion.view_indicacion")
    model = Indicacion
    template_name = 'indicacionapp/indexAll.html'

    def get_queryset(self):
        fk = self.kwargs['fk']
        return self.model.objects.filter(id_evolucionFK = fk, estado="Anulado")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['fk']
        return context

#DetalleIdicacion
class DetalleIndicacion(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = ("indicacion.view_indicacion")
    def get(self, request, *args, **kwargs):
        try:
            context = {
                'indicacion':Indicacion.objects.get(id_indicacionPK=self.kwargs['pk']),
                'logohospital': '{}{}'.format(base.MEDIA_URL, 'logo-hospital.png'),
                'logogobernacion': '{}{}'.format(base.MEDIA_URL, 'logo-gobernacion.png'),
                'direccion': 'Av. San Martin de Porres',
                'ciudad': 'Comarapa - Santa Cruz - Bolivia',
            }
            return render(request,'indicacionapp/detalle.html',context)
        except Exception as e:
            messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        return response.HttpResponseRedirect(reverse_lazy('indexHistoriaC'))

@login_required
@permission_required("indicacion.change_indicacion")
def change_status(request):
    pk = request.POST.get('pk')
    indicacion = Indicacion.objects.get(id_indicacionPK=pk)
    if indicacion.estado == 'Activo':
        indicacion.estado = 'Anulado'
        indicacion.save()
    else:
        indicacion.estado = 'Activo'
        indicacion.save()
    id = indicacion.id_evolucionFK_id
    data = id
    messages.success(request,"Se cambio el estado.")
    return response.HttpResponse(data)