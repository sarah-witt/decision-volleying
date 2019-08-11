from .models import MovieSelection, Group, Player, Constants
from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet, CheckboxInput, ModelForm
from django.db import models



class MovieForm(ModelForm):
    class Meta:
        model = MovieSelection
        fields = ['isChecked']
        widgets = {
            'isChecked': CheckboxInput()
        }
        
    def setLabel(self, label):
        self.fields['isChecked'].label = label
        self.fields['isChecked'].label_suffix = ''
