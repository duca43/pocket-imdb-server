from django.urls import path
from rest_framework import routers
from .views import MovieViewSet

movieRouter = routers.SimpleRouter()
movieRouter.register(r'movies', MovieViewSet, basename='Movie')
