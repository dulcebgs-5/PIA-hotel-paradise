from django.urls import path
from . import views

urlpatterns = [
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/nueva/', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones/<int:id>/', views.detalle_habitacion, name='detalle_habitacion'),
    path('habitaciones/<int:id>/editar/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/<int:id>/eliminar/', views.eliminar_habitacion, name='eliminar_habitacion'),

    
]
