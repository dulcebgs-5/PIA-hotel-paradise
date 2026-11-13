from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import HabitacionForm
from .models import Habitacion, Reservacion


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
