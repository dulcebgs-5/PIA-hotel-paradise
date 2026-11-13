from django import forms
from .models import Habitacion, Cliente


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
