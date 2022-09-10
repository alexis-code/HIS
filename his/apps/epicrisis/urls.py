from django.urls import path
from .views import *

urlpatterns = [
    path('index/<int:id>', ListEpicrisis.as_view(),name="IndexEpicrisis"),
    path('create/<int:id>', CreateEpicrisis.as_view(),name="CreateEpicrisis"),
    path('update/<int:pk>', UpdateEpicrisis.as_view(),name="UpdateEpicrisis"),
    path('detalle/<int:id>', DetalleEpicrisis.as_view(),name="DetalleEpicrisis"),
    path('anular', change_status,name="anular_epicrisis"),
]