from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard",GenerarEstadistica.as_view(), name="dashboard"),
    path('cardex', IndexHistoriaClinicaAll.as_view(), name="indexHistoriaCAll"),
    path('cardex/codigo/<int:cod>', IndexHistoriaClinicaByCodigo.as_view(), name="IndexHistoriaClinicaByCodigo"),
    path('cardex/paciente/<int:ci>', IndexHistoriaClinicaByCi.as_view(), name="IndexHistoriaClinicaByCi"),

    path('cardex/epicrisis/<int:id>', ListEpicrisisAll.as_view(),name="IndexEpicrisisAll"),
    path('cardex/epicrisis/activo/<int:id>', ListEpicrisisAllActivo.as_view(),name="IndexEpicrisisAllactivo"),
    path('cardex/epicrisis/anulados/<int:id>', ListEpicrisisAllInactivo.as_view(),name="IndexEpicrisisAllinactivo"),
]