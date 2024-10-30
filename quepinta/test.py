from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserLoginTest(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)  # Verificar redirección después del login

    def test_login_view_invalid(self):
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpass'})
        self.assertContains(response, "Por favor, verifica los datos.")
    
'''

pip install virtualenv # Instalar virtualenv
virtualenv venv # Crear un entorno virtual
source venv/bin/activate # Activar el entorno virtual
pip install django  # Instalar Django

'''

'''
python manage.py test # Ejecutar pruebas
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
'''