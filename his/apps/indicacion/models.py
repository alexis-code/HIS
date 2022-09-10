from django.db import models
from django.db.models.expressions import F
from django.forms.models import model_to_dict
from ..solicitudlaboratorio.models import SolicitudLaboratorio
from ..medidasgenerales.models import MedidasGenerales
from ..evolucion.models import Evolucion
from ..medico.models import Medico
from ..solucion.models import Solucion
from ..medicamento.models import Medicamento
from datetime import date, datetime
from simple_history.models import HistoricalRecords

class Indicacion(models.Model):
    id_indicacionPK = models.AutoField(primary_key=True)
    id_evolucionFK = models.ForeignKey(Evolucion, on_delete=models.CASCADE)
    id_medicoFK = models.ForeignKey(Medico, on_delete=models.CASCADE)
    medico_updated = models.CharField('Último en Modificar', max_length=50,blank=True,null=True,default="-")
    fecha_indicacion = models.DateField(blank=False, null=False)
    dieta = models.TextField('Dieta',blank=True, null=True)
    terapia_respiratoria = models.TextField('Terapia Respiratoria', blank=True, null=True)
    estado = models.CharField('Estado',max_length=10,blank=False,null=False,default='Activo')
    history = HistoricalRecords(table_name="audit_indicacion")

    class  Meta:
        verbose_name = "Indicacion"
        verbose_name_plural = "Indicaciones"
        db_table = "tb_indicacion"

class det_indicacion_medida_general(models.Model):
    id_det_indicacion_medidaPK = models.AutoField(primary_key=True)
    id_indicacionFK = models.ForeignKey(Indicacion, on_delete=models.CASCADE)
    id_medida_generalFK = models.ForeignKey(MedidasGenerales, on_delete=models.CASCADE)
    history = HistoricalRecords(table_name="audit_det_indic_medida")

    class Meta:
        db_table = "det_indicacion_medida_general"

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_indicacionFK'])
        item['id_medida_generalFK'] = self.id_medida_generalFK.toJSON()
        return item

class det_tratamiento_indicacion(models.Model):
    id_det_tratamiento_indicacionPK = models.AutoField(primary_key=True)
    id_indicacionFK = models.ForeignKey(Indicacion, on_delete=models.CASCADE)
    id_medicamentoFK =models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField('Cantidad', blank=False, null=False)
    descripcion = models.CharField('Descripción', max_length=200, blank=True,null=True)
    indicacion = models.CharField('Indicacion', max_length=500, blank=False,null=False,default="-")
    via_admin = models.CharField('Via de Administración', max_length=10, blank=True, null=True, default="-")
    history = HistoricalRecords(table_name="audit_det_indic_tratam")

    class Meta:
        db_table = "det_tratamiento_indicacion"

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_indicacionFK'])
        item['id_medicamentoFK'] = self.id_medicamentoFK.toJSON()
        item['cantidad'] = self.cantidad
        item['descripcion'] = self.descripcion
        item['indicacion'] = self.indicacion
        item['via_admin'] = self.via_admin
        return item

class det_solucion(models.Model):
    id_det_solucionPK = models.AutoField(primary_key=True)
    #id_solucionFK = models.ForeignKey(Solucion, on_delete=models.CASCADE)
    id_indicacionFK =models.ForeignKey(Indicacion, on_delete=models.CASCADE)
    id_medicamentoFK =models.ForeignKey(Medicamento, on_delete=models.CASCADE   )
    descripcion = models.CharField('Descripción', max_length=200, blank=True,null=True)
    indicacion = models.TextField('Indicacion',max_length=200,blank=True,null=True)
    via_admin = models.CharField('Via de Administración', max_length=10, blank=True, null=True, default="-")
    history = HistoricalRecords(table_name="audit_det_indic_soluc")

    class Meta:
        db_table ="det_solucion_nombresolucion"

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_indicacionFK'])
        item['id_medicamentoFK'] = self.id_medicamentoFK.toJSON()
        item['descripcion'] = self.descripcion
        item['indicacion'] = self.indicacion
        item['via_admin'] = self.via_admin
        return item

class det_solicitud_indicacion(models.Model):
    id_det_solicitud_indicacionPK = models.AutoField(primary_key=True)
    id_solicitud_laboratioFK = models.ForeignKey(SolicitudLaboratorio, on_delete=models.CASCADE)
    id_indicacionFK = models.ForeignKey(Indicacion, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField('Fecha Solicitud', blank=False,null=False)
    history = HistoricalRecords(table_name="audit_det_indic_solic")

    class Meta:
        db_table = "det_solicitud_indicacion"

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_indicacionFK'])
        item['id_solicitud_laboratioFK'] = self.id_solicitud_laboratioFK.toJSON()
        item['fecha_solicitud'] = self.fecha_solicitud
        return item