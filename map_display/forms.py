from django import forms
from .models import MapDisplay


class Display_form(forms.ModelForm):
    class Meta:
        model = MapDisplay
        fields = ('airline_icao',)