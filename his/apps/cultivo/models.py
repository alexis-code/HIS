from django.db import models
from django.forms.models import model_to_dict

class Cultivo(models.Model):
    id_cultivoPK = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de Cultivo', max_length=150,blank=False,null=False)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'
        db_table = 'tb_cultivo'

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        return item
