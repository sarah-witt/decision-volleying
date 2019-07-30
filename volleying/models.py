from django.forms import CheckboxInput, MultipleChoiceField, widgets as w
from random import randint
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.db.models import Model, ForeignKey

class Constants(BaseConstants):
    name_in_url = 'volleying'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for group_id, group in enumerate(self.get_groups()):
            group.eliminateNegative = group_id % 2 == 0
            group.generate_movie_options()

class Group(BaseGroup):

    def generate_movie_options(self):
        for name, movie in self.movies().items():
            movieObj = self.movieselection_set.create(group=self, movie_key=name, movie_name=movie["title"], movie_description=movie["description"], movie_isRemaining=True, movie_isChecked=False)
            movieObj.save()

    eliminateNegative = models.BooleanField(initial=True) 

    def movies(self):
        return {'intouchables': {"description": "The Intouchables (Foreign) – two very different men bond and develop a very close relationship", "title":  "The Intouchables"},
                'starfish': {"description": "Starfish (Science Fiction) – a young woman struggles with the death of her best friend", "title": "Starfish"}, 
                'versailles': {"description": "The Queen of Versailles (Documentary) – the economic crisis threatens the fortune of a billionaire family", "title": "The Queen of Versailles"},
                'hush': {"description": "Hush (Horror) – a deaf writer living in the woods fights for her life when a killer appears in her window", "title": "Hush"},
                'father': {"description": "Like Father (Rom-com) – a woman left at the altar takes her estranged father on her honeymoon", "title": "Like Father"},
                'tomboy': {"description": "Tomboy (Drama) - a 10-year old girl experiments with with her gender identity over the summer", "title": "Tomboy"},
                'phoenix': {"description": "Dark Phoenix (Science Fiction/Action) – the X-Men embark on a risky mission in space", "title": "Dark Phoenix"},
                'shazam': {"description": "Shazam! (Superhero) - a 14-year-old transforms into an adult superhero with one magic word", "title": "Shazam!"},
                'dumbo': {"description": "Dumbo (Fantasy) - a man and his two children take care of a newborn elephant that can fly", "title": "Dumbo"},
                'survivalist': {"description": "The Survivalist (Thriller) - a survivalist hides in the forest protecting his crop from intruders", "title": "The Survivalist"},
                'carol': {"description": "Carol (Romance) - two women develop a fast bond that becomes a love with complicated consequences", "title": "Carol"},
                'wild': {"description": "Wild (Adventure) - a woman's solo undertakes a hike as a way to recover from a recent personal tragedy", "title": "Wild"}}

    def get_movies(self):
        return MovieSelection.objects.filter(group__exact=self)

    def get_remaining_movies(self):
        return self.get_movies().filter(movie_isRemaining=True)

    def get_eliminated_movies(self):
        return self.get_movies().filter(movie_isRemaining=False)

    def get_eliminated_movie_descriptions(self):
        return map(lambda mov: mov.movie_description, self.get_eliminated_movies())

    def volleying(self):
        return not len(self.get_remaining_movies()) == 1

    def last_movie(self):
        return list(self.get_remaining_movies())[0]

    def last_movie_name(self):
        return self.get_remaining_movies()[0].movie_name

    numberVolleys = models.IntegerField(initial=0)

    volley = models.LongStringField(initial="")

class MovieSelection(Model):
    group = ForeignKey(Group) 
    movie_key = models.StringField()
    movie_name = models.StringField()
    movie_description = models.StringField()
    movie_isRemaining = models.BooleanField()
    movie_isChecked = models.BooleanField(initial=False, widget=CheckboxInput)

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
        choices=[[1, "Very Unsatisfied"], [2, "Unsatisfied"], [3, "Neutral"], [4, "Satisfied"], [5, "Very Satisfied"]],
        widget=widgets.RadioSelect,
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
        label="how old are you?",
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
 