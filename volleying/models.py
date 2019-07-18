from django.forms import CheckboxInput, MultipleChoiceField, widgets as w
from random import randint
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

    eliminateNegative = models.BooleanField(initial=True) 

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

    def movie_titles(self):
        return {'intouchables': 'The Intouchables', 
        'starfish': 'Starfish',
        'versailles': 'The Queen of Versailles',
        'hush': 'Hush',
        'father': 'Like Father',
        'tomboy': 'Tomboy',
        'phoenix': 'Dark Phoenix',
        'shazam': 'Shazam!',
        'dumbo': 'Dumbo',
        'survivalist': 'The Survivalist',
        'carol': 'Carol',
        'wild': 'Wild'}

    def movie_descriptions(self):
        return {'intouchables': "The Intouchables (Foreign) – two very different men bond and develop a very close relationship",
                'starfish': "Starfish (Science Fiction) – a young woman struggles with the death of her best friend",
                'versailles': "The Queen of Versailles (Documentary) – the economic crisis threatens the fortune of a billionaire family",
                'hush': "Hush (Horror) – a deaf writer living in the woods fights for her life when a killer appears in her window",
                'father': "Like Father (Rom-com) – a woman left at the altar takes her estranged father on her honeymoon",
                'tomboy': "Tomboy (Drama) - a 10-year old girl experiments with with her gender identity over the summer",
                'phoenix': "Dark Phoenix (Science Fiction/Action) – the X-Men embark on a risky mission in space",
                'shazam': "Shazam! (Superhero) - a 14-year-old transforms into an adult superhero with one magic word",
                'dumbo': "Dumbo (Fantasy) - a man and his two children take care of a newborn elephant that can fly",
                'survivalist': "The Survivalist (Thriller) - a survivalist hides in the forest protecting his crop from intruders",
                'carol': "Carol (Romance) - two women develop a fast bond that becomes a love with complicated consequences",
                'wild': "Wild (Adventure) - a woman's solo undertakes a hike as a way to recover from a recent personal tragedy"}


    def get_remaining_movies(self):
        if self.eliminateNegative:
            return {k for k,v in self.get_movies().items() if not v} 
        else: 
            movies = {k for k,v in self.get_movies().items() if not v}
            vals = {v for k,v in self.get_movies().items() if not v}
            vals.map(lambda x: not x)
            return movies
            #get all remaining movies and then mark them as false

    def get_eliminated_movie_descriptions(self):
        if self.eliminateNegative:
            return map(lambda x: self.movie_descriptions().get(x), list({k for k,v in self.get_movies().items() if v}))

    def volleying(self):
        if self.eliminateNegative:   
            return not list(self.get_movies().values()).count(False) == 1

    def last_movie(self):
        return list(self.get_remaining_movies())[0]

    def last_movie_name(self):
        return self.movie_titles().get(self.last_movie())


    numberVolleys = models.IntegerField(initial=0)

    volley = models.LongStringField(initial="")
                     
class Player(BasePlayer):

    isSelecting = models.BooleanField()

    first_name = models.StringField(
        label="What is your first name?",
        initial=""
    )

    mturkId = models.StringField(
        label="What is your mturk ID?",
        initial=""
    )

    mturkCode = models.StringField()

    mturkCompletitionCode = models.StringField(initial="")

    timed_out = models.BooleanField(initial=False)

    def role(self):
        if self.id_in_group == 1:
            return 'player1'
        else:
            return 'player2'

    def get_partner(self):
        return self.get_others_in_group()[0]

    def get_partner_name(self):
        return self.get_others_in_group()[0].first_name

    def get_code(self):
        code = ""
        if not self.timed_out:
            code = "movies" + str(randint(1000, 9999))
        else:
            code =  "timeout" + str(randint(1000, 9999))
        self.mturkCompletitionCode = code
        return code


    selectedMovie = models.StringField(initial="")

    
    satisfied = models.IntegerField(
        label="How satisfied are you with the choice you came to with your partner?",
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )

    partner_experience = models.LongStringField(
        label="Explain how your experience with your partner was:",
        blank=True,
    )

    rate_trailer = models.IntegerField(
        label="Please rate how much you liked the trailer",
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )

    likely_watch = models.IntegerField(
        label="how likely are you to watch the movie?",
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )

        # Demographic questions
    gender = models.IntegerField(
        label="What is your gender?",
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    age = models.IntegerField(
        label="how old are you??",
        min=18,
        max=130,
        blank=True
    )
    race = models.IntegerField(
        label="What is your race?",
        choices=[
            [1, 'White'],
            [2, 'Black, African-American'],
            [3, 'American Indian or Alaska Native'],
            [4, 'Asian or Asian-American'],
            [5, 'Pacific Islander'],
            [6, 'Some other race']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    education = models.IntegerField(
        label="Please indicate the highest level of education completed.",
        choices=[
            [1, 'Grammar school'],
            [2, 'High school or equivalent'],
            [3, 'Vocational/technical school (2 year)'],
            [4, 'Some college'],
            [5, 'College graduate (4 year)'],
            [6, 'Master\'s degree (MS, etc.)'],
            [7, 'Doctoral degree (PhD, etc.)'],
            [8, 'Professional degree (MD, JD, etc.)'],
            [9, 'Other']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    comment = models.LongStringField(
        label="Do you have any comments for the researchers? (Optional)", blank=True)
 