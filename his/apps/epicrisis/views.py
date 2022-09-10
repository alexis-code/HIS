import json

from django.contrib import messages
from apps.historiaclinica.models import HistoriaClinica
from django.http import response
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, View, ListView, UpdateView
from django.db import transaction
from django.http.response import JsonResponse
from datetime import datetime,date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Epicrisis, det_diagnosticodetalle
from ..evolucion.models import Evolucion
from ..codigocie.models import CodigoCie

from .forms import FormEmpicrisis

class ListEpicrisis(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("epicrisis.view_epicrisis")
    model = Epicrisis
    template_name = 'epicrisisapp/index.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(id_evolucionFK__id_historiaclinicaFK = self.kwargs['id'], estado="Activo")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        context['id'] = id
        return context




class CreateEpicrisis(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required=("epicrisis.add_epicrisis")
    model = Epicrisis
    form_class = FormEmpicrisis
    template_name = "epicrisisapp/create.html"

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Evolucion, id_evolucionPK=id)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        evolucion = Evolucion.objects.get(id_evolucionPK=id)
        nro_cama = evolucion.nro_cama
        context['nro_cama'] = nro_cama
        
        #Calcula el total de dias que el paciente estuvo en el area desde el ingreso al hospital
        fecha_ingreso = evolucion.id_historiaclinicaFK.fecha_ingresohospital
        fecha_actual = datetime.now()
        resultado = (fecha_actual - fecha_ingreso).days
        context['diasArea'] = resultado
        return context


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']

        try:
            if action == 'search_cie':
                data = []
                for i in CodigoCie.objects.filter(codigo_cie__icontains=request.POST['term'], estado='Activo'):
                    item = i.toJSON()
                    item['value'] = i.codigo_cie
                    data.append(item)
            if action == 'search_diagnostico':
                data = []
                for i in CodigoCie.objects.filter(diagnostico__icontains=request.POST['term'], estado='Activo'):
                    item = i.toJSON()
                    item['value'] = i.diagnostico
                    data.append(item)
            if action == "epicrisis_add":
                try:
                    with transaction.atomic():
                        diagnostico_list = json.loads(request.POST['diagnostico'])
                        
                        epicrisis = Epicrisis()
                        epicrisis.id_evolucionFK_id = request.POST['id_evolucionFK']
                        epicrisis.id_medicoFK_id = request.POST['id_medicoFK']
                        epicrisis.total_dias = request.POST['total_dias']
                        epicrisis.proc_mayores = request.POST['proc_mayores']
                        epicrisis.resumen_evolucion = request.POST['resumen_evolucion']
                        epicrisis.complicaciones = request.POST['complicaciones']
                        epicrisis.intervenciones = request.POST['intervenciones']
                        epicrisis.estudios = request.POST['estudios']
                        epicrisis.estudio_imagenes = request.POST['estudio_imagenes']
                        epicrisis.condicion_alta = request.POST['condicion_alta']
                        epicrisis.contra_referido = request.POST['contra_referido']
                        epicrisis.motivo_alta = request.POST['motivo_alta']
                        epicrisis.referido_centro = request.POST['referido_centro']
                        epicrisis.red = request.POST['red']
                        if request.POST['motivo_alta'] == "Otros":
                            epicrisis.motivo_descripcion = request.POST['motivo_descripcion']
                        else:    
                            epicrisis.motivo_descripcion = "-"
                        epicrisis.plan = request.POST['plan']
                        epicrisis.fecha = date.today()
                        epicrisis.save()

                        for i in diagnostico_list['diagnosticos']:
                            diagnostico = det_diagnosticodetalle()
                            diagnostico.id_epicrisisFK_id = epicrisis.id_epicrisisPK
                            diagnostico.id_codigocieFK_id = i['id_codigo']
                            diagnostico.save()

                        evolucion = Evolucion.objects.get(id_evolucionPK = epicrisis.id_evolucionFK_id)
                        historia = HistoriaClinica.objects.get(id_historiaPK = evolucion.id_historiaclinicaFK_id)
                        historia.estado = "Inactivo"
                        historia.save()
                        messages.success(request,"Epicrisis registrada correctamente!")
                        data['id'] = epicrisis.id_epicrisisPK
                except Exception as e:
                    data['error'] = str(e)
                    messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        except Exception as e:
            data['error'] = str(e)
            messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        return JsonResponse(data,safe=False)

class UpdateEpicrisis(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required=("epicrisis.change_epicrisis")
    model = Epicrisis
    form_class = FormEmpicrisis
    template_name = 'epicrisisapp/update.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "search_cie":
                data =[]
                for i in CodigoCie.objects.filter(codigo_cie__icontains=request.POST['term'],estado='Activo'):
                    item = i.toJSON()
                    item['value'] = i.codigo_cie
                    data.append(item)
            if action == 'search_diagnostico':
                data = []
                for i in CodigoCie.objects.filter(diagnostico__icontains=request.POST['term'],estado='Activo'):
                    item = i.toJSON()
                    item['value'] = i.diagnostivo
                    data.append(item)
            if action == 'epicrisis_edit':
                try:
                    with transaction.atomic():
                        diagnostico_list = json.loads(request.POST['diagnostico'])
                        
                        epicrisis = Epicrisis.objects.get(pk = self.get_object().id_epicrisisPK)
                        epicrisis.id_evolucionFK_id = request.POST['id_evolucionFK']
                        epicrisis.medico_updated = request.POST['medico_updated']
                        epicrisis.total_dias = request.POST['total_dias']
                        epicrisis.proc_mayores = request.POST['proc_mayores']
                        epicrisis.resumen_evolucion = request.POST['resumen_evolucion']
                        epicrisis.complicaciones = request.POST['complicaciones']
                        epicrisis.intervenciones = request.POST['intervenciones']
                        epicrisis.estudios = request.POST['estudios']
                        epicrisis.estudio_imagenes = request.POST['estudio_imagenes']
                        epicrisis.condicion_alta = request.POST['condicion_alta']
                        epicrisis.contra_referido = request.POST['contra_referido']
                        epicrisis.motivo_alta = request.POST['motivo_alta']
                        epicrisis.referido_centro = request.POST['referido_centro']
                        epicrisis.red = request.POST['red']
                        if request.POST['motivo_alta'] == "Otros":
                            epicrisis.motivo_descripcion = request.POST['motivo_descripcion']
                        else:    
                            epicrisis.motivo_descripcion = "-"
                        epicrisis.plan = request.POST['plan']
                        epicrisis.save()

                        epicrisis.det_diagnosticodetalle_set.all().delete()
                        for i in diagnostico_list['diagnosticos']:
                            diagnostico = det_diagnosticodetalle()
                            diagnostico.id_epicrisisFK_id = epicrisis.id_epicrisisPK
                            diagnostico.id_codigocieFK_id = i['id_codigo']
                            diagnostico.save()


                        evolucion = Evolucion.objects.get(id_evolucionPK = epicrisis.id_evolucionFK_id)
                        historia = HistoriaClinica.objects.get(id_historiaPK = evolucion.id_historiaclinicaFK_id)
                        historia.estado = "Inactivo"
                        historia.save()

                        data['id'] = epicrisis.id_epicrisisPK
                        messages.success(request,"Epicrisis editada correctamente!")
                except Exception as e:
                    data['error'] = str(e)
                    messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        except Exception as e:
            data['error'] = str(e)
            messages.error(request,"error: "+str(e)+", contacte con su administrador.")
        return JsonResponse(data,safe=False)

    def get_detail_diagnostico(self):
        data = []
        try:
            for i in det_diagnosticodetalle.objects.filter(id_epicrisisFK_id=self.get_object().id_epicrisisPK):
                item = i.id_codigocieFK.toJSON()
                data.append(item)
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['det_diagnostico'] = json.dumps(self.get_detail_diagnostico())
        context['label_button'] = "Guardar Cambios"
        return context      


class DetalleEpicrisis(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required=("epicrisis.view_epicrisis")
    def get(self, request, *args, **kwargs):
        try:
            context = {
                'epicrisis': Epicrisis.objects.get(id_epicrisisPK=self.kwargs['id']),
                'direccion': '3er. Anillo Externo, Av. Japón, entre Av. Canal Cotoca y Av. Paraguá – Telef. Piloto: 3-462037',
                'ciudad': 'Santa Cruz de la Sierra - Bolivia',
            }
            return render(request, 'epicrisisapp/detalle.html',context)
        except Exception as e:
            print(str(e))
        return response.HttpResponseRedirect(reverse_lazy('indexHistoriaC'))

@login_required
@permission_required("epicrisis.change_epicrisis")
def change_status(request):
    pk = request.POST.get('pk')
    epicrisis = Epicrisis.objects.get(id_epicrisisPK=pk)
    if epicrisis.estado == 'Activo':
        epicrisis.estado = 'Anulado'
        epicrisis.save()
    else:
        epicrisis.estado = 'Activo'
        epicrisis.save()
    response = JsonResponse({'mensaje': 'Exito!!'})
    response.status_code = 200
    messages.success(request,"Se cambio el estado.")
    return response
    