from django import forms
from .models import Evento, TipoEntrada, Promocion, Organizacion


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_evento', 'cantidad_entradas_disponibles', 'precio', 'promocion', 'organizacion', 'tipo_entrada', 'entradas_promocion']
        widgets = {
                'fecha_evento': forms.DateInput(attrs={
                    'type': 'date',  # Usa un input HTML tipo date
                    'class': 'form-control',
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_entrada'].required = False
        self.fields['entradas_promocion'].required = False
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            
        }

class TipoEntradaForm(forms.ModelForm):
    class Meta:
        model = TipoEntrada
        fields = ['nombre', 'precio']

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'descuento', 'cantidad_minima_entradas']
        

