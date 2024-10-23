from django.shortcuts import render
from .models import Evento, Reserva

from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse

def index(request):
    return render(request, 'service.html')

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Reserva, Evento, Estado

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


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
    



#vista de registro para que los usuarios puedan registrarse.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('index')  # Asegúrate de tener una URL con el nombre 'index'
        else:
            messages.error(request, 'Error en el registro. Por favor, verifica los datos.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'login.html', {'login_form': login_form, 'register_form': register_form})

# Eventos disponibles

class EventListView(ListView):
    model = Evento
    template_name = 'eventos.html'
    context_object_name = 'eventos'
    
    
    
# Vista para crear eventos
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    fields = ['nombre', 'descripcion', 'fecha_evento', 'cantidad_entradas_disponibles', 'organizacion']
    template_name = 'eventos/crear.html'
    success_url = reverse_lazy('lista_eventos')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

# Logica de requerimento de inicio sesion para reservar eventos
@login_required
def reservar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        estado_reservado = Estado.objects.get(nombre='Reservado')
        cantidad = int(request.POST.get('cantidad', 0))

        if evento.cantidad_entradas_disponibles >= cantidad:
            reserva = Reserva.objects.create(
                usuario=request.user,
                evento=evento,
                estado=estado_reservado,
                cantidad=cantidad,
                fecha_reserva=timezone.now().date()
            )
            evento.cantidad_entradas_disponibles -= cantidad
            evento.save()
            return redirect('lista_eventos')
        else:
            return render(request, 'error.html', {'mensaje': 'No hay suficientes entradas disponibles.'})
    
    return render(request, 'eventos/reservar.html', {'evento_id': evento_id})
    

    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_eventos')  # Cambia 'lista_eventos' según la página a la que quieras redirigir después del login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'register_url': reverse('register')})