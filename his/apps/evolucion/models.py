from django.db import models
from ..historiaclinica.models import HistoriaClinica
from ..examenfisico.models import ExamenFisico
from ..medico.models import Medico
from ..medicamento.models import Medicamento
from ..resultadolaboratorio.models import ResultadoLab
from ..cultivo.models import Cultivo
from django.forms import model_to_dict
from simple_history.models import HistoricalRecords

class Evolucion(models.Model):
    id_evolucionPK = models.AutoField(primary_key=True)
    id_historiaclinicaFK = models.ForeignKey(HistoriaClinica, on_delete=models.PROTECT)
    id_medicoFK = models.ForeignKey(Medico, on_delete=models.PROTECT)
    medico_updated = models.CharField('Último en Modificar', max_length=50,default="-")
    id_examenfisicoFK = models.ForeignKey(ExamenFisico, on_delete=models.PROTECT, null=True)
    id_resultadolabFK = models.ForeignKey(ResultadoLab,on_delete=models.PROTECT,null=True)
    nro_cama = models.IntegerField('Nro. de Cama', blank=False,null=False,default=1)
    fecha_hora = models.DateTimeField('Fecha', blank=False, null=False)
    dias_area = models.CharField('Dias en Areas', max_length=10,blank=False,null=False, default="-")
    diagnostico_evolucion = models.TextField('Diagnostico',blank=False,null=False, default="-")
    analisis = models.TextField('Análisis',blank=False,null=False,default="-")
    plan = models.TextField('Plan',blank=False,null=False,default="-")
    estado = models.CharField(max_length=20,blank=False,null=False, default='Activo')
    history = HistoricalRecords(table_name = 'audit_evol')

    def __str__(self):
        return str(self.fecha_hora)

    class Meta:
        ordering =['-id_evolucionPK']
        verbose_name = 'Evolucion'
        verbose_name_plural = 'Evoluciones'
        db_table = 'tb_evolucion'

class det_cultivo_evolucion(models.Model):
    id_det_cultivo_evolucionPK = models.AutoField(primary_key=True)
    id_evolucionFK = models.ForeignKey(Evolucion, on_delete=models.CASCADE, null=True)
    id_cultivoFK = models.ForeignKey(Cultivo, on_delete=models.CASCADE, null=True)
    fecha = models.DateField('Fecha',blank=False,null=False)
    estado = models.CharField('Estado',max_length=50,blank=True,null=False)
    history = HistoricalRecords(table_name = "audit_det_cultivo")

    def __str__(self):
        return self.fecha

    class Meta:
        db_table = 'det_cultivo_evolucion'

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_evolucionFK'])
        item['id_cultivoFK'] = self.id_cultivoFK.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['estado'] = self.estado
        return item


class det_tratmiento_evolucion(models.Model):
    id_det_tratamiento_evolucionPK = models.AutoField(primary_key=True)
    id_evolucionFK = models.ForeignKey(Evolucion, on_delete=models.CASCADE, null=True) 
    id_medicamentoFK = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField('Cantidad', blank=False,null=False)
    indicacion = models.CharField('Indicacion', max_length=500, blank=False,null=False,default="-")
    history = HistoricalRecords(table_name="audit_det_tratam")

    def __str__(self):
        return str(self.cantidad)

    class Meta:
        db_table = 'det_tratamiento_evolucion'

    def toJSON(self):
        item = model_to_dict(self,exclude=['id_evolucionFK'])
        item['id_medicamentoFK'] = self.id_medicamentoFK.toJSON()
        item['cant'] = self.cantidad
        item['indicacion'] = self.indicacion
        return item