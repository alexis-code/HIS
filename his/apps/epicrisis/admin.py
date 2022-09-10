from django.contrib import admin
from .models import Epicrisis
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Epicrisis,SimpleHistoryAdmin)
