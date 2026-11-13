from django import forms
from .models import Habitacion, Cliente, Reservacion


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if Habitacion.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'Ya existe una habitación con ese número.'
            )
        return numero

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'correo', 'telefono']

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Cliente.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ese correo ya está registrado.')
        return correo

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = [
            'cliente', 'habitacion', 'fecha_entrada',
            'fecha_salida', 'total', 'estado',
        ]
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        data = super().clean()
        entrada = data.get('fecha_entrada')
        salida = data.get('fecha_salida')
        habitacion = data.get('habitacion')
        total = data.get('total')

        if entrada and salida:
            if salida <= entrada:
                raise forms.ValidationError(
                    'La fecha de salida debe ser mayor que la fecha de entrada.'
                )

        if habitacion and entrada and salida:
            choque = Reservacion.objects.filter(
                habitacion=habitacion,
                estado=Reservacion.Estado.CONFIRMADA,
                fecha_entrada__lt=salida,
                fecha_salida__gt=entrada,
            ).exclude(pk=self.instance.pk)
            if choque.exists():
                raise forms.ValidationError(
                    'Esa habitación ya está reservada en esas fechas. '
                    'Elige otras fechas u otra habitación.'
                )

        if habitacion and entrada and salida and total is not None:
            noches = (salida - entrada).days
            esperado = habitacion.precio_noche * noches
            if total != esperado:
                raise forms.ValidationError(
                    f'El total debe ser ${esperado} '
                    f'(${habitacion.precio_noche} por noche x {noches} noches).'
                )
        return data
