from django.urls import path
from .views import CreateMedico, IndexMedico, PasswordChangeView

urlpatterns = [
    path('add',CreateMedico.as_view(),name='CrearMedico'),
    path('index',IndexMedico.as_view(),name='IndexMedico'),
    path('password',PasswordChangeView.as_view(),name='change_password')
]