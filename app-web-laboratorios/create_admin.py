import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_laboratorios.settings')
django.setup()

from django.contrib.auth.models import User

# Configura aquí tus datos
username = 'admin_leo'
email = 'tu_correo@ejemplo.com'
password = 'TuPasswordSegura123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superusuario '{username}' creado con éxito.")
else:
    print(f"El usuario '{username}' ya existe.")