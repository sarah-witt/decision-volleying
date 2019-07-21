from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import Constants
import re
import time
import random


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

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        self.player.isSelecting = False
        self.player.get_others_in_group()[0].isSelecting = True
        self.group.numberVolleys +=1
        self.group.volley = self.group.volley + " ".join(self.group.get_remaining_movies())
        if self.timeout_happened:
            self.player.get_partner().timed_out = True
            self.player.timed_out = True

    def get_timeout_seconds(self):
        return 60

    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 1)

class VolleyPlayer2(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        self.player.isSelecting = False
        self.player.get_others_in_group()[0].isSelecting = True
        self.group.numberVolleys +=1
        self.group.volley = self.group.volley + " [" +  " ".join(self.group.get_remaining_movies()) + "]"
        if self.timeout_happened:
            self.player.get_partner().timed_out = True
            self.player.timed_out = True

    def get_timeout_seconds(self):
        return 60

    def is_displayed(self):
        return (not self.player.timed_out) and self.group.volleying() and (self.player.id_in_group == 2)


class Results(Page):

    def is_displayed(self):
        return not self.player.timed_out

    def before_next_page(self):
        self.player.selectedMovie = self.player.group.last_movie()
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
