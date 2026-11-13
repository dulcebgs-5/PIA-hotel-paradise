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

class Reservacion(models.Model):
    class Estado(models.TextChoices):
        CONFIRMADA = 'confirmada', 'Confirmada'
        CANCELADA = 'cancelada', 'Cancelada'

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='reservaciones'
    )
    habitacion = models.ForeignKey(
        Habitacion, on_delete=models.CASCADE, related_name='reservaciones'
    )
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.CONFIRMADA
    )

    def __str__(self):
        return (
            f"Reservación {self.id}: {self.cliente} - "
            f"Habitación {self.habitacion.numero}"
        )

    def get_absolute_url(self):
        return reverse('detalle_reservacion', args=[self.id])

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.fecha_entrada and self.fecha_salida:
            if self.fecha_salida <= self.fecha_entrada:
                raise ValidationError(
                    'La fecha de salida debe ser mayor que la fecha de entrada.'
                )
        if self.habitacion_id and self.fecha_entrada and self.fecha_salida:
            choque = Reservacion.objects.filter(
                habitacion=self.habitacion,
                estado=self.Estado.CONFIRMADA,
                fecha_entrada__lt=self.fecha_salida,
                fecha_salida__gt=self.fecha_entrada,
            ).exclude(pk=self.pk)
            if choque.exists():
                raise ValidationError(
                    'Esa habitación ya está reservada en esas fechas.'
                )
