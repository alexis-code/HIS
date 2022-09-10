from django.db import models
from simple_history.models import HistoricalRecords

class ResultadoLab(models.Model):
    id_resultadolabPK = models.AutoField(primary_key=True)
    lab_gb = models.DecimalField('GB',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_hb = models.DecimalField('HB',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_ph = models.DecimalField('PH',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_got = models.DecimalField('GOT',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_neu = models.DecimalField('NEU',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_htco = models.DecimalField('HTCO',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_pco = models.DecimalField('PCO2',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_gpt = models.DecimalField('GPT',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_lin = models.DecimalField('LIN',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_cr = models.DecimalField('CR',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_hco = models.DecimalField('HCO3',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_pt = models.DecimalField('PT',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_cay = models.DecimalField('CAY',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_urea = models.DecimalField('UREA',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_alb = models.DecimalField('ALB',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_po = models.DecimalField('PO2',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_plq = models.DecimalField('PLQ',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_na = models.DecimalField('NA',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_eb = models.DecimalField('EB',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_cl = models.DecimalField('CL',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_k = models.DecimalField('K',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_lact = models.DecimalField('LACT',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    lab_dd = models.DecimalField('DD',max_digits=15,decimal_places=2,default=0.00,blank=False,null=False)
    history = HistoricalRecords(table_name="audit_result_lab")

    class Meta:
        verbose_name = 'Resultadolab'
        verbose_name_plural = 'Resultadolabs'
        db_table = 'tb_resultadolab'
