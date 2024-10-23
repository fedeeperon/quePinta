from django.shortcuts import render
from .models import Evento, Reserva

from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

def index(request):
    return render(request, 'service.html')

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Reserva, Evento, Estado

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


class ReservaListView(View):
    def get(self, request):
        reservas = Reserva.objects.all()
        return render(request, 'list.html', {'reservas': reservas})

class ReservaDetailView(View):
    def get(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        return render(request, 'detail.html', {'reserva': reserva})

class CrearReservaView(View):
    def get(self, request):
        # Mostrar formulario para crear una nueva reserva
        return render(request, 'create.html')
    
def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'lista_eventos.html', {'eventos': eventos})

def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'lista_reservas.html', {'reservas': reservas})



#vista de registro para que los usuarios puedan registrarse.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# Eventos disponibles

class EventListView(ListView):
    model = Evento
    template_name = 'lista.html'
    context_object_name = 'eventos'
    
    
    
# Vista para crear eventos
class EventCreateView(CreateView):
    model = Evento
    fields = ['fecha_evento', 'nombre', 'descripcion', 'cantidad_entradas_disponible']
    template_name = 'eventos/crear.html'
    success_url = reverse_lazy('lista_eventos')
    
    
    
# Logica de requwrimento de inicio sesion para reservar eventos
@login_required
def reservar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    estado_reservado = Estado.objects.get(nombre='Reservado')  # Asegúrate de tener este estado en la base de datos
    cantidad = request.POST.get('cantidad')

    # Lógica para verificar disponibilidad
    if evento.cantidad_entradas_disponible >= int(cantidad):
        reserva = Reserva.objects.create(
            usuario=request.user,
            evento=evento,
            estado=estado_reservado,
            cantidad=cantidad
        )
        # Reducir la cantidad de entradas disponibles
        evento.cantidad_entradas_disponible -= int(cantidad)
        evento.save()
        return redirect('lista_eventos')
    else:
        # Manejar el caso cuando no hay suficientes entradas
        return render(request, 'error.html', {'mensaje': 'No hay suficientes entradas disponibles.'})