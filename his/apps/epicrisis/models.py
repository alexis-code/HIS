from django.db import models
from django.db.models.fields import DateField
from ..evolucion.models import Evolucion
from ..medico.models import Medico
from ..codigocie.models import CodigoCie
from simple_history.models import HistoricalRecords

class Epicrisis(models.Model):
    id_epicrisisPK = models.AutoField(primary_key=True)
    id_evolucionFK = models.OneToOneField(Evolucion,on_delete=models.CASCADE)
    id_medicoFK = models.ForeignKey(Medico,on_delete=models.CASCADE)
    medico_updated = models.CharField('Último en Modificar', max_length=50,blank=True,null=True,default="-")
    total_dias = models.IntegerField('Total Días en Hospital', blank=False, null=False,default=0)
    proc_mayores = models.TextField('Procedimientos Mayores', blank=False,null=False)
    resumen_evolucion = models.TextField('Resumen de la evolución hospitalaria',blank=False,null=False)
    complicaciones = models.TextField('Complicaciones',blank=False,null=False)
    intervenciones = models.TextField('Intervenciones Quirurgicas',blank=False,null=False,default="-")
    estudios = models.TextField('Estudios Diagnósticos realizados',blank=False,null=False,default="-")
    estudio_imagenes = models.TextField('Estudio de Imagenes',blank=False,null=False,default="-")
    condicion_alta = models.CharField('Condición al alta',max_length=50,blank=False,null=False)
    contra_referido = models.CharField('Contra Referido',max_length=5,blank=False,null=False)
    motivo_alta = models.CharField('Motivo de alta',max_length=200,blank=False,null=False)
    motivo_descripcion = models.TextField('Motivo',blank=True,null=True)
    plan = models.TextField('Plan de Tratamiento al alta',blank=False,null=False,default="-")
    fecha = models.DateField('Fecha', blank=False,null=False)
    referido_centro = models.CharField(max_length=150,blank=True,null=True, default="-")
    red = models.CharField(max_length=50,blank=True,null=True, default="-")
    estado = models.CharField(max_length=20,blank=True,null=True, default='Activo')
    history = HistoricalRecords(table_name = 'audit_epicrisis')

    def __str__(self):
        return str(self.fecha)

    class Meta:
        ordering = ['-id_epicrisisPK']
        verbose_name = 'epicrisi'
        verbose_name_plural = 'epicrisis'
        db_table = 'tb_epicrisis'

class det_diagnosticodetalle(models.Model):
    id_det_detalle_diagnostico = models.AutoField(primary_key=True)
    id_epicrisisFK = models.ForeignKey(Epicrisis, on_delete=models.CASCADE)
    id_codigocieFK = models.ForeignKey(CodigoCie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_codigocieFK)

    class Meta:
        verbose_name = 'detallediagnostico'
        verbose_name_plural = 'detallediagnosticos'
        db_table = 'det_diagnosticodetalle'
