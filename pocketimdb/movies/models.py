from django.db import models
from django.contrib.auth import get_user_model
from .constants import MOVIE_GENRES, ACTION

User = get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    cover_image_url = models.CharField(max_length=300)
    genre = models.CharField(max_length=2, choices=MOVIE_GENRES, default=ACTION)

class MovieLike(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')

    class Like(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    like = models.IntegerField(choices=Like.choices)

    class Meta:
        unique_together = ('movie', 'user',)