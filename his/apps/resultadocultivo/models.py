from django.db import models
from django.db.models.deletion import CASCADE
from ..cultivo.models import Cultivo
from ..evolucion.models import Evolucion
from simple_history.models import HistoricalRecords

class ResultadoCultivo(models.Model):
    id_resultCultivoPK = models.AutoField(primary_key=True)
    id_cultivoFK = models.OneToOneField(Cultivo, on_delete=CASCADE)
    id_evolucionFK = models.ForeignKey(Evolucion, on_delete=CASCADE)
    medico = models.CharField('Nombre del Médico',max_length=150,blank=False,null=False, default="-")
    medico_udpated = models.CharField('Último en Modificar',max_length=150,blank=False,null=False, default="-")
    resultado_probable = models.CharField('Resultados Probables',max_length=50,blank=False,null=False)
    patogeno = models.CharField('Nombre del Patógeno',max_length=200,blank=True,null=True)
    sensible = models.CharField('Sensible',max_length=500,blank=True,null=True)
    resistente = models.CharField('Resistente',max_length=500,blank=True,null=True)
    parcial_sensible = models.CharField('Parcialmente Sensible',max_length=500,blank=True,null=True)
    comentario = models.TextField('Comentario', blank=True,null=True)
    estado = models.CharField('Estado',max_length=10,default='Activo')
    history = HistoricalRecords(table_name="audit_result_cultivo")

    class Meta:
        ordering = ['-id_resultCultivoPK']
        verbose_name='resultadocultivo'
        verbose_name_plural='resultadocultivos'
        db_table = 'tb_resultadoCultivo'
