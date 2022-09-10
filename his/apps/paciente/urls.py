from django.urls import path
from .views import PacienteList

urlpatterns = [
     path('index/', PacienteList.as_view(),name='ListaPaciente')
]