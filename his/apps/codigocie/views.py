from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .models import CodigoCie
from django.urls.base import reverse_lazy
from .forms import CodigocieForms
from .models import CodigoCie

class CodigoCieList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("codigocie.view_codigocie")
    model = CodigoCie
    template_name = "codigocieapp/index.html"


class CodigoCieListActivo(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("codigocie.view_codigocie")
    model = CodigoCie
    template_name = "codigocieapp/index.html"

    def get_queryset(self):
       return self.model.objects.filter(estado='Activo')

class CodigoCieListAnulado(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ("codigocie.view_codigocie")
    model = CodigoCie
    template_name = "codigocieapp/index.html"

    def get_queryset(self):
       return self.model.objects.filter(estado='Anulado')

    

class CreateCodigoCie(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ("codigocie.add_codigocie")
    model = CodigoCie
    form_class = CodigocieForms
    template_name = "codigocieapp/create.html"
    success_url = reverse_lazy("indexCodigoCie")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "codigocie_add":
                codigo_cie = CodigoCie()
                codigo_cie.codigo_cie = request.POST['codigo_cie'] 
                codigo_cie.diagnostico = request.POST['diagnostico']
                codigo_cie.estado = 'Activo'
                codigo_cie.save()
        except Exception as e:
            data['error'] = 'Error al procesar la solicitud: ' + str(e)
            print(data['error'])

        return redirect("indexCodigoCie") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "codigocie_add"
        return context


class UpdateCodigoCie(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ("codigocie.change_codigocie")
    model = CodigoCie
    form_class = CodigocieForms
    template_name = "codigocieapp/update.html"

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
            if action == 'codigocie_edit':
                codigocie = CodigoCie.objects.get(pk = self.get_object().id_codigo)
                codigocie.codigo_cie = request.POST['codigo_cie'] 
                codigocie.diagnostico = request.POST['diagnostico']
                codigocie.estado = 'Activo'
                codigocie.save()
        
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        
        return redirect("indexCodigoCie")


@login_required
@permission_required("codigocie.change_codigocie")
def change_status(request):
    pk = request.POST.get('pk')
    codigo_cie = CodigoCie.objects.get(id_codigo=pk)
    if codigo_cie.estado == 'Activo':
        codigo_cie.estado = 'Anulado'
        codigo_cie.save()
    else:
        codigo_cie.estado = 'Activo'
        codigo_cie.save()
    response = JsonResponse({"mensaje": "Exito!!"})
    response.status_code = 200
    messages.success(request,"Se cambió el estado del codigo CIE - 10: "+codigo_cie.codigo_cie)
    return response