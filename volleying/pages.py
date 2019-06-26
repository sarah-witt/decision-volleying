from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import Constants
import re
import time
import random


class Introduction(Page):
    def get_timeout_seconds(self):
        pass

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
    def get_timeout_seconds(self):
        pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Introduction,
    ParticipantInfo,
    Instructions,
    Results
]
