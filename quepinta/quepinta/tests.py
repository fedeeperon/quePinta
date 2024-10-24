from django.test import TestCase
from quepinta.forms import EventoForm

class EventoFormTest(TestCase):
    def test_evento_form_cantidad_entradas_negativa(self):
        # Test de ejemplo
        form_data = {
            'nombre': 'Concierto de prueba',
            'descripcion': 'Un concierto',
            'fecha_evento': '2024-12-10',
            'cantidad_entradas_disponibles': -10,
            'precio': 50.00,
            'organizacion': 'Organización X',
            'tipo_entrada': 'General',
            'entradas_promocion': 5,
            'promocion': '3x1',
        }
        form = EventoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_entradas_disponibles', form.errors)
