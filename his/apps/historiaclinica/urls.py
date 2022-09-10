from django.urls import path
from .views import *

urlpatterns = [
    path('index', IndexHistoriaClinicaActivo.as_view(), name="indexHistoriaC"),
    path('create', CreateHistoriaClinica.as_view(), name="createhistoriaclinica" ),
    path('update/<int:pk>', UpdateHistoriaClinica.as_view(), name="updatehistoriaclinica" ),
    path('detalle/<int:pk>', DetalleHistoria.as_view(), name="detallehistoriaclinica" ),
    path('epicrisis/<int:pk>', DetalleHistoria.as_view(), name="detallehistoriaclinica" ),
    path('change_status', change_status, name='cambiarestadoHC'),

    path('index/<int:cod>', IndexHistoriaClinicaByCod.as_view(), name="indexHistoriaCByCod"),
    path('index/byfecha', FilterbyFecha.as_view(), name="filtrar_fecha"),
    
    #en caso de encontrar una coincidencia de nro_documento se redirige a crear una evolución
    path('redirigir/evolucion/', redirectToEvolucionCreate,name="redirigirEvolucion")
]