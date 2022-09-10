from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin


class MedicoManager(BaseUserManager):

    def create_user(self,username,first_name,last_name,email,password=None,**other_fields):
        if not email:
            raise ValueError('Debes ingresar un email')

        email = self.normalize_email(email)
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,first_name,last_name,email,password=None,**other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(username,first_name,last_name,email,password,**other_fields)

class Medico(AbstractBaseUser,PermissionsMixin):
    id_medicoPK = models.AutoField(primary_key=True)
    username = models.CharField('Nombre de Usuario', unique=True,max_length=100)
    first_name = models.CharField('Nombres',max_length=200, blank=True,null=True)
    last_name = models.CharField('Apellidos',max_length=200, blank=True,null=True)
    email = models.EmailField('Correo Electrónico', unique=True,max_length=254)
    nro_registro = models.IntegerField('Número de Registro',null=True,blank=True,unique=True)
    nro_documento = models.IntegerField('Nro. Documento',null=True,blank=True,unique=True)
    complemento = models.CharField('Complemento',max_length=5,null=True,blank=True)
    especialidad = models.CharField('Especialidad',max_length = 200,null=True,blank=True)
    nro_telefono = models.IntegerField('Número de Teléfono',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = MedicoManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
        return self.username