from django.contrib import admin
from .models import HistoriaClinica

from simple_history.admin import SimpleHistoryAdmin

admin.site.register(HistoriaClinica,SimpleHistoryAdmin)
