from rest_framework import serializers
from .models import Movie, MovieLike, MovieComment
from pocketimdb.users.serializers import BasicUserSerializer

class MovieSerializer(serializers.ModelSerializer):

    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    user_liked_or_disliked = serializers.IntegerField(read_only=True, default=0)
    is_in_user_watchlist = serializers.BooleanField(read_only=True, default=None)
    did_user_watch = serializers.BooleanField(read_only=True, default=None)

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
                'is_in_user_watchlist',
                'did_user_watch',
                'visits']

class BasicMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cover_image_url', 'genre']

class AddMovieLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLike
        fields = ['like']  

class AddMovieCommentSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = MovieComment
        fields = ['content']

class MovieCommentSerializer(serializers.ModelSerializer):

    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = MovieComment
        fields = ['id', 'content', 'user', 'created_at']

class PopularMovieSerializer(serializers.ModelSerializer):

    likes = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'likes',]