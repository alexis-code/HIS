from django.contrib.auth.models import UserManager
from django.test import TestCase
from .models import Medico

class MedicoTestCase(TestCase):
    def setUp(self):
        Medico.objects.create(
            username='afrodriguez',
            first_name='Alexis',
            last_name='Rodriguez Villarroel',
            email='alexir325@gmail.com',
            password1='admin1213',
            password2='admin1213'
            )