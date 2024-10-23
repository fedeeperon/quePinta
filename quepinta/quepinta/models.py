from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Clase abstracta para reutilización de los campos comunes
class UsuarioBase(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    estado = models.BooleanField(default=True)

    class Meta:
        abstract = True

# Modelo Usuario que extiende de la clase abstracta UsuarioBase
class Usuario(UsuarioBase):
    dni = models.CharField(max_length=20, unique=True)
    edad = models.IntegerField()
    localidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Estado para manejar los diferentes estados de una reserva, evento, etc.
class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo Promoción
class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo Organizaciones
class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)
    dueño = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    purchase_parking_pass = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

# Modelo Evento
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_evento = models.DateField()
    cantidad_entradas_disponibles = models.IntegerField()
    organizacion = models.ForeignKey(Organizacion, on_delete=models.PROTECT)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    

    def __str__(self):
        return self.nombre

# Modelo TipoEntrada
class TipoEntrada(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo Entrada
class Entrada(models.Model):
    no_entrada = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    hora = models.TimeField()
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT)

    def __str__(self):
        return self.no_entrada

# Modelo Reserva
class Reserva(models.Model):
    fecha_reserva = models.DateField()
    no_reserva = models.CharField(max_length=100, unique=True)
    entrada = models.ForeignKey(Entrada, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    promocion = models.ForeignKey(Promocion, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.no_reserva
