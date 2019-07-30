from .models import MovieSelection, Group, Player, Constants
from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet, CheckboxInput
from django import forms
from django.db import models
from django.forms import ModelForm

class MovieForm(ModelForm):
    class Meta:
        model = MovieSelection
        fields = ['movie_isChecked']
        widgets = {
            'movie_isChecked': CheckboxInput()
        }
        
    def setLabel(self, label):
        self.fields['movie_isChecked'].label = label