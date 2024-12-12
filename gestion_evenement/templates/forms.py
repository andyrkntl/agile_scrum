from django import forms
from .models import Evenement

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre_event', 'date_debut_event', 'date_fin_event', 'lieu_event', 'description_event', 'disponibilite_event']

        widgets = {
            'date_debut_event': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin_event': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
