from django.forms import CheckboxInput, MultipleChoiceField, widgets as w
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

    intouchables = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="The Intouchables (Foreign) – two very different men bond and develop a very close relationship")
    starfish =  models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Starfish (Science Fiction) – a young woman struggles with the death of her best friend")
    versailles = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="The Queen of Versailles (Documentary) – the economic crisis threatens the fortune of a billionaire family")
    hush = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Hush (Horror) – a deaf writer living in the woods fights for her life when a killer appears in her window")
    father = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Like Father (Rom-com) – a woman left at the altar takes her estranged father on her honeymoon")
    tomboy = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Tomboy (Drama) - a 10-year old girl experiments with with her gender identity over the summer")
    phoenix = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Dark Phoenix (Science Fiction/Action) – the X-Men embark on a risky mission in space")
    shazam = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Shazam! (Superhero) - a 14-year-old transforms into an adult superhero with one magic word")
    dumbo = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Dumbo (Fantasy) - a man and his two children take care of a newborn elephant that can fly")
    survivalist = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="The Survivalist (Thriller) - a survivalist hides in the forest protecting his crop from intruders")
    carol = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Carol (Romance) - two women develop a fast bond that becomes a love with complicated consequences")
    wild = models.BooleanField(blank=True, widget=CheckboxInput, initial=False, label="Wild (Adventure) - a woman's solo undertakes a hike as a way to recover from a recent personal tragedy")

    def get_movies(self):
        return {'intouchables': self.intouchables, 
        'starfish': self.starfish,
        'versailles': self.versailles,
        'hush': self.hush,
        'father': self.father,
        'tomboy': self.tomboy,
        'phoenix': self.phoenix,
        'shazam': self.shazam,
        'dumbo': self.dumbo,
        'survivalist': self.survivalist,
        'carol': self.carol,
        'wild': self.wild}

    def get_remaining_movies(self):
        return {k for k,v in self.get_movies().items() if not v} 


    def volleying(self):
        #still_available = self.get_movies()
        return True #any(still_available) and not any(still_available)
                 
    
    isVolleying = models.BooleanField(initial= True)


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

    def get_partner_name(self):
        return self.get_others_in_group()[0].first_name