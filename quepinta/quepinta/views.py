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
from .models import Reserva, Evento, Estado, Promocion

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages



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
    fields = ['nombre', 'descripcion', 'fecha_evento', 'cantidad_entradas_disponibles', 'organizacion', 'precio', 'tipo_entrada', 'entradas_promocion']
    template_name = 'eventos/crear.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# Logica de requerimento de inicio sesion para reservar eventos
@login_required
def reservar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    promociones = Promocion.objects.all()

    if request.method == 'POST':
        estado_reservado = Estado.objects.get(nombre='Reservado')
        cantidad = int(request.POST.get('cantidad', 0))
        precio_entrada = evento.precio
        promocion_id = request.POST.get('promocion')
        promocion = Promocion.objects.get(id=promocion_id) if promocion_id else None
        descuento = Decimal(0)

        # Aplicar descuento si el número de entradas cumple con la promoción
        if promocion and cantidad >= evento.entradas_promocion:
            descuento = Decimal(promocion.descuento)
            precio_total = (precio_entrada * Decimal(cantidad)) * (Decimal(1) - descuento / Decimal(100))
        else:
            precio_total = precio_entrada * Decimal(cantidad)

        if evento.cantidad_entradas_disponibles >= cantidad:
            reserva = Reserva.objects.create(
                usuario=request.user,
                entrada=evento,
                estado=estado_reservado,
                cantidad=cantidad,
                promocion=promocion,
                fecha_reserva=timezone.now().date()
            )

            evento.cantidad_entradas_disponibles -= cantidad
            evento.save()

            messages.success(request, f"¡Reserva confirmada! Precio final: {precio_total}")
            return redirect('lista_eventos')
        else:
            messages.error(request, 'No hay suficientes entradas disponibles.')

    return render(request, 'eventos/reservar.html', {'evento': evento, 'promociones': promociones})

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