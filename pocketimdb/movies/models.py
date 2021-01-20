from django.db import models
from .constants import MOVIE_GENRES, ACTION

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    cover_image_url = models.CharField(max_length=300)
    genre = models.CharField(max_length=2, choices=MOVIE_GENRES, default=ACTION)
    visits = models.IntegerField(blank=True, default=0)