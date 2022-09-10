from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from django.views.generic import CreateView,ListView
from django.views.generic.edit import FormView
from .forms import FormularioLogin, FormCreateMedico
from .models import Medico


class CreateMedico(CreateView,LoginRequiredMixin):
    model = Medico
    form_class = FormCreateMedico
    template_name = 'createMedico.html'

class IndexMedico(ListView,LoginRequiredMixin):
    model = Medico
    template_name = 'indexMedico.html'

class PasswordChangeView(PasswordChangeView,LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = 'change-password.html'
    success_url = reverse_lazy('logout')

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('Inicio')
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

    def post(self, request, *args, **kwargs):
        msg = None
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            msg = 'Credenciales Incorrectas'

        return render(request,"login.html",{"msg":msg})

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')