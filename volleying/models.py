from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'volleying'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    first_name = models.StringField(
        label="What is your first name?",
        initial=""
    )

    sonaId = models.StringField(
        label="What is your SONA ID?",
        initial=""
    )

    def role(self):
        if self.id_in_group == 1:
            return 'player1'
        else:
            return 'player2'

    def get_partner(self):
        return self.get_others_in_group()[0]