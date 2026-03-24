from django.contrib import admin
from .models import Laboratorio, Usuario # Aquí decía UsuarioDocente, cámbialo a Usuario

admin.site.register(Laboratorio)
admin.site.register(Usuario)