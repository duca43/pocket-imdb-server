from django.urls import path
from rest_framework import routers
from .views import MovieViewSet, PopularMoviesViewSet

movieRouter = routers.SimpleRouter()
movieRouter.register(r'movies', MovieViewSet, basename='Movie')

popular_movie_router = routers.SimpleRouter()
popular_movie_router.register(r'popular-movies', PopularMoviesViewSet, basename='popular-movies')