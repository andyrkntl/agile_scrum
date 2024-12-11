from django.contrib import admin
from .models import Compte, Personne, Evenement, Discuter, Participer, Notifier

admin.site.register(Compte)
admin.site.register(Personne)
admin.site.register(Evenement)
admin.site.register(Discuter)
admin.site.register(Participer)
admin.site.register(Notifier)
