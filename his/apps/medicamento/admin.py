from django.contrib import admin
from .models import Medicamento

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MedicamentoResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        exclude = ('id_medicamentoPK',)
        import_id_fields = ('nombre','medida','estado')
        model = Medicamento

class MeciamentoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre','medida','estado')
    resource_class = MedicamentoResource

admin.site.register(Medicamento,MeciamentoAdmin)
