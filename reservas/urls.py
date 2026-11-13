from django.urls import path
from . import views

urlpatterns = [
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/nueva/', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones/<int:id>/', views.detalle_habitacion, name='detalle_habitacion'),
    path('habitaciones/<int:id>/editar/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/<int:id>/eliminar/', views.eliminar_habitacion, name='eliminar_habitacion'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
path('clientes/<int:id>/', views.detalle_cliente, name='detalle_cliente'),
path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
path('clientes/<int:id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    path('reservaciones/', views.lista_reservaciones, name='lista_reservaciones'),
    path('reservaciones/nueva/', views.crear_reservacion, name='crear_reservacion'),
    path('reservaciones/<int:id>/', views.detalle_reservacion, name='detalle_reservacion'),
    path('reservaciones/<int:id>/editar/', views.editar_reservacion, name='editar_reservacion'),
    path('reservaciones/<int:id>/cancelar/', views.cancelar_reservacion, name='cancelar_reservacion'),


]
