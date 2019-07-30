from .models import MovieSelection, Group, Player, Constants
from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet, CheckboxInput, ModelForm
from django.db import models



class MovieForm(ModelForm):
    class Meta:
        model = MovieSelection
        fields = ['movie_isChecked']
        widgets = {
            'movie_isChecked': CheckboxInput()
        }
        
    def setLabel(self, label):
        self.fields['movie_isChecked'].label = label
