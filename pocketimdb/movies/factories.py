from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from factory import Faker
from .models import Movie
from .utils import MOVIE_GENRES

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker('sentence', nb_words=3, variable_nb_words=True)
    description = Faker('text', max_nb_chars=200)
    cover_image_url = Faker('image_url')
    genre = FuzzyChoice([x[0] for x in MOVIE_GENRES])
