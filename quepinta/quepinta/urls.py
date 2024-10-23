"""
URL configuration for quepinta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Import the views module
from .views import register, EventListView, EventCreateView, reservar_evento  # Import views
from django.contrib.auth import views as auth_views  # Import auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('reservas/', views.ReservaListView.as_view(), name='lista_reservas'),
    path('reservas/<int:reserva_id>/', views.ReservaDetailView.as_view(), name='detalle_reserva'),
    path('reservas/crear/', views.CrearReservaView.as_view(), name='crear_reserva'),

    path('eventos/', EventListView.as_view(), name='lista_eventos'),
    path('eventos/crear/', EventCreateView.as_view(), name='crear_evento'),
    path('eventos/reservar/<int:evento_id>/', reservar_evento, name='reservar_evento'),
]
