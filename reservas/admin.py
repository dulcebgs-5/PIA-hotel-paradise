from django.contrib import admin
from .models import Habitacion, Cliente

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'precio_noche', 'capacidad', 'disponible']
    list_filter = ['tipo', 'disponible']
    search_fields = ['numero', 'tipo']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'correo', 'telefono', 'fecha_registro']
    search_fields = ['nombre', 'apellidos', 'correo']
