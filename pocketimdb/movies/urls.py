from django.urls import path
from rest_framework import routers
from .views import MovieViewSet

movie_router = routers.SimpleRouter()
movie_router.register(r'movies', MovieViewSet, basename='movie')