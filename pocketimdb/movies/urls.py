from rest_framework_nested import routers
from .views import MovieViewSet, MovieCommentsViewSet, PopularMoviesViewSet

movie_router = routers.SimpleRouter()
movie_router.register(r'movies', MovieViewSet, basename='movie')

movie_nested_router = routers.NestedSimpleRouter(movie_router, r'movies', lookup='movie')
movie_nested_router.register(r'comments', MovieCommentsViewSet, basename='movie-comments')

popular_movie_router = routers.SimpleRouter()
popular_movie_router.register(r'popular-movies', PopularMoviesViewSet, basename='popular-movies')