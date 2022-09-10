from django.db import models
from django.forms.models import model_to_dict

class Medicamento(models.Model):
    id_medicamentoPK = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre del Medicamento',max_length=500,blank=False,null=False)
    medida = models.CharField('gr/ml/etc',max_length=100,blank=False,null=False)
    estado = models.CharField('Estado', max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-id_medicamentoPK']
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        db_table = 'tb_medicamento'

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['medida'] = self.medida
        return item