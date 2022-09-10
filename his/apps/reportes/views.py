from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.db import connection
from django.http import response
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import View
from django.views.generic.list import ListView

from ..historiaclinica.models import HistoriaClinica
from ..epicrisis.models import Epicrisis

class GenerarEstadistica(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = ('historiaclinica.view_historiaclinica')
    def get(self,request,*args,**kwargs):
        data = {}
        def dictfetchall(cursor):
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        script_hc = "select count(*) as cantidad, monthname(fecha_ingresohospital) as mes from db_his_test.tb_historiaclinica where year(fecha_ingresohospital) = year(curdate()) group by month(fecha_ingresohospital) order by fecha_ingresohospital"
        script_medicamentos = "SELECT sum(dt.cantidad) AS cantidad, m.nombre FROM det_tratamiento_evolucion dt INNER JOIN tb_medicamento m ON dt.id_medicamentoFK_id = m.id_medicamentoPK GROUP BY m.id_medicamentoPK LIMIT 3"
        script_child = "select count(*) as cantidad, '1-12 años' as rango from db_his_test.tb_paciente where edad between 1 and 12"
        script_teen = "select count(*) as cantidad, '13-17 años' as rango from db_his_test.tb_paciente where edad between 13 and 17"
        script_adult = "select count(*) as cantidad, '18-39 años' as rango from db_his_test.tb_paciente where edad between 18 and 39"
        script_adult2 = "select count(*) as cantidad, '40-59 años' as rango from db_his_test.tb_paciente where edad between 40 and 59"
        script_elderly = "select count(*) as cantidad, '>= 60 años' as rango from db_his_test.tb_paciente where edad >= 60"

        try:
            with connection.cursor() as cursor_hc:
                #cursor para obtener la cantidad de Historias clinicas por més
                cursor_hc.execute(script_hc)
                result = dictfetchall(cursor_hc)
                data_mes_hc = []
                data_cantidad_hc = []
                cantidad = len(result)
                cont = 0
                while cantidad > cont:
                    data_mes_hc.append(result[cont]['mes'])
                    data_cantidad_hc.append(result[cont]['cantidad'])
                    cont = cont + 1
                data['mes'] = data_mes_hc
                data['cantidad'] = data_cantidad_hc

                #cursor para obtener un top 3 de los medicamentos más usados
                cursor_hc.execute(script_medicamentos)
                result_medic = dictfetchall(cursor_hc)
                data_nombre_medic = []
                data_cantidad_medic = []
                cantidad_medic = len(result_medic)
                cont_medic = 0
                while cantidad_medic > cont_medic:
                    data_nombre_medic.append(result_medic[cont_medic]['nombre'])
                    data_cantidad_medic.append(int(result_medic[cont_medic]['cantidad']))
                    cont_medic = cont_medic + 1
                data['nombre_medic'] = data_nombre_medic
                data['cantidad_medic'] = data_cantidad_medic

                #cursor para obtener el total de pacientes por rango de edades
                cursor_hc.execute(script_child)
                result_child = dictfetchall(cursor_hc)
                data_cantidad_rango = []
                data_rango = []
                data_cantidad_rango.append(result_child[0]["cantidad"])
                data_rango.append(result_child[0]["rango"])

                cursor_hc.execute(script_teen)
                result_teen = dictfetchall(cursor_hc)
                data_cantidad_rango.append(result_teen[0]["cantidad"])
                data_rango.append(result_teen[0]["rango"])

                cursor_hc.execute(script_adult)
                result_adult = dictfetchall(cursor_hc)
                data_cantidad_rango.append(result_adult[0]["cantidad"])
                data_rango.append(result_adult[0]["rango"])

                cursor_hc.execute(script_adult2)
                result_adult2 = dictfetchall(cursor_hc)
                data_cantidad_rango.append(result_adult2[0]["cantidad"])
                data_rango.append(result_adult2[0]["rango"])

                cursor_hc.execute(script_elderly)
                result_ederly = dictfetchall(cursor_hc)
                data_cantidad_rango.append(result_ederly[0]["cantidad"])
                data_rango.append(result_ederly[0]["rango"])

                data['cantidad_rango'] = data_cantidad_rango
                data['rango'] = data_rango
            
            return render(request,'reportesapp/index.html',data)
        except Exception as e:
            print(str(e))
        return response.HttpResponse(reverse_lazy('indexHistoriaC'),data)

class IndexHistoriaClinicaByCi(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('historiaclinica.view_historiaclinica')
    model = HistoriaClinica
    template_name = "reportesapp/indexAll.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
      ci = self.kwargs['ci']
      return self.model.objects.filter(id_pacienteFK__nro_documento = ci)

class IndexHistoriaClinicaByCodigo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('historiaclinica.view_historiaclinica')
    model = HistoriaClinica
    template_name = "reportesapp/indexAll.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
      cod = self.kwargs['cod']
      return self.model.objects.filter(cod_historiaclinica = cod)

class IndexHistoriaClinicaAll(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('historiaclinica.view_historiaclinica')
    model = HistoriaClinica
    template_name = "reportesapp/indexAll.html"
    paginate_by = 6


class ListEpicrisisAllActivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("epicrisis.view_epicrisis")
    model = Epicrisis
    template_name = 'reportesapp/reportEpicrisis.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(id_evolucionFK__id_historiaclinicaFK = self.kwargs['id'], estado='Activo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        context['id'] = id
        return context

class ListEpicrisisAllInactivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("epicrisis.view_epicrisis")
    model = Epicrisis
    template_name = 'reportesapp/reportEpicrisis.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(id_evolucionFK__id_historiaclinicaFK = self.kwargs['id'], estado='Anulado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        context['id'] = id
        return context


class ListEpicrisisAll(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required=("epicrisis.view_epicrisis")
    model = Epicrisis
    template_name = 'reportesapp/reportEpicrisis.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(id_evolucionFK__id_historiaclinicaFK = self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        context['id'] = id
        context['action'] = 'reporte'
        return context