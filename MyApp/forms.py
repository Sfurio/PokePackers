from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'series', 'type', 'description', 'price', 'image']
