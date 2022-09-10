from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import Medico

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MedicoResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        exclude = ('id_medicoPK','last_login','is_superuser','groups','user_permissions','is_active','is_staff','date_joined','nro_registro')
        import_id_fields = ('password','username','first_name','last_name','email','especialidad','nro_documento','complemento','nro_telefono',)
        model = Medico

class UserAdminConfig(UserAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MedicoResource
    fieldsets = (
        ('Información Personal',{'fields':('username','first_name','last_name','email','especialidad','nro_documento','complemento','nro_telefono','password',)}),
        ('Permisos',{'fields':('is_active','is_staff','is_superuser',)}),
        ('Groups',{'fields':('groups',)}),
    )
    add_fieldsets = (
        ('Información Personal',{'fields':('username','first_name','last_name','email','especialidad','nro_documento','complemento','nro_telefono','password1','password2',)}),
        ('Permisos',{'fields':('is_active','is_staff','is_superuser')}),
        ('Groups',{'fields':('groups',)}),
    )

admin.site.register(Medico, UserAdminConfig)
admin.site.register(Permission)
