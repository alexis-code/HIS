from .base import *
from decouple import config
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
DB_NAME = config("NAME_DBPRUEBA")
DB_PASS = config("PSSWD_DBPRUEBA")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': 'root',
        'PASSWORD': DB_PASS,
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}