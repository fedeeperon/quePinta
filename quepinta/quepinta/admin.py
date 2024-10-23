from django.contrib import admin
from .models import Evento, Reserva, Usuario, Organizacion, Promocion, Estado, TipoEntrada, Entrada

admin.site.register(Evento)
admin.site.register(Reserva)
admin.site.register(Usuario)
admin.site.register(Organizacion)
admin.site.register(Promocion)
admin.site.register(Estado)
admin.site.register(TipoEntrada)
admin.site.register(Entrada)