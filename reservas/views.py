from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import HabitacionForm, ClienteForm
from .models import Habitacion, Cliente, Reservacion


def paginar(request, lista, por_pagina=3):
    paginator = Paginator(lista, por_pagina)
    page_number = request.GET.get('page')
    try:
        pagina = paginator.page(page_number)
    except PageNotAnInteger:
        pagina = paginator.page(1)
    except EmptyPage:
        pagina = paginator.page(paginator.num_pages)
    return pagina


@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.order_by('numero')
    q = request.GET.get('q')
    if q:
        if q.isdigit():
            habitaciones = habitaciones.filter(
                Q(numero=int(q)) | Q(tipo__icontains=q)
            )
        else:
            habitaciones = habitaciones.filter(tipo__icontains=q)
    pagina = paginar(request, habitaciones)
    return render(request, 'reservas/habitacion_lista.html', {
        'habitaciones': pagina,
        'total': habitaciones.count(),
        'q': q or '',
    })


@login_required
def detalle_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    return render(request, 'reservas/habitacion_detalle.html', {
        'habitacion': habitacion,
    })


@login_required
def crear_habitacion(request):
    form = HabitacionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Habitación creada correctamente.')
        return redirect('lista_habitaciones')
    return render(request, 'reservas/habitacion_formulario.html', {
        'form': form, 'titulo': 'Nueva habitación',
    })


@login_required
def editar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    form = HabitacionForm(
        request.POST or None, request.FILES or None, instance=habitacion
    )
    if form.is_valid():
        form.save()
        messages.success(request, 'Habitación actualizada correctamente.')
        return redirect('lista_habitaciones')
    return render(request, 'reservas/habitacion_formulario.html', {
        'form': form, 'titulo': 'Editar habitación',
    })


@login_required
def eliminar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    activas = habitacion.reservaciones.filter(
        estado=Reservacion.Estado.CONFIRMADA
    ).exists()
    if request.method == 'POST':
        if activas:
            messages.error(
                request,
                'No se puede eliminar: la habitación tiene reservaciones activas.'
            )
            return redirect('lista_habitaciones')
        habitacion.delete()
        messages.success(request, 'Habitación eliminada correctamente.')
        return redirect('lista_habitaciones')
    return render(request, 'reservas/habitacion_confirmar_eliminar.html', {
        'habitacion': habitacion, 'activas': activas,
    })

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.order_by('nombre')
    q = request.GET.get('q')
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q)
            | Q(apellidos__icontains=q)
            | Q(correo__icontains=q)
        )
    pagina = paginar(request, clientes)
    return render(request, 'reservas/cliente_lista.html', {
        'clientes': pagina,
        'total': clientes.count(),
        'q': q or '',
    })


@login_required
def detalle_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'reservas/cliente_detalle.html', {
        'cliente': cliente,
    })


@login_required
def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('lista_clientes')
    return render(request, 'reservas/cliente_formulario.html', {
        'form': form, 'titulo': 'Nuevo cliente',
    })


@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('lista_clientes')
    return render(request, 'reservas/cliente_formulario.html', {
        'form': form, 'titulo': 'Editar cliente',
    })


@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('lista_clientes')
    return render(request, 'reservas/cliente_confirmar_eliminar.html', {
        'cliente': cliente,
    })
