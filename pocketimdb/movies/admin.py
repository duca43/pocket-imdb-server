from django.contrib import admin
from .models import Movie, MovieLike, WatchList, MovieWatch

admin.site.register(Movie)
admin.site.register(MovieLike)
admin.site.register(WatchList)
admin.site.register(MovieWatch)