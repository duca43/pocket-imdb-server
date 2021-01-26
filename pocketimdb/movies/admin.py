from django.contrib import admin
from .models import Movie, MovieLike

admin.site.register(Movie)
admin.site.register(MovieLike)