from django.db import models
from simple_history.models import HistoricalRecords

class ExamenFisico(models.Model):
    id_examenfisicoPK = models.AutoField(primary_key=True)
    tension_arterial = models.CharField('TA',max_length=15,default="-",blank=True,null=True)
    frecuencia_cardiaca = models.FloatField('FC',default=0.00,blank=True, null=True)
    frecuencia_respiratoria = models.DecimalField('FR',max_digits=15,decimal_places=2,default=0.00,blank=True, null=True)
    temp_ax = models.DecimalField('TEMP AX',max_digits=15,decimal_places=2,blank=True, null=True)
    sindrome_at = models.DecimalField('SAT',max_digits=15,decimal_places=2,default=0.00,blank=True, null=True)
    pao = models.DecimalField('PAO-2',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    fio = models.DecimalField('FIO-2',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    pao_fio = models.DecimalField('PAO2/FIO2',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    pas = models.DecimalField('PAS',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    pad = models.DecimalField('PAD',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    pam = models.DecimalField('PAM',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    avm = models.DecimalField('AVM',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    modo = models.DecimalField('MODO',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    noradrenalina = models.CharField('Noradrenalina',max_length=30,blank=True,null=True, default='-')
    atracurio = models.CharField('Atracurio',max_length=30,blank=True,null=True, default='-')
    vc = models.DecimalField('VC',max_digits=15,decimal_places=2,default=0.00,blank=True,null=True)
    peep = models.DecimalField('PEEP',blank=True,null=True, max_digits=15,decimal_places=2,default=0.00,)
    prono_dias = models.CharField('Prono Días',max_length=15,blank=True,null=True, default='-')
    pi = models.DecimalField('PI',blank=True,null=True, max_digits=15,decimal_places=2,default=0.00,)
    peso = models.DecimalField('Peso',blank=True, null=True, max_digits=15,decimal_places=2,default=0.00,)
    piel_mucosa = models.TextField('Piel y Mucosas',blank=True, null=True, default='-')
    neurologico = models.TextField('Neurologico',blank=True, null=True, default='-')
    cardiopulmonar = models.TextField('Cardiopulmonar',blank=True, null=True, default='-')
    abdomen = models.TextField('Abdomen',blank=True, null=True, default='-')
    genitourinario = models.TextField('Genitourinario',blank=True, null=True, default='-')
    musculoesqueletico = models.TextField('Musculoesqueletico',blank=True, null=True, default='-')
    history = HistoricalRecords(table_name = "audit_examen_fisico")

    class Meta:
        verbose_name = 'ExamenFisico'
        verbose_name_plural = 'ExamenFisicos'
        db_table = 'tb_examenfisico'