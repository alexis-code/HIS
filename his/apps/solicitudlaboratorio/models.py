from django.db import models
from django.forms.models import model_to_dict
from simple_history.models import HistoricalRecords

class SolicitudLaboratorio(models.Model):
    id_solicitudlabPK = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=150, blank=True, null=True)
    history = HistoricalRecords(table_name="audit_solic_lab")

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'SolicitudLab'
        verbose_name_plural = 'SolicitudLabs'
        db_table = 'tb_solicitudlab'

    def toJSON(self):
        item = model_to_dict(self)
        item['descripcion'] = self.descripcion
        item['estado'] = self.estado
        return item