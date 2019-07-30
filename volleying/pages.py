from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, MovieSelection
from .forms import MovieForm
import re
import time
import random
from django.forms import modelformset_factory
from django.forms import CheckboxInput

MovieFormset = modelformset_factory(MovieSelection, form=MovieForm, fields=('movie_isChecked',),
widgets={'movie_isChecked': CheckboxInput}, extra=0)

class Introduction(Page):
    def before_next_page(self):
        # user has 60 minutes to complete as many pages as possible
        if self.player.id_in_group == 1:
            self.player.isSelecting = True
        else:
            self.player.isSelecting = False
        
        self.participant.vars['expiry'] = time.time() + 3600

class ParticipantInfo(Page):
    template_name = 'volleying/ParticipantInfo.html'
    form_model = 'player'
    form_fields = ['first_name', 'mturkId']

    def error_message(self, values):
        if values["first_name"] == '':
            return 'Please enter your name'
        if values["mturkId"] == '':
            return 'Please enter a valid mturkId'

class WelcomeInstructions(Page):
    pass

class Chat(Page):
    def get_timeout_seconds(self):
        return 60

class Instructions(Page):
    pass
    
class WaitForOtherPlayer(WaitPage):
    template_name = 'volleying/WaitPage.html'

class VolleyPlayer1(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def vars_for_template(self):
        remaining_movies = self.player.group.get_remaining_movies()

        question_formset = MovieFormset(queryset=remaining_movies)
        for (form, model) in zip(question_formset, remaining_movies):
            form.setLabel(model.movie_description)

        return {
            'movie_formset': question_formset,
            'movie_values_and_forms': zip([mov.movie_isChecked for mov in remaining_movies], question_formset.forms),

        }
    
    def before_next_page(self):
        all_movies = MovieSelection.objects.filter(group__exact=self.player.group)
        remaining_movies = all_movies.filter(movie_isRemaining__exact=True)

        submitted_data = self.form.data
        print(submitted_data)

        movies_by_id = {mov.pk: mov for mov in self.player.group.movieselection_set.all()}


        for i in range(len(remaining_movies)):
            input_prefix = 'form-%d-' % i
            mov_id = int(submitted_data[input_prefix + 'id'])
            isChecked = submitted_data.get(input_prefix + 'movie_isChecked')

            mov = movies_by_id[mov_id]

            print(isChecked)
            if isChecked:
                mov.movie_isChecked = True

            if not self.group.eliminateNegative:
                if not mov.movie_isChecked:
                    mov.movie_isRemaining = False
                else: 
                    mov.movie_isRemaining = True
                    mov.movie_isChecked = False
            else:
                if mov.movie_isChecked:
                    mov.movie_isRemaining = False
                    mov.movie_isChecked = True

            mov.save()

    def get_timeout_seconds(self):
        return 60

    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 1)

class VolleyPlayer2(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def vars_for_template(self):
        remaining_movies = self.player.group.get_remaining_movies()

        question_formset = MovieFormset(queryset=remaining_movies)
        for (form, model) in zip(question_formset, remaining_movies):
            form.setLabel(model.movie_description)

        return {
            'movie_formset': question_formset,
            'movie_values_and_forms': zip([mov.movie_isChecked for mov in remaining_movies], question_formset.forms),

        }
    
    def before_next_page(self):
        all_movies = MovieSelection.objects.filter(group__exact=self.player.group)
        remaining_movies = all_movies.filter(movie_isRemaining__exact=True)

        submitted_data = self.form.data
        print(submitted_data)

        movies_by_id = {mov.pk: mov for mov in self.player.group.movieselection_set.all()}


        for i in range(len(remaining_movies)):
            input_prefix = 'form-%d-' % i
            mov_id = int(submitted_data[input_prefix + 'id'])
            isChecked = submitted_data.get(input_prefix + 'movie_isChecked')

            mov = movies_by_id[mov_id]

            if isChecked:
                mov.movie_isChecked = True

            if not self.group.eliminateNegative:
                if not mov.movie_isChecked:
                    mov.movie_isRemaining = False
                mov.movie_isChecked = False
            else:
                if not mov.movie_isChecked:
                    mov.movie_isRemaining = True
                else: 
                    mov.movie_isRemaining = False
                    mov.movie_isChecked = True

            mov.save()
            
    def get_timeout_seconds(self):
        return 60

    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 2)

class Results(Page):

    def is_displayed(self):
        return not self.player.timed_out

    def before_next_page(self):
        self.player.selectedMovie = self.player.group.last_movie_name()
        if self.timeout_happened:
            self.player.timed_out = True

    def get_timeout_seconds(self):
        return 200

class Demographics(Page):
    form_model = 'player'
    form_fields = ['satisfied', 'partner_experience', 'age', 'race', 'gender', 'comment']
    
    def is_displayed(self):
        return not self.player.timed_out

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timed_out = True

class Conclusion(Page):
    pass


page_sequence = [
    Introduction,
    ParticipantInfo,
    WelcomeInstructions,
    Chat,
    Instructions,
    VolleyPlayer1,
    WaitForOtherPlayer,
    VolleyPlayer2,
    WaitForOtherPlayer,
    VolleyPlayer1,
    WaitForOtherPlayer,
    VolleyPlayer2,
    WaitForOtherPlayer,
    VolleyPlayer1,
    WaitForOtherPlayer,
    VolleyPlayer2,
    WaitForOtherPlayer,
    VolleyPlayer1,
    WaitForOtherPlayer,
    VolleyPlayer1,
    WaitForOtherPlayer,
    VolleyPlayer2,
    WaitForOtherPlayer,
    VolleyPlayer2,
    WaitForOtherPlayer,
    VolleyPlayer1,
    WaitForOtherPlayer,
    Results,
    Demographics,
    Conclusion
]
