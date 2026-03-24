from django.db import models

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50)
    password = models.CharField(max_length=255) 

    def __str__(self):
        return self.nombre

class RegistroBitacora(models.Model):
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    carrera = models.CharField(max_length=100)
    cuatrimestre = models.CharField(max_length=50)
    grado_grupo = models.CharField(max_length=20)
    anio = models.IntegerField(default=2026)
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    equipo = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.docente.nombre}"