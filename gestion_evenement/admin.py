from django.contrib import admin
from .models import Personne, Evenement

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('nom_prs', 'prenom_prs', 'email_prs', 'role_pers')
    search_fields = ('nom_prs', 'email_prs')

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre_event', 'date_debut_event', 'date_fin_event', 'lieu_event')
    list_filter = ('date_debut_event', 'lieu_event')
    search_fields = ('titre_event', 'lieu_event')
