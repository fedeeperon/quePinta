from django.db import models
from django.contrib.auth.models import User


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
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

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

# Modelo TipoEntrada
class TipoEntrada(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo Evento

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_evento = models.DateField()
    cantidad_entradas_disponibles = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    organizacion = models.CharField(max_length=100)
    tipo_entrada = models.CharField(max_length=100, blank=False)
    entradas_promocion = models.PositiveIntegerField(blank=False)

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
    no_reserva = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    evento = models.ForeignKey('Evento', on_delete=models.PROTECT, null=True, default=None)  # Modificado
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    promocion = models.ForeignKey('Promocion', on_delete=models.PROTECT, null=True, blank=True)
    fecha_reserva = models.DateField()

    def __str__(self):
        return self.no_reserva

    def save(self, *args, **kwargs):
        if not self.no_reserva:
            self.no_reserva = f"R{self.fecha_reserva.strftime('%Y%m%d')}-{Reserva.objects.count() + 1:04d}"
        super().save(*args, **kwargs)