from django.db import models
from django.forms.models import model_to_dict
from simple_history.models import HistoricalRecords

class Solucion(models.Model):
    id_solucionPK = models.AutoField(primary_key=True)
    nombre = models.CharField('Solucion', max_length=150, blank=False, null=False)
    descripcion = models.TextField('Descripcion', blank=False, null=False)
    history = HistoricalRecords(table_name="audit_solucion")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Solucion"
        verbose_name_plural = "Soluciones"
        db_table = "tb_solucion"

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre 
        item['descripcion'] = self.descripcion
        return item 

