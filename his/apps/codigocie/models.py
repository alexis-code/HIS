from django.db import models
from django.forms.models import model_to_dict

class CodigoCie(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    codigo_cie = models.CharField('Código CIE-10', max_length=20, blank=False,null=False)
    diagnostico = models.TextField('Diagnóstico',blank=False,null=False)
    estado = models.CharField('Estado', max_length=10, blank=False, null=False, default='Activo')

    def __str__(self):
        return self.diagnostico
    
    class Meta:
        ordering = ['-id_codigo']

    def toJSON(self):
        item = model_to_dict(self)
        item['codigo_cie'] = self.codigo_cie
        item['diagnostico'] = self.diagnostico
        return item