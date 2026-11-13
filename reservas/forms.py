from django import forms
from .models import Habitacion


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
