from django.db import models
from django.forms.models import model_to_dict
from simple_history.models import HistoricalRecords

class Paciente(models.Model):
    id_pacientePK = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombres',max_length=150,blank=False,null=False)
    apellido_paterno = models.CharField('Apellido Paterno',max_length=250,blank=False,null=False)
    apellido_materno = models.CharField('Apellido Materno',max_length=150,blank=False,null=False)
    nro_documento = models.IntegerField('Nro de Documento',unique=True, blank=False,null=False)
    complementario_ci = models.CharField('Complement Ci',max_length=20,blank=False,null=False, default="-")
    sexo = models.CharField('Sexo',max_length=2,blank=False,null=False)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=False,null=False)
    edad = models.IntegerField('Edad',blank=False,null=False)
    ocupacion = models.CharField('Ocupación',max_length=150,blank=True,null=True)
    estado_civil = models.CharField('Estado Civil',max_length=100,blank=True,null=True)
    residencia = models.CharField('Residencia',max_length=150,blank=False,null=False)
    procedencia = models.CharField('Procedencia',max_length=150,blank=False,null=False)
    domicilio = models.TextField('Domicilio',max_length=600,blank=True,null=True)
    telefono = models.IntegerField('Telefono', blank=True, null=True)
    nombre_referencia = models.CharField('Nombre Referencia', max_length=300, blank=True, null=True)
    telefono_referencia = models.IntegerField('Telefono Referencia', blank=True, null=True)
    vacuna_covid = models.CharField('Vacuna - Covid 19',max_length=30,blank=False,null=False,default="No")
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    history = HistoricalRecords(table_name="audit_paciente")

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        db_table = 'tb_paciente'
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nro_documento'] = self.nro_documento
        return item
