from django.urls import path
from rest_framework_nested import routers
from .views import MovieViewSet, MovieWatchListViewSet, MovieWatchViewSet

movie_router = routers.SimpleRouter()
movie_router.register(r'movies', MovieViewSet, basename='movie')

watch_list_router = routers.SimpleRouter()
watch_list_router.register(r'watch-list', MovieWatchListViewSet, basename='watch-list')

movie_watch_list_nested_router = routers.NestedSimpleRouter(watch_list_router, r'watch-list', lookup='watch_list')
movie_watch_list_nested_router.register(r'movies', MovieWatchViewSet, basename='movie-watch-list')