from django.urls import path
from .views import MedicamentoList, CreateMedicamento, UpdateMedicamento, change_status

urlpatterns = [
    path('index', MedicamentoList.as_view(), name='ListaMedicamento'),
    path('create', CreateMedicamento.as_view(), name="createmedicamento" ),
    path('anular', change_status ,name='MedicamentoChangeSatus'),
    path('update/<int:pk>', UpdateMedicamento.as_view(), name="updatemedicamento" ),
]