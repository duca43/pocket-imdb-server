from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import MovieWatchlist

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']
    
    email = serializers.CharField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, min_length=6, max_length=128, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

from pocketimdb.movies.serializers import BasicMovieSerializer

class MovieWatchlistSerializer(serializers.ModelSerializer):

    movie = BasicMovieSerializer(read_only=True)

    class Meta:
        model = MovieWatchlist
        fields = ['id', 'movie', 'is_watched'] 

class AddAndRemoveMovieWatchlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieWatchlist
        fields = ['movie']

class UpdateMovieWatchlistSerializer(serializers.ModelSerializer):

    is_watched = serializers.BooleanField(required=True)

    class Meta:
        model = MovieWatchlist
        fields = ['movie', 'is_watched']