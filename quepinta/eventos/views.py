from django.shortcuts import render
from .models import Evento, Reserva

def index(request):
    return render(request, 'quepinta\templates')

def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'eventos/lista_reservas.html', {'reservas': reservas})
