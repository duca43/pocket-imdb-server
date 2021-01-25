from rest_framework import serializers
from .models import Movie, MovieLike, WatchList, MovieWatch

class MovieSerializer(serializers.ModelSerializer):

    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    user_liked_or_disliked = serializers.IntegerField(read_only=True, default=0)
    in_user_watch_list = serializers.BooleanField(read_only=True, default=None)
    user_watched = serializers.BooleanField(read_only=True, default=None)

    class Meta:
        model = Movie
        fields = ['id', 
                'title',
                'description', 
                'cover_image_url', 
                'genre', 
                'likes', 
                'dislikes', 
                'user_liked_or_disliked',
                'in_user_watch_list',
                'user_watched',
                'visits']

class BasicMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cover_image_url', 'genre']

class AddMovieLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLike
        fields = ['like']

class MovieWatchSerializer(serializers.ModelSerializer):

    movie = BasicMovieSerializer(read_only=True)

    class Meta:
        model = MovieWatch
        fields = ['movie', 'watched']  

class SetMovieWatchSerializer(serializers.ModelSerializer):

    watched = serializers.BooleanField(required=True)

    class Meta:
        model = MovieWatch
        fields = ['watched']

class WatchListSerializer(serializers.ModelSerializer):

    movies = MovieWatchSerializer(source='moviewatch_set', many=True)

    class Meta:
        model = WatchList
        fields = ['id', 'movies']    
