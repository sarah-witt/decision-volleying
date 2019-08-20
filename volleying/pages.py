from ._builtin import Page, WaitPage
from .models import Constants, MovieSelection
from .forms import MovieForm, MovieResultForm
from django.forms import modelformset_factory
import time

MovieFormset = modelformset_factory(MovieSelection, form=MovieForm, fields=('isChecked',), extra=0)
RemainingMovie = modelformset_factory(MovieSelection, form=MovieResultForm, fields=('embeddedVideo',), extra=0)

class Introduction(Page):
    def before_next_page(self):
        # user has 60 minutes to complete as many pages as possible
        if self.player.id_in_group == 1:
            self.player.isSelecting = True
        else:
            self.player.isSelecting = False

class ParticipantInfo(Page):
    template_name = 'volleying/ParticipantInfo.html'
    form_model = 'player'
    form_fields = ['first_name', 'mturkId']

    def error_message(self, values):
        if len(values["first_name"]) == 0:
            return 'Please enter your name'
        if len(values["mturkId"]) == 0:
            return 'Please enter a valid mturkId'

class WelcomeInstructions(Page):
    def before_next_page(self):
        self.player.participant.vars['expiry'] = time.time() + 120

class ChatWaitPage(WaitPage):
    template_name = 'volleying/WaitForChat.html'
    
    def after_all_players_arrive(self):
        self.is_displayed = True

class Chat(Page):
    def get_timeout_seconds(self):
        return 120

class Instructions(Page):
    pass

    def get_timeout_seconds(self):
        return 45
    
class WaitForOtherPlayer(WaitPage):
    template_name = 'volleying/WaitPage.html'

def sort_movies(movie):
    return movie.key

class Volley(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def vars_for_template(self):
        remaining_movies = self.player.group.get_remaining_movies()

        question_formset = MovieFormset(queryset=MovieSelection.objects.filter(group__exact=self.player.group).filter(isRemaining__exact=True))
        for (form, model) in zip(question_formset, remaining_movies):
            form.setLabel(model.description)

        return {
            'movie_formset': question_formset
        }
    
    def before_next_page(self):
        self.group.numberVolleys +=1
        self.player.isSelecting = False
        self.player.get_others_in_group()[0].isSelecting = True
        self.group.volley = self.group.volley + "[" + " ".join(self.group.get_remaining_movie_names()) + "] "

        all_movies = MovieSelection.objects.filter(group__exact=self.player.group)
        remaining_movies = all_movies.filter(isRemaining__exact=True)

        submitted_data = self.form.data
    
        movies_by_id = {mov.pk: mov for mov in remaining_movies}
    
        for i in range(len(remaining_movies)):
            input_prefix = 'form-%d-' % (len(remaining_movies) - i - 1)
            input_prefix1 = 'form-%d-' % i
            mov_id1 = int(submitted_data[input_prefix1 + 'id'])
            isChecked = submitted_data.get(input_prefix + 'isChecked')

            mov = movies_by_id[mov_id1]

            if isChecked:
                mov.isChecked = True

            if not self.group.eliminateNegative:
                if not mov.isChecked:
                    mov.isRemaining = False
                else: 
                    mov.isRemaining = True
                    mov.isChecked = False
            else:
                if mov.isChecked:
                    mov.isRemaining = False
                    mov.isChecked = True

            mov.save()

        if self.timeout_happened:
            self.player.get_partner().timed_out = True
            self.player.timed_out = True

    def get_timeout_seconds(self):
        return 120
    
    def error_message(self, values):
        remaining_movies = self.player.group.get_remaining_movies()
        submitted_data = self.form.data
        num_checked = 0

        for i in range(len(remaining_movies)):
            input_prefix = 'form-%d-' % i
            isChecked = submitted_data.get(input_prefix + 'isChecked')

            if isChecked:
                num_checked+=1 

        if (len(remaining_movies) == num_checked):
            return 'You cannot select every movie trailer'
        elif (num_checked == 0):
            return 'You must select at least one movie trailer'
        else:
            pass

class VolleyPlayer1(Volley):
    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 1)

class VolleyPlayer2(Volley):
    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 2)

class TrailerIntro(Page):
    timeout_seconds = 30

    def is_displayed(self):
        return not self.player.timed_out

    def before_next_page(self):
        self.player.selectedMovie = self.player.group.last_movie_name()


class Results(Page):
    def get_timeout_seconds(self):
        return 200
        
    def is_displayed(self):
        return not self.player.timed_out

    def vars_for_template(self):
        remaining_movies = self.player.group.get_remaining_movies()
        question_formset = RemainingMovie(queryset=MovieSelection.objects.filter(group__exact=self.player.group).filter(isRemaining__exact=True))

        for (form, model) in zip(question_formset, remaining_movies):
            form.generateVideoHtml(model.embeddedVideo)

        return {
            'movie_formset': question_formset
        }

class Demographics(Page):
    form_model = 'player'
    form_fields = ['satisfied', 'partner_experience', 'strategy', 'age', 'race', 'gender', 'comment']
    
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
    ChatWaitPage,
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
    VolleyPlayer2,
    WaitForOtherPlayer,
    Results,
    Demographics,
    Conclusion
]
