from django.urls import path
from .views import *

urlpatterns = [
    path('index/<int:fk>', EvolucionListFilterbyHC.as_view(),name='EvolucionFilter'),
    path('index/byfecha', EvolucionListbyFecha.as_view(),name='FilterbyFechaEvolucion'),
   
    path('index/evoluciones/Activo/<int:fk>',EvolucionListFilterbyHCActivo.as_view(),name='EvolucionIndexActivo'),
    path('index/evoluciones/Anulados/<int:fk>',EvolucionListFilterbyHCAnulado.as_view(),name='EvolucionIndexAnulado'),
    path('create/<int:id>', EvolucionDetailCreate.as_view(),name='EvolucionCreate'),
    path('update/<int:pk>', EvolucionUpdate.as_view(),name='EvolucionUpdate'),
    path('anular', change_status,name='EvolucionChangeSatus'),
    path('detalle/<int:pk>', DetalleEvolucion.as_view(),name='EvolucionDetail'),
    path('index/evoluciones/<int:fk>',EvolucionListFilterbyHCAll.as_view(),name='EvolucionIndexAll'),
    
    #url para cultivos
    path('cultivo/pendientes/<int:fk>',CultivoSolicitadoListEnCurso.as_view(),name='ListaCultivosSolicitados'),
    path('cultivo/resultados/<int:fk>',ResultadoCultivoList.as_view(),name='CultivosRegistrados'),
    #Urls para las acciones con los resultados de cultivos
    path('registrar_resultado',registrar_result_cultivo,name="RegistroResultCultivo"), 
    path('result_cultivo/<int:fk>', ResultadoCultivoList.as_view(),name='ResultadoCultivo'),
    path('update/resultado_cultivo/<int:pk>', UpdateResultCultivo.as_view(),name='ResultCultivoUpdate'),
    path('detalle_cultivo/<int:pk>', DetalleResultCultivo.as_view(),name='DetalleCultivo'),
    path('change_status/cultivo/',change_status_cultivo,name='ResultCultivo_anular'),

    path('estadistica/generar/', generar_estadistica,name='GenerarEstadistica'),
    path('estadistica/examenfisico/generar/', generar_estadistica_fisico,name='GenerarEstadisticaFisica'),

]