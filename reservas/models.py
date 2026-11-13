from django.db import models
from django.urls import reverse

class Habitacion(models.Model):
    class Tipo(models.TextChoices):
        INDIVIDUAL = 'Individual', 'Individual'
        DOBLE = 'Doble', 'Doble'
        SUITE = 'Suite', 'Suite'
        PRESIDENCIAL = 'Presidencial', 'Presidencial'

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='habitaciones/', blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"

    def get_absolute_url(self):
        return reverse('detalle_habitacion', args=[self.id])

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def get_absolute_url(self):
        return reverse('detalle_cliente', args=[self.id])
