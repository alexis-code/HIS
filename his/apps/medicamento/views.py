from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from .models import Medicamento
from .forms import MedicamentoForms
from django.urls.base import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


class MedicamentoList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("medicamento.view_medicamento")
    model = Medicamento
    template_name = "medicamentoapp/indexmedicamento.html"
    
    def get_queryset(self):
        return self.model.objects.filter(estado = 'Activo')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CreateMedicamento(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ("medicamento.add_medicamento")
    model = Medicamento
    form_class = MedicamentoForms
    template_name = "medicamentoapp/create.html"
    success_url = reverse_lazy("ListaMedicamento")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            form = MedicamentoForms(request.POST)
            if action == "medicamento_add":
                if request.POST['nombre'].strip() != "" and request.POST['medida'].strip != "":
                    medicamento = Medicamento()
                    medicamento.nombre = request.POST['nombre']
                    medicamento.medida = request.POST['medida']
                    medicamento.estado = "Activo"
                    medicamento.save()
                else:
                    messages.error(self.request,"Error al registrar el medicamento, verifique la información a registrar")
        except Exception as e:
            data['error'] = 'Error al procesar la solicitud: ' + str(e)
            messages.error(self.request,"Error al procesar la solicitud")
            print(data['error'])
        return redirect("ListaMedicamento") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "medicamento_add"
        return context

class UpdateMedicamento(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ("medicamento.change_medicamento")
    model = Medicamento
    form_class = MedicamentoForms
    template_name = "medicamentoapp/update.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label_boton'] = 'Confirmar los datos nuevos'
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'medicamento_edit':
                if request.POST['nombre'].strip() != "" and request.POST['medida'].strip() != "":
                    medicamento = Medicamento.objects.get(pk = self.get_object().id_medicamentoPK)
                    medicamento.nombre = request.POST['nombre'] 
                    medicamento.medida = request.POST['medida']
                    medicamento.estado = 'Activo'
                    medicamento.save()
                else:
                    messages.error(self.request,"Error al modificar el medicamento, verifique la información a registrar")
        except Exception as e:
            data['error'] = str(e)
            messages.error(self.request,"Error al procesar la solicitud")
            print(str(e))
        return redirect("ListaMedicamento")

@login_required
@permission_required("medicamento.change_medicamento")
def change_status(request):
    pk = request.POST.get('pk')
    medicamento = Medicamento.objects.get(id_medicamentoPK=pk)
    medicamento.estado = 'Anulado'
    medicamento.save()
    response = JsonResponse({'mensaje': 'Exito!!'})
    response.status_code = 200
    messages.success(request,"Se cambio el estado del medicamento: "+medicamento.nombre)
    return response