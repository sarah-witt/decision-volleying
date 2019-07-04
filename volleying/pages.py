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
    form_fields = ['first_name', 'sonaId']

    def error_message(self, values):
        if values["first_name"] == '':
            return 'Please enter your name'
        if values["sonaId"] == '':
            return 'Please enter a valid sonaId'

class Instructions(Page):
    pass

class Chat(Page):
    def get_timeout_seconds(self):
        return 60
    
class WaitForOtherPlayer(WaitPage):
    template_name = 'volleying/WaitPage.html'

    def is_displayed(self):
        return self.player.isSelecting

class Volley1(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        self.player.isSelecting = False
        self.player.get_others_in_group()[0].isSelecting = True

        if self.timeout_happened:
            self.player.set_timeout_data()

    def is_displayed(self):
        return self.group.isVolleying and self.player.id_in_group == 1

class Volley2(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.set_timeout_data()

    def is_displayed(self):
        return self.group.isVolleying and self.player.id_in_group == 2

class Volley3(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.set_timeout_data()
            
    def is_displayed(self):
        return self.group.isVolleying and self.player.id_in_group == 1

class Volley4(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.set_timeout_data()
            
    def is_displayed(self):
        return self.group.isVolleying

class Volley5(Page):
    form_model = 'group'
    template_name = 'volleying/Volley.html'

    def get_form_fields(self): 
        return self.group.get_remaining_movies()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.set_timeout_data()
            
    def is_displayed(self):
        return self.group.isVolleying and self.player.id_in_group == 2

class Results(Page):

    def is_displayed(self):
        return not self.group.isVolleying


class Demographics(Page):
    form_model = 'player'
    form_fields = ['rate_trailer', 'likely_watch', 'age', 'race', 'gender', 'comment']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry'] - time.time() > 3

    def before_next_page(self):
        if self.timeout_happened:
            self.player.set_timeout_data()

class Conclusion(Page):
    pass


page_sequence = [
    Introduction,
    ParticipantInfo,
    Instructions,
    Chat,
    Volley1,
    Volley2,
    Volley3,
    Volley4,
    Volley5,
    Demographics,
    Conclusion
]
