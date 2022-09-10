# Generated by Django 3.2.4 on 2021-11-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoCie',
            fields=[
                ('id_codigo', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_cie', models.CharField(max_length=20, verbose_name='Código CIE-10')),
                ('diagnostico', models.TextField(verbose_name='Diagnóstico')),
                ('estado', models.CharField(default='Activo', max_length=10, verbose_name='Estado')),
            ],
            options={
                'ordering': ['-id_codigo'],
            },
        ),
    ]