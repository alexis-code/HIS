from django.urls import path
from .views import *

urlpatterns = [
    path('index/codigos',CodigoCieList.as_view(),name='indexCodigoCie'),
    path('index/activo',CodigoCieListActivo.as_view(),name='indexCodigoCieActivo'),
    path('index/anulado',CodigoCieListAnulado.as_view(),name='indexCodigoCieAnulado'),
    path('create',CreateCodigoCie.as_view(),name='createCodigoCie'),
    path('update/<int:pk>', UpdateCodigoCie.as_view(), name="updatecodigocie" ),
    path('anular', change_status ,name='CodigoCieChangeSatus'),

]