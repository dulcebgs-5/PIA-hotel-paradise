from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import HabitacionForm, ClienteForm, ReservacionForm, UserRegistrationForm
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
@login_required
def lista_reservaciones(request):
    reservaciones = Reservacion.objects.order_by('-fecha_entrada')
    q = request.GET.get('q')
    if q:
        reservaciones = reservaciones.filter(
            Q(cliente__nombre__icontains=q)
            | Q(cliente__apellidos__icontains=q)
        )
    pagina = paginar(request, reservaciones)
    return render(request, 'reservas/reservacion_lista.html', {
        'reservaciones': pagina,
        'total': reservaciones.count(),
        'q': q or '',
    })


@login_required
def detalle_reservacion(request, id):
    reservacion = get_object_or_404(Reservacion, id=id)
    return render(request, 'reservas/reservacion_detalle.html', {
        'reservacion': reservacion,
    })


@login_required
def crear_reservacion(request):
    form = ReservacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Reservación creada correctamente.')
        return redirect('lista_reservaciones')
    return render(request, 'reservas/reservacion_formulario.html', {
        'form': form, 'titulo': 'Nueva reservación',
    })


@login_required
def editar_reservacion(request, id):
    reservacion = get_object_or_404(Reservacion, id=id)
    form = ReservacionForm(request.POST or None, instance=reservacion)
    if form.is_valid():
        form.save()
        messages.success(request, 'Reservación actualizada correctamente.')
        return redirect('lista_reservaciones')
    return render(request, 'reservas/reservacion_formulario.html', {
        'form': form, 'titulo': 'Editar reservación',
    })


@login_required
def cancelar_reservacion(request, id):
    reservacion = get_object_or_404(Reservacion, id=id)
    if request.method == 'POST':
        reservacion.estado = Reservacion.Estado.CANCELADA
        reservacion.save()
        messages.success(request, 'Reservación cancelada correctamente.')
        return redirect('lista_reservaciones')
    return render(request, 'reservas/reservacion_confirmar_cancelar.html', {
        'reservacion': reservacion,
    })

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_habitaciones = Habitacion.objects.count()
    total_reservaciones = Reservacion.objects.count()
    disponibles = Habitacion.objects.filter(disponible=True).count()
    ingresos = Reservacion.objects.filter(
        estado=Reservacion.Estado.CONFIRMADA
    ).aggregate(total=Sum('total'))['total'] or 0
    ultimas = Reservacion.objects.order_by('-id')[:5]

    return render(request, 'reservas/dashboard.html', {
        'total_clientes': total_clientes,
        'total_habitaciones': total_habitaciones,
        'total_reservaciones': total_reservaciones,
        'disponibles': disponibles,
        'ingresos': ingresos,
        'ultimas': ultimas,
    })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'reservas/register_done.html', {
                'new_user': new_user,
            })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'reservas/register.html', {
        'user_form': user_form,
    })
