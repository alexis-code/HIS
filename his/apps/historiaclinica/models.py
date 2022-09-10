from django.db import models
from ..medico.models import Medico
from ..paciente.models import Paciente
from simple_history.models import HistoricalRecords

class HistoriaClinica(models.Model):
    id_historiaPK = models.AutoField(primary_key=True)
    id_medicoFK = models.ForeignKey(Medico, on_delete=models.CASCADE)
    id_pacienteFK = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_updated = models.CharField('Último en Modificar', max_length=50,blank=True,null=True,default="-")
    cod_historiaclinica = models.IntegerField('HC',unique=True, blank=False,null=False)
    fecha_ingresohospital = models.DateTimeField('Fecha de ingreso a Hospital',blank=False,null=False)
    fecha_ingresoarea = models.DateTimeField('Fecha de ingreso a Area',blank=True,null=True)
    nro_cama = models.IntegerField('Nro. de Cama',blank=False,null=False, default=0)
    grado_instruccion = models.CharField('Grado Instrucción',max_length=100, blank=False,null=False)
    proviene = models.CharField('Proviene de',max_length=100,blank=False,null=False)
    antecedente = models.CharField('Antecedentes', max_length=700,blank=False,null=False)
    historia_enfermedad_actual = models.TextField('Historia de la Enfermedad Actual',blank=False,null=False)
    tension_arterial = models.CharField('TA',max_length=30,blank=False, null=True, default='-')
    frecuencia_cardiaca = models.CharField('FC',max_length=30,blank=False, null=True, default='-')
    frecuencia_respiratoria = models.CharField('FR',max_length=30,blank=False, null=True, default='-')
    temp_ax = models.CharField('TEMP AX',max_length=30,blank=False, null=True, default='-')
    sindrome_at = models.CharField('SAT',max_length=30,blank=False, null=True, default='-')
    peso = models.CharField('Peso',max_length=50,blank=False, null=True, default='-')
    piel_mucosa = models.TextField('Piel y Mucosas',blank=False, null=True, default='-')
    neurologico = models.TextField('Neurologico',blank=False, null=True, default='-')
    cardiopulmonar = models.TextField('Cardiopulmonar',blank=False, null=True, default='-')
    abdomen = models.TextField('Abdomen',blank=False, null=True, default='-')
    genitourinario = models.TextField('Genitourinario',blank=False, null=True, default='-')
    musculoesqueletico = models.TextField('Musculoesqueletico',blank=False, null=True, default='-')
    impresion_diagnostica = models.TextField('Impresion Diagnostica',blank=False,null=False)
    estado = models.CharField('Estado', max_length=10,blank=False, null=False,default="Activo")
    history = HistoricalRecords(table_name = 'audit_hc')

    def __str__(self):
        return str(self.cod_historiaclinica)

    class Meta:
        ordering = ['-id_historiaPK']
        verbose_name = 'HistoriaClinica'
        verbose_name_plural = 'HistoriaClinicas'
        db_table = 'tb_historiaclinica'