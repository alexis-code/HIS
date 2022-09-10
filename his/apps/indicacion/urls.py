from django.urls import path
from .views import *

urlpatterns = [
    path('create/<int:pk>', CreateIndicacion.as_view(), name='createIndicacion'),
    path('update/<int:pk>', UpdateIndicacion.as_view(), name='updateIndicacion'),
    path('index/<int:fk>', IndicacionListFilterbyE.as_view(),name='IndicacionFilter'),
    path('detalle/<int:pk>', DetalleIndicacion.as_view(),name='IndicacionDetail'),

    path('index/indicacion/<int:fk>', IndicacionListFilterAll.as_view(),name='IndicacionFilterAll'),
    path('index/indicacion/activo/<int:fk>', IndicacionListFilterActivo.as_view(),name='IndicacionFilterActivo'),
    path('index/indicacion/anulado/<int:fk>', IndicacionListFilterAnulado.as_view(),name='IndicacionFilterAnulado'),
    
    path('cambiar_estado', change_status,name='change_statusIndicacion'),
]