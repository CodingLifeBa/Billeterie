from django import forms
from .models import Evenement

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'description', 'date', 'location', 'prix_ticket','thumbnail']