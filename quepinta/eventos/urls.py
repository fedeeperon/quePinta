from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
]
