from django.db import models
from pocketimdb.movies.models import Movie
from pocketimdb.users.models import User

class MovieFeedback(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.BooleanField()

    class Meta:
        unique_together = ('movie', 'user',)
