from django.contrib import admin
from .models import Movie, MovieLike, MovieComment

admin.site.register(Movie)
admin.site.register(MovieLike)
admin.site.register(MovieComment)
