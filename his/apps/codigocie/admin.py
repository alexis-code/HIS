from django.contrib import admin
from .models import CodigoCie

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CodigoCieResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        exclude = ('id_codigo',)
        import_id_fields = ('codigo_cie','diagnostico')
        model = CodigoCie

class CodigoCieAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo_cie']
    list_display = ('codigo_cie','diagnostico')
    resource_class = CodigoCieResource

admin.site.register(CodigoCie, CodigoCieAdmin)
